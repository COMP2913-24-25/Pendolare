from fastapi import HTTPException, status
from discount_repository import DiscountRepository

class CreateDiscountCommand:

    def __init__(self, db_session, request, logger):
        self.db_session = db_session
        self.request = request
        self.logger = logger

    def Execute(self):
        try:
            self.logger.info("Creating discount...")

            repository = DiscountRepository(self.db_session)
            discount_id = repository.CreateDiscount(self.request.WeeklyJourneys, self.request.DiscountPercentage)

            self.logger.info(f"Discount was created successfully with id: {discount_id}")

            return {
                "DiscountId": str(discount_id),
                "Status": "Success", 
                "Message": "Discount was created successfully"
                }
        
        except Exception as e:
            self.logger.error(f"Failed to create discount: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


class GetDiscountsCommand:
    def __init__(self, db_session, logger):
        self.db_session = db_session
        self.logger = logger

    def Execute(self):
        try:
            self.logger.info("Getting discounts...")

            repository = DiscountRepository(self.db_session)
            discounts = repository.GetDiscounts()

            self.logger.info(f"Found {len(discounts)} discounts")

            return [{"DiscountId": str(discount.DiscountID),
                     "WeeklyJourneys": discount.WeeklyJourneys,
                     "DiscountPercentage": discount.DiscountPercentage}
                    for discount in discounts]
        except Exception as e:
            self.logger.error(f"Failed to get discounts: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


class DeleteDiscountCommand:
    def __init__(self, db_session, discount_id: str, logger):
        self.db_session = db_session
        self.discount_id = discount_id
        self.logger = logger

    def Execute(self):
        try:
            self.logger.info(f"Deleting discount with id: {self.discount_id}")

            repository = DiscountRepository(self.db_session)
            deleted = repository.DeleteDiscount(self.discount_id)
            if not deleted:
                self.logger.error(f"Discount with id: {self.discount_id} was not found")
                return HTTPException(status_code=404, detail="Discount is not found")
            
            self.logger.info(f"Discount with id: {self.discount_id} was deleted successfully")
            return {"Status": "Success", "Message": "Discount was deleted successfully"}
        
        except Exception as e:
            self.logger.error(f"Failed to delete discount: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
