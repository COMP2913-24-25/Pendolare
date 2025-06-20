from models import Discounts
from sqlalchemy import delete
import uuid

class DiscountRepository:
    """
    A class used to house all the methods that interact with the Discount table in the database.
    """

    def __init__(self, db_session):
        """
        Constructor for DiscountRepository class.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def CreateDiscount(self, weekly_journeys: int, discount_percentage: float):
        discount_percentage_decimal = discount_percentage / 100.0 # convert percentage to decimal
        try:
            discount = Discounts(WeeklyJourneys=weekly_journeys, DiscountPercentage=discount_percentage_decimal)
            self.db_session.add(discount)
            self.db_session.commit()
            return str(discount.DiscountID)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            self.logger.error("Error creating discount: %s", e)
            raise e

    
    def GetDiscounts(self):
        """
        Retrieves all discounts.

        Returns:
            list[Discounts]: A list of all Discount objects.
        """
        return self.db_session.query(Discounts).all()
    
    def DeleteDiscount(self, discount_id: str):
        """
        Deletes a discount by its ID.

        Args:
            discount_id (UUID): The ID of the discount to delete.

        Returns:
            bool: True if the discount was deleted, False otherwise.
        """
        
        try:
            discount_uuid = uuid.UUID(discount_id)
            discount = self.db_session.query(Discounts).filter(Discounts.DiscountID == discount_uuid).first()

            if discount:
                self.db_session.delete(discount)
                self.db_session.commit()
                return True
            else:
                return False
        except ValueError:
            return False # if the uuid is invalid
        except Exception:
            self.db_session.rollback()
            return False
