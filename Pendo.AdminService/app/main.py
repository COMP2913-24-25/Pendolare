from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, Response, status, Query
from configuration_provider import ConfigurationProvider
from db_provider import get_db
from sqlalchemy.orm import Session


from request_lib import *

from get_booking_fee import GetBookingFeeCommand
from get_weekly_revenue import GetWeeklyRevenueCommand
from journey_analytics import JourneyAnalyticsCommand

configuration_provider = ConfigurationProvider()

app = FastAPI(
    title="Pendo.AdminService.Api", 
    version="1.0.0",
    root_path="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Pendo Admin API"}

@app.get("/HealthCheck", tags=["HealthCheck"], status_code=status.HTTP_200_OK)
def health_check():
    return {"Status": "Ok"}

@app.patch("/UpdateBookingFee", tags=["Booking Fee"], status_code=status.HTTP_200_OK)
def update_booking_fee():
    return {"Status": "Ok"}

@app.get("/GetBookingFee", tags=["Booking Fee"], status_code=status.HTTP_200_OK)
def get_booking_fee(response : Response, db_session = Depends(get_db)):
    return GetBookingFeeCommand(configuration_provider, response, db_session).Execute()

@app.get("/GetWeeklyRevenue", tags=["Booking Revenue"], status_code=status.HTTP_200_OK)
def get_booking_revenue(filter_query : Annotated[GetWeeklyRevenueQuery, Query()], response : Response, db_session = Depends(get_db)):
    return GetWeeklyRevenueCommand(db_session, filter_query, response, configuration_provider).Execute()

@app.get("/JourneyAnalytics", tags=["Journey Analytics"], status_code=status.HTTP_200_OK)
def journey_analytics(response: Response, db_session: Session = Depends(get_db)):
    return JourneyAnalyticsCommand(db_session, response).execute()