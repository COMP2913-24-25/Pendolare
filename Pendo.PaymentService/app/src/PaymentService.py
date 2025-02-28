# 
# Python FastAPI implentation for Pendo.PaymentService
# Author: Alexander McCall
# Created: 12/02/2025
#

from fastapi import FastAPI, HTTPException, Depends
import logging, sys
from .PendoDatabaseProvider import get_db, Session, text, configProvider, environment

if environment == "Development":
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        #filename='Pendo.PaymentService.log',
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

app = FastAPI()

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

def queryBalance(userID):
    nonpending = 0
    pending = 0 
    # input: userID

    # Query non-pending balance

    # Query pending balance

    # return both
    return pending, non-pending

@app.post("/AuthenticatePaymentDetails", tags=["Pre-booking"])
def AuthenticatePaymentDetails():
    """
    Used to save and authorise new card details of a user, to Stripe's Customer list
    """

    # TODO: Complete AuthenticatePaymentDetails Endpoint

    # query stripe to see if customer already exists
        # if not, create customer

    # create stripe.SetupIntent with card from body

    return {"status" : "success"}


@app.get("/PaymentMethods", tags=["Pre-booking"])
def PaymentMethods():
    """
    Used to query stripe for the customers saved payment methods, to display before adding another card or contiuning with a booking
    """
    # TODO: Complete PaymentMethods endpoint
    
    # input: userID

    # query stripe for payments method list for customer

    # return list to client

    return {"status" : "success",
            "PaymentMethods" : "List of stripe payment methods go here"}


@app.post("/PendingBooking", tags=["At Booking time"])
def PendingBooking():
    """
    Used when a booking is created in the pending state
    """
    # TODO: Complete PendingBooking endpoint

    # input: journeyID

    # get fee - from journey
    # get adminID - from db

    # increase admin pending balance by fee
    # increase advertiser pending balance by journey value (minus fee!)

    return {"status" : "success"}

@app.post("/ConfirmedBooking", tags=["On booking confirmation"])
def ConfirmedBooking():
    """
    Used when a booking status changes to confirmed, takes payment from user's saved card details and non-pending balance
    """
    # TODO: Complete Confirm endpoint

    # input: bookingID

    # get fee - from booking
    # get adminID - from db
    
    # decrease admin pending balance by fee
    # increase admin non-pending balance by fee

    # decrease booker non-pending by booking value
    
    # if leftover cost
        # STRIPE - take payment

    # decrease pending balance by journey value (minus fee!)
    # increase non-pending balance by journey value (minus fee!)

    return {"status" : "success"}

@app.get("/ViewBalance", tags=["Anytime"])
def ViewBalance():

    # TODO: Complete View endpoint
    
    # pending, non-pending = queryBalance(userID)

    return {"status" : "success",
            "pending": "value",
            "non-pending": "value"}


@app.post("/RefundPayment", tags=["Anytime"])
def refund():

    # TODO: Complete refund endpoint

    # input: BookingID

    # logic needs confirming, can booking be refunded after confirmed?

    return {"status" : "success"}

@app.post("/CreatePayout", tags=["Anytime"])
def CreatePayout():
    
    # TODO: Complete Payout endpoint

    # call get balance

    # email user with payout amount (non-pending)
    # email admin with notice to payout / invoice to pay

    return {"status" : "success"}

def some_testing_function(param):
    return param