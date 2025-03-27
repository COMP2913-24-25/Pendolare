import logging
import sys
from typing import Annotated
from fastapi import FastAPI, Depends, Response, status, Query
from configuration_provider import ConfigurationProvider
from db_provider import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from frequent_users import FrequentUsersCommand
from update_booking_fee import UpdateBookingFeeCommand
from discount_commands import CreateDiscountCommand, GetDiscountsCommand, DeleteDiscountCommand

from request_lib import *
from response_lib import *

from get_booking_fee import GetBookingFeeCommand
from get_weekly_revenue import GetWeeklyRevenueCommand
from journey_analytics import JourneyAnalyticsCommand

configuration_provider = ConfigurationProvider()

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

app = FastAPI(
    title="Pendo.AdminService.Api", 
    version="1.0.0",
    root_path="/api/Admin")

@app.get("/HealthCheck", tags=["HealthCheck"], status_code=status.HTTP_200_OK)
def health_check(db_session = Depends(get_db)):
    try:
        db_session.execute(text("SELECT 1"))
        return {"Status": "Ok"}
    except Exception as e:
        return {"Status": "Error", "Message": str(e)}

@app.patch("/UpdateBookingFee", tags=["Booking Fee"], status_code=status.HTTP_200_OK)
def update_booking_fee(request: UpdateBookingFeeRequest, response: Response, db_session: Session = Depends(get_db)):
    return UpdateBookingFeeCommand(db_session, request, response, configuration_provider, logging.getLogger("UpdateBookingFee")).Execute()

@app.get("/GetBookingFee", tags=["Booking Fee"], status_code=status.HTTP_200_OK)
def get_booking_fee(response : Response, db_session = Depends(get_db)):
    return GetBookingFeeCommand(configuration_provider, response, db_session, logging.getLogger("GetBookingFee")).Execute()

@app.get("/GetWeeklyRevenue", tags=["Booking Revenue"], status_code=status.HTTP_200_OK)
def get_booking_revenue(filter_query : Annotated[GetWeeklyRevenueQuery, Query()], response : Response, db_session = Depends(get_db)):
    return GetWeeklyRevenueCommand(db_session, filter_query, response, configuration_provider, logging.getLogger("GetWeeklyRevenue")).Execute()

@app.get("/JourneyAnalytics", tags=["Journey Analytics"], status_code=status.HTTP_200_OK)
def journey_analytics(response: Response, db_session: Session = Depends(get_db)) -> JourneyAnalyticsResponse:
    return JourneyAnalyticsCommand(db_session, response, logging.getLogger("JourneyAnalytics")).Execute()

@app.get("/FrequentUsers", tags=["User Analytics"], status_code=status.HTTP_200_OK)
def frequent_users(response: Response, db_session: Session = Depends(get_db)):
    return FrequentUsersCommand(db_session, response, logging.getLogger("FrequentUsers")).Execute()

@app.post("/CreateDiscount", tags=["Discounts"], status_code=status.HTTP_200_OK)
def create_discount(request: CreateDiscountRequest, db_session: Session = Depends(get_db)):
    return CreateDiscountCommand(db_session, request, logging.getLogger("CreateDiscount")).Execute()

@app.get("/Discounts",  tags=["Discounts"], status_code=status.HTTP_200_OK)
def get_discounts(db_session: Session = Depends(get_db)):
    return GetDiscountsCommand(db_session, logging.getLogger("GetDiscounts")).Execute()

@app.delete("/Discounts/{discount_id}", tags=["Discounts"])
def delete_discount(discount_id: str, db_session: Session = Depends(get_db)):
    return DeleteDiscountCommand(db_session, discount_id, logging.getLogger("DeleteDiscount")).Execute()