# 
# Python FastAPI implentation for Pendo.PaymentService
# Author: Alexander McCall
# Created: 12/02/2025
#

from fastapi import FastAPI, HTTPException, Depends, Request
import logging, sys, stripe
from .endpoints.ViewBalanceCmd import ViewBalanceCommand
from .endpoints.PendingBookingCmd import PendingBookingCommand
from .endpoints.PaymentMethodsCmd import PaymentMethodsCommand
from .endpoints.PaymentSheetCmd import PaymentSheetCommand
from .db.PendoDatabase import UserBalance
from .db.PendoDatabaseProvider import get_db, Session, text, configProvider, environment
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
    
    response = PaymentSheetCommand(logging.getLogger("PaymentMethods"), request.UserId, request.Amount, db).Execute()

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
def StripeWebhook(request: Request) -> StatusResponse:

    # update user balance

    return StatusResponse(Status="success")


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
    # TODO: Complete Confirm endpoint

    # input: bookingID

    # get fee - from booking

    # decrease booker non-pending by booking value
    
    # if leftover cost
        # STRIPE - take payment

    # decrease pending balance by journey value (minus fee!)
    # increase non-pending balance by journey value (minus fee!)

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
    # TODO: Complete refund endpoint

    # input: Booking Object, cancelled by 

    # > 15 mins before start?
    fullRefund = False

    # if driver cancelled
        # reduce driver pending
        # credit passenger non-pending

    # if passenger cancelled

    return StatusResponse(Status="success")

@app.post("/CreatePayout", tags=["Anytime"])
def CreatePayout(request: MakePendingBooking, db: Session = Depends(get_db)) -> StatusResponse:
    """
    Used to retrieve the non-pending value of a user. Will send an email to Admin with value to process payment
    """
    # TODO: Complete Payout endpoint

    # call get balance

    # email user with payout amount (non-pending)
    # email admin with notice to payout / invoice to pay

    return StatusResponse(Status="success")

def some_testing_function(param):
    return param