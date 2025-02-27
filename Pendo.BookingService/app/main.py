import logging

from fastapi import FastAPI, HTTPException, Depends
from .db_provider import get_db, Session, text, configProvider, environment
from .create_booking import CreateBookingCommand
from .get_bookings import GetBookingsCommand
from .requests import CreateBookingRequest, GetBookingsRequest
from .email_sender import MailSender
import sys

if environment == "Development":
    logging.basicConfig(
        level=logging.DEBUG,
        filename='Pendo.BookingService.log',
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )

logger = logging.getLogger(__name__)
logger.info("Starting Pendo.BookingService.Api")

app = FastAPI(
    title="Pendo.BookingService.Api", 
    version="1.0.0",
    root_path="/api")

logger.info("Initialising Mail Sender Service...")
mailSender = MailSender(configProvider.LoadEmailConfiguration(next(get_db())))
logger.info("Mail Sender Service Initialised")

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

@app.post("/GetBookings", tags=["Get Bookings"])
def get_bookings(request: GetBookingsRequest, db: Session = Depends(get_db)):
    logger.debug("Getting bookings...")
    return GetBookingsCommand(request, logging.getLogger("GetBookingsCommand")).Execute()

@app.post("/CreateBooking", tags=["Create Bookings"])
def create_booking(request: CreateBookingRequest, db: Session = Depends(get_db)):
    logger.debug(f"Creating booking with request {request}.")
    return CreateBookingCommand(request, mailSender, logging.getLogger("CreateBookingCommand")).Execute()

@app.post("/UpdateBooking", tags=["Update Bookings"])
def update_booking(db: Session = Depends(get_db)):
    return {}