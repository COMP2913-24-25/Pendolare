import logging

from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends
from .db_provider import get_db, Session, text, configProvider, environment
from .create_booking import CreateBookingCommand
from .get_bookings import GetBookingsCommand
from .requests import *
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

@app.get("/GetBookings/{UserId}", tags=["Get Bookings"])
def get_bookings(UserId: UUID, db: Session = Depends(get_db)):
    logger.debug("Getting bookings...")
    return GetBookingsCommand(UserId, logging.getLogger("GetBookingsCommand")).Execute()

@app.post("/CreateBooking", tags=["Create Bookings"])
def create_booking(request: CreateBookingRequest, db: Session = Depends(get_db)):
    logger.debug(f"Creating booking with request {request}.")
    return CreateBookingCommand(request, mailSender, logging.getLogger("CreateBookingCommand")).Execute()

@app.put("/UpdateBookingStatus/{BookingId}", tags=["Update Booking"])
def update_booking_status(BookingId: UUID, request : UpdateBookingStatusRequest, db: Session = Depends(get_db)):
    return {}

@app.post("/AddBookingAmmendment", tags=["Add Booking Ammendment"])
def add_booking_ammendment(request : AddBookingAmmendmentRequest, db: Session = Depends(get_db)):
    return {}

@app.put("/ApproveBooking/{BookingAmmendmentId}", tags=["Approve Booking Ammendment"])
def approve_booking_ammendment(BookingAmmendmentId: UUID, request: ApproveBookingAmmendmentRequest, db: Session = Depends(get_db)):
    return {}

@app.post("/ApproveBooking", tags=["Approve Booking Request"])
def approve_booking_request(request: ApproveBookingRequest, db: Session = Depends(get_db)):
    return {}