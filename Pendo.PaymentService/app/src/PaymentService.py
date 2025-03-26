# 
# Python FastAPI implentation for Pendo.PaymentService
# Author: Alexander McCall
# Created: 12/02/2025
#

# univeral libaries
from fastapi import FastAPI, HTTPException, Depends, Request
import logging, sys, stripe

# endpoint commands
from .endpoints.ViewBalanceCmd import ViewBalanceCommand
from .endpoints.PendingBookingCmd import PendingBookingCommand
from .endpoints.PaymentMethodsCmd import PaymentMethodsCommand
from .endpoints.PaymentSheetCmd import PaymentSheetCommand
from .endpoints.StripeWebhookCmd import StripeWebhookCommand
from .endpoints.RefundPaymentCmd import RefundPaymentCommand
from .endpoints.CompletedBookingCmd import CompletedBookingCommand
from .endpoints.CreatePayoutCmd import CreatePayoutCommand

# database handling
from .db.PendoDatabase import UserBalance
from .db.PendoDatabaseProvider import get_db, Session, text, environment, configProvider

# requests and returns
from .requests.PaymentRequests import GetwithUUID, MakePendingBooking, PaymentSheetRequest, RefundPaymentRequest
from .returns.PaymentReturns import ViewBalanceResponse, StatusResponse, PaymentMethodResponse, PaymentSheetResponse


if environment == "Development":
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )

logger = logging.getLogger(__name__)
logger.info("Starting Pendo.PaymentService.Api")

app = FastAPI(title="Pendo.PaymentService.Api", 
    version="1.0.0",
    root_path="/api/PaymentService")

@app.get("/HealthCheck", tags=["HealthCheck"])
def test_db(db: Session = Depends(get_db)):
    logger.info("Testing DB connection...")
    try:
        db.execute(text("SELECT 1"))
        logger.info("DB connection successful")
        return {"db_connection": "successful"}
    except Exception as e:
        logger.error(f"DB connection failed. Error: {str(e)}")
        raise HTTPException(500, detail="DB connection failed.")

@app.post("/PaymentSheet", tags=["Stripe"])
def PaymentSheet(request: PaymentSheetRequest, db: Session = Depends(get_db)) -> PaymentSheetResponse:
    configProvider.LoadStripeConfiguration(db)
    secret = configProvider.StripeConfiguration.secret

    response = PaymentSheetCommand(logging.getLogger("PaymentSheet"), request.UserId, request.Amount, secret).Execute()

    
    if response.Status != "success":
        raise HTTPException(400, detail=response.Error)
    else:
        return response


@app.post("/PaymentMethods", tags=["Pre-booking"])
def PaymentMethods(request: GetwithUUID, db: Session = Depends(get_db)) -> PaymentMethodResponse:
    """
    Used to query stripe for the customers saved payment methods, to display before adding another card or contiuning with a booking
    """
    response = PaymentMethodsCommand(logging.getLogger("PaymentMethods"), request.UserId, db).Execute()

    if response.Status != "success":
        raise HTTPException(400, detail=response.Error)
    else:
        return response

@app.post("/StripeWebhook", tags=["Stripe"])
async def StripeWebhook(request: Request) -> StatusResponse:

    # update user balance

    requestBody = await request.json()
    customer = requestBody["data"]["object"]["customer"]
    amount = requestBody["data"]['object']['amount'] / 100

    if (customer == None) or (amount == None):
        raise HTTPException(400, detail="Customer or ammount cannnot be parsed from the request")
    
    response = StripeWebhookCommand(logging.getLogger("StripeWebhook"), customer, amount).Execute()

    if response.Status != "success":
        raise HTTPException(400, detail=response.Error)
    else:
        return response


@app.post("/PendingBooking", tags=["At Booking time"])
def PendingBooking(request: MakePendingBooking, db: Session = Depends(get_db)) -> StatusResponse:
    """
    Used when a booking is created in the pending state
    """
    response = PendingBookingCommand(logging.getLogger("PendingBooking"), request.BookingId).Execute()

    if response.Status != "success":
        raise HTTPException(400, detail=response.Error)
    else:
        return response

@app.post("/CompletedBooking", tags=["On booking confirmation"])
def CompletedBooking(request: MakePendingBooking, db: Session = Depends(get_db)) -> StatusResponse:
    """
    Used when a booking status changes to complete, takes payment from user's saved card details and non-pending balance
    """
    # TODO: Complete Confirm endpoint - Catherine
    # See src/endpoints/CompletedBookingCmd

    response = CompletedBookingCommand(logging.getLogger("CompleteBooking"), request.BookingId).Execute()
    if response.Status != "success":
        raise HTTPException(400, detail=response.Error)
    else:
        return response

    return StatusResponse(Status="success")

@app.post("/ViewBalance", tags=["Anytime"])
def ViewBalance(request: GetwithUUID, db: Session = Depends(get_db)) -> ViewBalanceResponse:
    """
    Used to query a users balance, both pending and non-pending
    """
    BalanceSheet = ViewBalanceCommand(logging.getLogger("ViewBalance"), request.UserId).Execute()
    if BalanceSheet.Status != "success":
        raise HTTPException(400, detail=BalanceSheet.Error)
    else:
        return BalanceSheet


@app.post("/RefundPayment", tags=["Anytime"])
def refund(request: RefundPaymentRequest, db: Session = Depends(get_db)) -> StatusResponse:
    """
    Used to refund a payment on a cancelled journey, revert any pending balance.
    """
    # TODO: Complete refund endpoint - Catherine
    # See src/endpoints/RefundPaymentCmd

    response = RefundPaymentCommand(logging.getLogger("RefundPayment"), request.BookingId, request.CancelledById, request.LatestPrice, request.CancellationTime, request.JourneyTime).Execute()
    if response.Status != "success":
        raise HTTPException(400, detail=response.Error)
    else:
        return response


@app.post("/CreatePayout", tags=["Anytime"])
def CreatePayout(request: GetwithUUID, db: Session = Depends(get_db)) -> StatusResponse:
    """
    Used to retrieve the non-pending value of a user. Will send an email to Admin with value to process payment
    """
    # TODO: Complete Payout endpoint - Alex

    response = CreatePayoutCommand(logging.getLogger("CreatePayout"), request.UserId).Execute()
    if response.Status != "success":
        raise HTTPException(400, detail=response.Error)
    else:
        return response