from models import Discounts
from sqlalchemy import delete

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
        """
        Creates a new discount.

        Args:
            weekly_journeys (int): The number of weekly journeys required for the discount.
            discount_percentage (float): The discount percentage.

        Returns:
            UUID: The ID of the created discount.
        """

        discount = Discounts(WeeklyJourneys=weekly_journeys, DiscountPercentage=discount_percentage)
        self.db_session.add(discount)
        self.db_session.commit()
        return discount.DiscountID
    
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
        
        deleting_d = delete(Discounts).where(Discounts.DiscountID == discount_id)
        to_execute = self.db_session.execute(deleting_d)
        rows_deleted = to_execute.rowcount
        self.db_session.commit()
        return rows_deleted > 0
