from fastapi import HTTPException
from discount_repository import DiscountRepository

class CreateDiscountCommand:
    def __init__(self, db_session, request):
        self.db_session = db_session
        self.request = request

    def Execute(self):
        try:
            repository = DiscountRepository(self.db_session)
            discount_id = repository.CreateDiscount(self.request.WeeklyJourneys, self.request.DiscountPercentage)
            return {"DiscountId": str(discount_id),
                    "Status": "Success", 
                    "Message": "Discount was created successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


class GetDiscountsCommand:
    def __init__(self, db_session):
        self.db_session = db_session

    def Execute(self):
        try:
            repository = DiscountRepository(self.db_session)
            discounts = repository.GetDiscounts()
            return [{"DiscountId": str(discount.DiscountID),
                     "WeeklyJourneys": discount.WeeklyJourneys,
                     "DiscountPercentage": discount.DiscountPercentage}
                    for discount in discounts]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


class DeleteDiscountCommand:
    def __init__(self, db_session, discount_id: str):
        self.db_session = db_session
        self.discount_id = discount_id

    def Execute(self):
        try:
            repository = DiscountRepository(self.db_session)
            deleted = repository.DeleteDiscount(self.discount_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Discount is not found")
            return {"Status": "Success", "Message": "Discount was deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
