# 
# Python FastAPI implentation for Pendo.PaymentService
# Author: Alexander McCall
# Created: 12/02/2025
#

from fastapi import FastAPI
from src.PendoDatabase import Transaction
from pydantic import BaseModel



app = FastAPI()

@app.post("/AuthenticatePaymentDetails")
def AuthenticatePaymentDetails():
    """
    Used to save and authorise the card details of a user to Stripe's Customer list for our Account
    """

    # TODO: Complete AuthenticatePaymentDetails Endpoint

    # query stripe to see if customer already exists
        # if not, create customer

    # create stripe.SetupIntent with card from body

    return {"status" : "success"}


@app.get("/PaymentMethods")
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


@app.post("/PendingBooking")
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

@app.post("/ConfirmedBooking")
def ConfirmedBooking():

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

@app.get("/ViewBalance")
def ViewBalance():

    # TODO: Complete View endpoint
    
    # input: userID

    # Query non-pending balance

    # Query pending balance

    # return both

    return {"status" : "success",
            "pending": "value",
            "non-pending": "value"}


@app.post("/RefundPayment")
def refund():

    # TODO: Complete refund endpoint

    # input: BookingID

    # logic needs confirming, can booking be refunded after confirmed?

    return {"status" : "success"}

@app.post("/CreatePayout")
def CreatePayout():
    
    # TODO: Complete Payout endpoint

    # call get balance

    # email user with payout amount (non-pending)
    # email admin with notice to payout / invoice to pay

    return {"status" : "success"}

def some_testing_function(param):
    return param