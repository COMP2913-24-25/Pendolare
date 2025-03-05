from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, Response, status, Query
from configuration_provider import ConfigurationProvider
from db_provider import get_db

from request_lib import *

from get_booking_fee import GetBookingFeeCommand
from get_weekly_revenue import GetWeeklyRevenueCommand

configuration_provider = ConfigurationProvider()

app = FastAPI(
    title="Pendo.AdminService.Api", 
    version="1.0.0",
    root_path="/api")

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