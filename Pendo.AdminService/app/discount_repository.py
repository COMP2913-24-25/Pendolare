from models import Discounts
from sqlalchemy import delete

class DiscountRepository:
    """
    A class used to house all the methods that interact with the Discount table in the database.
    """

    def __init__(self, db_session):
        """
        Constructor for DiscountRepository class.
        """
        self.db_session = db_session

    def CreateDiscount(self, weekly_journeys: int, discount_percentage: float):
        discount = Discounts(WeeklyJourneys=weekly_journeys, DiscountPercentage=discount_percentage)
        self.db_session.add(discount)
        self.db_session.commit()
        return discount.DiscountID
    
    def GetDiscounts(self):
        return self.db_session.query(Discounts).all()
    
    def DeleteDiscount(self, discount_id: str):
        deleting_d = delete(Discounts).where(Discounts.DiscountID == discount_id)
        to_execute = self.db_session.execute(deleting_d)
        rows_deleted = to_execute.rowcount
        self.db_session.commit()
        return rows_deleted > 0
