import logging

from fastapi import FastAPI, HTTPException, Depends
from .db_provider import get_db, Session, text, configProvider, environment
from .create_booking import CreateBookingCommand
from .requests import CreateBookingRequest
from .email_sender import MailSender

logging.basicConfig(
    level=logging.INFO if environment == "Production" else logging.DEBUG,
    filename='Pendo.BookingService.log',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
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
        return {"db_connection": "failed", "error": str(e)}

@app.post("/GetBookings", tags=["Get Bookings"])
def get_bookings(db: Session = Depends(get_db)):
    logger.debug("Getting bookings...")
    return {}

@app.post("/CreateBooking", tags=["Create Bookings"])
def create_booking(request: CreateBookingRequest, db: Session = Depends(get_db)):
    logger.debug(f"Creating booking with request {request}.")
    return CreateBookingCommand(request, mailSender, logging.getLogger("CreateBookingCommand")).Execute()

@app.post("/UpdateBooking", tags=["Update Bookings"])
def update_booking(db: Session = Depends(get_db)):
    return {}