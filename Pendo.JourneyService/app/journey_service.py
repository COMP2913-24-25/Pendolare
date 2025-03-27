import logging
import sys
from uuid import UUID
from .request_lib import GetJourneysRequest, CreateJourneyRequest, AdjustPriceRequest
from .journey_repository import JourneyRepository

from fastapi import Depends, HTTPException, FastAPI, Response
from sqlalchemy import  asc, desc
from sqlalchemy.orm import Session

from sqlalchemy.orm import joinedload
from sqlalchemy.sql import and_

from .PendoDatabase import Journey
from .parameter_filtering import FilterJourneys
from .parameter_checking import CheckJourneyData
from .PendoDatabaseProvider import get_db, text



app = FastAPI(
    title="Pendo.JourneyService.Api",
    version="1.0.0",
    root_path="/api/Journey"
)

logger = logging.getLogger(__name__)


logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Starting Pendo.JourneyService.Api")

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

@app.post("/CreateJourney")
def create_journey(JourneyParam: CreateJourneyRequest, db: Session = Depends(get_db)):
    logger.debug("Creating new journey data: %s", JourneyParam.model_dump())

    try:
        check_journey_data = CheckJourneyData(JourneyParam, logger)
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
    
@app.post("/ViewJourney")
def get_journeys(FilterParam: GetJourneysRequest, db: Session = Depends(get_db)):
    logger.debug("Getting journey data with filters: %s", FilterParam.dict())

    filter_journeys = FilterJourneys(FilterParam, db)
    filters = filter_journeys.apply_filters()

    repo = JourneyRepository(db)
    journeys_query = repo.get_journeys(filters).options(joinedload(Journey.User_, innerjoin=False))

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

@app.put("/AdjustPrice/{journey_id}")
async def adjust_price(journey_id: int, request: AdjustPriceRequest):
    logger.debug(f"Adjusting price for journey ID {journey_id}")
    try:
        repo = JourneyRepository(db)
        journey = repo.adjust_journey(JourneyId, request)
        return journey
    except Exception as e:
        logger.error(f"Failed to adjust price journey: {e}")
        return {"Status" : "Failed", "Message" : str(e)}