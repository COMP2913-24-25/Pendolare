from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, Response, status, Query
from configuration_provider import ConfigurationProvider
from db_provider import get_db
from sqlalchemy.orm import Session
from frequent_users import FrequentUsersCommand
from update_booking_fee import UpdateBookingFeeCommand


from request_lib import *

from get_booking_fee import GetBookingFeeCommand
from get_weekly_revenue import GetWeeklyRevenueCommand
from journey_analytics import JourneyAnalyticsCommand
from discount_repository import DiscountRepository
from models import Discounts

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
def update_booking_fee(request: UpdateBookingFeeRequest, response: Response, db_session: Session = Depends(get_db)):
    return UpdateBookingFeeCommand(db_session, request, response, configuration_provider).Execute()

@app.get("/GetBookingFee", tags=["Booking Fee"], status_code=status.HTTP_200_OK)
def get_booking_fee(response : Response, db_session = Depends(get_db)):
    return GetBookingFeeCommand(configuration_provider, response, db_session).Execute()

@app.get("/GetWeeklyRevenue", tags=["Booking Revenue"], status_code=status.HTTP_200_OK)
def get_booking_revenue(filter_query : Annotated[GetWeeklyRevenueQuery, Query()], response : Response, db_session = Depends(get_db)):
    return GetWeeklyRevenueCommand(db_session, filter_query, response, configuration_provider).Execute()

@app.get("/JourneyAnalytics", tags=["Journey Analytics"], status_code=status.HTTP_200_OK)
def journey_analytics(response: Response, db_session: Session = Depends(get_db)):
    return JourneyAnalyticsCommand(db_session, response).execute()

@app.get("/FrequentUsers", tags=["User Analytics"], status_code=status.HTTP_200_OK)
def frequent_users(response: Response, db_session: Session = Depends(get_db)):
    return FrequentUsersCommand(db_session, response).execute()

@app.post("/CreateDiscount", tags=["Discounts"], status_code=status.HTTP_200_OK)
def create_discount(request: CreateDiscountRequest, db_session: Session = Depends(get_db)):
    try:
        repository = DiscountRepository(db_session)
        discount_id = repository.CreateDiscount(request.WeeklyJourneys, request.DiscountPercentage)
        return {"DiscountId": str(discount_id),
                "Status": "Success", 
                "Message": "Discount was created successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/Discounts",  tags=["Discounts"], status_code=status.HTTP_200_OK)
def get_discounts(db_session: Session = Depends(get_db)):
    try:
        repository = DiscountRepository(db_session)
        discounts = repository.GetDiscounts()
        return [{"DiscountId": str(discount.DiscountID),
                 "WeeklyJourneys": discount.WeeklyJourneys,
                 "DiscountPercentage": discount.DiscountPercentage
            }
            for discount in discounts
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/Discounts/{discount_id}", tags=["Discounts"])
def delete_discount(discount_id: str, db_session: Session = Depends(get_db)):
    try:
        repository = DiscountRepository(db_session)
        deleted = repository.DeleteDiscount(discount_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Discount is not found")

        return {
            "Status": "Success",
            "Message": "Discount was deleted successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


