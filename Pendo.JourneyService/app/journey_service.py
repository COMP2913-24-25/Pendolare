from typing import Optional, List
from datetime import datetime
import datetime
import logging
import sys
import time
from uuid import UUID
from .request_lib import GetJourneysRequest, CreateJourneyRequest
from .journey_repository import JourneyRepository

from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import and_

from .PendoDatabase import Journey, User
from .parameter_filtering import FilterJourneys
from .parameter_checking import CheckJourneyData

app = FastAPI()

DATABASE_URL = "mssql+pymssql://SA:reallyStrongPwd123@172.17.0.2:1433/Pendo.Database"

Base = declarative_base()

logger = logging.getLogger(__name__)

max_retries = 10
retry_count = 0
while retry_count < max_retries:
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        break
    except OperationalError as e:
        logger.error("Database connection failed. Retrying in 5 seconds...")
        time.sleep(5)
        retry_count += 1
else:
    logger.error("Failed to connect to the database after multiple attempts.")
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Starting Pendo.JourneyService.Api")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def journey():
    return {"message": "Journey"}

@app.post("/CreateJourney/")
def create_journey(JourneyParam: CreateJourneyRequest, db: Session = Depends(get_db)):
    logger.debug("Creating new journey data: %s", JourneyParam.dict())

    try:
        check_journey_data = CheckJourneyData(JourneyParam)
        response = check_journey_data.check_inputs()
        logger.debug("Journey data after validation: %s", response)
    except Exception as e:
        logger.error(f"Failed to create journey during validation: {e}")
        return {"Status": "Failed", "Message": str(e)}
    
    try:
        repo = JourneyRepository(db)
        journey = repo.create_journey(response)
        logger.info("Created new journey with ID: %s", journey.JourneyId)
        return journey
    except Exception as e:
        logger.error(f"Failed to create journey during database operation: {e}")
        return {"Status": "Failed", "Message": str(e)}
    

@app.post("/ViewJourney/")
def get_journeys(FilterParam: GetJourneysRequest, db: Session = Depends(get_db)):
    logger.debug("Getting journey data with filters: %s", FilterParam.dict())

    filter_journeys = FilterJourneys(FilterParam, db)
    filters = filter_journeys.apply_filters()

    repo = JourneyRepository(db)
    journeys_query = repo.get_journeys(filters)

    #Apply sorting if specified by the request parameters
    if FilterParam.SortByPrice:
        if FilterParam.SortByPrice.lower() == "asc":
            journeys_query = journeys_query.order_by(asc(Journey.AdvertisedPrice))
        elif FilterParam.SortByPrice.lower() == "desc":
            journeys_query = journeys_query.order_by(desc(Journey.AdvertisedPrice))

    journeys = journeys_query.all()

    return journeys

@app.put("/LockJourney/{JourneyId}")
def lock_journey(JourneyId: UUID, response : Response, db: Session = Depends(get_db)):
    logger.debug(f"Locking journey ID {JourneyId}")
    try:
        repo = JourneyRepository(db)
        journey = repo.lock_journey(JourneyId, response)
        return journey
    except Exception as e:
        logger.error(f"Failed to lock journey: {e}")
        return {"Status" : "Failed", "Message" : str(e)}

def some_testing_function(param):
    return param