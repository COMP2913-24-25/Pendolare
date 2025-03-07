from typing import Optional, List
from datetime import datetime
import datetime
import logging
import sys
import time
from uuid import UUID
from .request_lib import GetJourneysRequest
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

'''
class CreateJourneyRequest(BaseModel):
    user_id: UUID
    advertised_price: float
    start_name: str
    start_long: float
    start_lat: float
    end_name: str
    end_long: float
    end_lat: float
    start_date: datetime.datetime
    repeat_until: datetime.datetime
    start_time: datetime.datetime
    max_passengers: int
    reg_plate: str
    currency_code: str = "GBP"
    journey_type: int = 1
    recurrance: Optional[str] = None
    journey_status_id: int = 1
    boot_width: Optional[float] = None
    boot_height: Optional[float] = None
    locked_until: Optional[datetime.datetime] = None
'''

def create_journey_data(
    user_id: UUID,
    advertised_price: float,
    start_name: str,
    start_long: float,
    start_lat: float,
    end_name: str,
    end_long: float,
    end_lat: float,
    start_date: datetime.datetime,
    repeat_until: datetime.datetime,
    start_time: datetime.datetime,
    max_passengers: int,
    reg_plate: str,
    currency_code: str = "GBP",
    journey_type: int = 1,
    recurrance: Optional[str] = None,
    journey_status_id: int = 1,
    boot_width: Optional[float] = None,
    boot_height: Optional[float] = None,
    locked_until: Optional[datetime.datetime] = None
):
    return {
        "UserId": user_id,
        "AdvertisedPrice": advertised_price,
        "StartName": start_name,
        "StartLong": start_long,
        "StartLat": start_lat,
        "EndName": end_name,
        "EndLong": end_long,
        "EndLat": end_lat,
        "StartDate": start_date,
        "RepeatUntil": repeat_until,
        "StartTime": start_time,
        "MaxPassengers": max_passengers,
        "RegPlate": reg_plate,
        "CurrencyCode": currency_code,
        "JourneyType": journey_type,
        "Recurrance": recurrance,
        "JourneyStatusId": journey_status_id,
        "BootWidth": boot_width,
        "BootHeight": boot_height,
        "LockedUntil": locked_until
    }



@app.post("/CreateJourney/")
def create_journey(journey_data: dict = Depends(create_journey_data), db: Session = Depends(get_db)):
    logger.debug("Creating new journey data: %s", journey_data)
    journey = Journey(**journey_data)
    db.add(journey)
    db.commit()
    db.refresh(journey)
    logger.info("Created new journey with ID: %s", journey.JourneyId)
    return journey



@app.post("/ViewJourney/")
def get_journeys(FilterParam: GetJourneysRequest, db: Session = Depends(get_db)):
    logger.debug("Getting journey data with filters: %s", FilterParam.dict())

    filter_journeys = FilterJourneys(FilterParam, db)
    filters = filter_journeys.apply_filters()

    repo = JourneyRepository(db)
    journeys_query = repo.get_journeys(filters)

    # Apply sorting by price if specified
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