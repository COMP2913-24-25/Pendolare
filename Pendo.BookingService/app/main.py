import logging

from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends, Response, status
from .db_provider import get_db, Session, text, configProvider, environment

from .create_booking import CreateBookingCommand
from .get_bookings import GetBookingsCommand
from .add_booking_ammendment import AddBookingAmmendmentCommand
from .approve_booking_ammendment import ApproveBookingAmmendmentCommand
from .approve_booking import ApproveBookingCommand
from .confirm_at_pickup import ConfirmAtPickupCommand
from .booking_complete import BookingCompleteCommand

from .requests import *
from .responses import *
from .email_sender import MailSender
import sys
from .dvla_api import VehicleEnquiryClient
from .payment_service_api import PaymentServiceClient

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
    root_path="/api/Booking")

logger.info("Initialising Mail Sender Service...")
mailSender = MailSender(configProvider.LoadEmailConfiguration(next(get_db())))
logger.info("Mail Sender Service Initialised")

dvla_client = VehicleEnquiryClient(configProvider.GetSingleValue(next(get_db()), "Booking.DvlaApiKey"), logger)

payment_service_client = PaymentServiceClient(configProvider.paymentServiceConfiguration, logger)

@app.get("/HealthCheck", tags=["HealthCheck"], status_code=status.HTTP_200_OK)
def test_db(db: Session = Depends(get_db)):
    logger.info("Testing DB connection...")
    try:
        db.execute(text("SELECT 1"))
        logger.info("DB connection successful")
        return {"DbConnection": "Successful"}
    except Exception as e:
        logger.error(f"DB connection failed. Error: {str(e)}")
        raise HTTPException(500, detail="DB connection failed.")

@app.post("/GetBookings", tags=["Get Bookings"], status_code=status.HTTP_200_OK)
def get_bookings(request: GetBookingsRequest, db: Session = Depends(get_db)):
    logger.debug("Getting bookings...")
    return GetBookingsCommand(request, logging.getLogger("GetBookingsCommand")).Execute()

@app.post("/CreateBooking", tags=["Create Bookings"], status_code=status.HTTP_200_OK)
def create_booking(request: CreateBookingRequest, response : Response, db: Session = Depends(get_db)) -> StatusResponse:
    logger.debug(f"Creating booking with request {request}.")
    return CreateBookingCommand(request, 
                                response, 
                                mailSender, 
                                logging.getLogger("CreateBookingCommand"), 
                                dvla_client, 
                                configProvider,
                                payment_service_client).Execute()

@app.post("/AddBookingAmmendment", tags=["Add Booking Ammendment"], status_code=status.HTTP_200_OK)
def add_booking_ammendment(request : AddBookingAmmendmentRequest, response : Response, db: Session = Depends(get_db)):
    return AddBookingAmmendmentCommand(request, 
                                       response, 
                                       logging.getLogger("AddBookingAmmendmentCommand")).Execute()

@app.put("/ApproveBookingAmmendment/{BookingAmmendmentId}", tags=["Approve Booking Ammendment"], status_code=status.HTTP_200_OK)
def approve_booking_ammendment(BookingAmmendmentId: UUID, request: ApproveBookingAmmendmentRequest, response : Response, db: Session = Depends(get_db)):
    return ApproveBookingAmmendmentCommand(BookingAmmendmentId, 
                                           request, 
                                           response, 
                                           logging.getLogger("ApproveBookingAmmendmentCommand"), 
                                           mailSender, 
                                           dvla_client,
                                           payment_service_client).Execute()

@app.put("/ApproveBooking/{BookingId}", tags=["Approve Booking Request"], status_code=status.HTTP_200_OK)
def approve_booking_request(BookingId: UUID, request: ApproveBookingRequest, response : Response, db: Session = Depends(get_db)):
    return ApproveBookingCommand(BookingId, 
                                 request, 
                                 response, 
                                 logging.getLogger("ApproveBookingCommand"), 
                                 mailSender, 
                                 dvla_client).Execute()

@app.put("/ConfirmAtPickup/{BookingId}", tags=["Confirm At Pickup"], status_code=status.HTTP_200_OK)
def confirm_at_pickup(BookingId: UUID, request : ConfirmAtPickupRequest, response : Response, db: Session = Depends(get_db)) -> StatusResponse:
    return ConfirmAtPickupCommand(BookingId, 
                                  request, 
                                  response, 
                                  configProvider, 
                                  mailSender, 
                                  logging.getLogger("ConfirmAtPickupCommand"), 
                                  dvla_client).Execute()

@app.put("/CompleteBooking/{BookingId}", tags=["Complete Booking"], status_code=status.HTTP_200_OK)
def complete_booking(BookingId: UUID, request : CompleteBookingRequest, response : Response, db: Session = Depends(get_db)) -> StatusResponse:
    return BookingCompleteCommand(BookingId, 
                                  request, 
                                  response, 
                                  logging.getLogger("BookingCompleteCommand"), 
                                  payment_service_client).Execute()