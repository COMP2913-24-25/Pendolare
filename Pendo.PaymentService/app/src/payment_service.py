# 
# Python FastAPI implentation for Pendo.PaymentService
# Author: Alexander McCall
# Created: 12/02/2025
#

from fastapi import FastAPI
from src.PendoDatabase import Transaction
from pydantic import BaseModel

class Take

app = FastAPI()

@app.post("/takeStripe")
def take():

    # TODO: Complete TakeStipe endpoint

    # get fee - from journey?
    # get adminID

    # increase pending balance by journey value (minus fee!)
    # increase fee balance

    return {"Hello" : "World"}

@app.post("/takeBalance")
def take():

    # TODO: Complete TakeStipe endpoint

    # get fee - from journey?
    # get adminID

    # increase pending balance by journey value (minus fee!)
    # increase fee balance

    return {"Hello" : "World"}

@app.post("/confirm")
def confirm():

    # TODO: Complete Confirm endpoint

    # input: bookingID or journeyID, advertiserID

    # get fee - from journey?

    # decrease pending balance by journey value (minus fee!)
    # increase non-pending balance by journey value (minus fee!)


    return {"Hello" : "World"}

@app.get("/view")
def view():

    # TODO: Complete View endpoint
    
    # input: userID

    # Query non-pending balance

    # Query pending balance

    # return both

    return {"status" : "success",
            "pending": "value",
            "non-pending": "value"}

@app.get("/calculate")
def calculate():

    # TODO: Complete calculate endpoint

    # input: userID, journeyID, useCredit?

    # query non-pending balance

    # return journey cost - credit if possible and requested

@app.post("/refund")
def refund():

    # TODO: Complete refund endpoint

    return {"Hello" : "World"}

@app.post("/payout")
def payout():
    
    # TODO: Complete Payout endpoint

    return {"Hello" : "World"}

def some_testing_function(param):
    return param