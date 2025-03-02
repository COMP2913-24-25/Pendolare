# 
# Python FastAPI implentation for Pendo.JourneyService
# Author: Catherine Weightman
# Created: 13/02/2025
#

from fastapi import FastAPI, HTTPException, Depends
#from .PendoDatabase import Journeys
#from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from .create_journey import CreateJourneyCommand
from .get_journeys import GetJourneysCommand
#from .PendoDatabase import Journeys  # Import the model from PendoDatabase.py

from .db_provider import get_db, Session, text, configProvider, environment

from .requests import CreateJourneyRequest, GetJourneysRequest
import sys

import logging

from .create_journey import CreateJourneyCommand

if environment == "Development":
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        #filename='Pendo.JourneyService.log',
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )

logger = logging.getLogger(__name__)
logger.info("Starting Pendo.JourneyService.Api")


app = FastAPI()

#LOGGING THING

'''
class Journeys(BaseModel):
    UserId: str
    Cost: float
    StartName: str
    StartLong: float
    StartLat: float
    EndName: str
    EndLong: float
    EndLat: float
    JourneyType: int
    StartDate: str
    RepeatUntil: Optional[str] = None
    Recurrance: Optional[str] = None
    Status: int
    MaxPassengers: int
    RegPlate: str
    BootWidth: float
    BootHeight: float
'''

#@app.get("/")
#def journey():
#    return {"message": "Journey"}

@app.get("/GetJourneys")
def journey(request: GetJourneysRequest, db: Session = Depends(get_db)):
    logger.debug("Getting bookings...")
    return GetJourneysCommand(request, logging.getLogger("GetBookingsCommand")).Execute()  
    #return {"message": "View Journey"}

@app.post("/CreateJourney")
def create_journey(request: CreateJourneyRequest, db: Session = Depends(get_db)):
    #item = "Create Journey"
    #return item
    logger.debug(f"Creating booking with request {request}.")
    return CreateJourneyCommand(request, logging.getLogger("CreateJourneyCommand")).Execute()

'''
@app.post("/create/")
def create_journey(journey: Journeys):
    #return {"message": "Journey created successfully", "data": journey.dict()}
    new_journey = Journeys(
        JourneyId=uuid4(),
        UserId=journey.UserId,  # Now expects UUID
        Cost=journey.Cost,
        StartName=journey.StartName,
        StartLong=journey.StartLong,
        StartLat=journey.StartLat,
        EndName=journey.EndName,
        EndLong=journey.EndLong,
        EndLat=journey.EndLat,
        JourneyType=journey.JourneyType,
        StartDate=journey.StartDate,
        RepeatUntil=journey.RepeatUntil,
        Recurrance=journey.Recurrance,
        Status=journey.Status,
        MaxPassengers=journey.MaxPassengers,
        RegPlate=journey.RegPlate,
        BootWidth=journey.BootWidth,
        BootHeight=journey.BootHeight
    )

    #ADD TO DB HERE

    #return {"message": "Journey created successfully", "data": new_journey}
    return {"message": "Create Journey"}
'''
'''
@app.post("/create/")
def create_journey(journey: Journeys):
    new_journey = Journeys(
        UserId=journey.UserId,
        Cost=journey.Cost,
        StartName=journey.StartName,
        StartLong=journey.StartLong,
        StartLat=journey.StartLat,
        EndName=journey.EndName,
        EndLong=journey.EndLong,
        EndLat=journey.EndLat,
        JourneyType=journey.JourneyType,
        StartDate=journey.StartDate,
        RepeatUntil=journey.RepeatUntil,
        Recurrance=journey.Recurrance,
        Status=journey.Status,
        MaxPassengers=journey.MaxPassengers,
        RegPlate=journey.RegPlate,
        BootWidth=journey.BootWidth,
        BootHeight=journey.BootHeight
    )
    
    return {"message": "Create Journey"}
'''

def some_testing_function(param):
    return param