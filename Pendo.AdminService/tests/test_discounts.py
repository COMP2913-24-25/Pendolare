import pytest
from unittest.mock import MagicMock
from app.discount_repository import DiscountRepository
from app.models import Discounts
from uuid import UUID
from app.conftest import *

def test_create_discount(db_session_mock):
    db_session_mock.add = MagicMock()
    db_session_mock.commit = MagicMock()
    repository = DiscountRepository(db_session_mock)

    discount_id = repository.CreateDiscount(weekly_journeys=5, discount_percentage=0.10)

    db_session_mock.add.assert_called_once()
    db_session_mock.commit.assert_called_once()

def test_get_discounts(db_session_mock):
    
    discount1_mock = MagicMock(Discounts, DiscountID=UUID('123e4567-e89b-12d3-a456-426614174000'), WeeklyJourneys=5, DiscountPercentage=10)
    discount2_mock = MagicMock(Discounts, DiscountID=UUID('123e4567-e89b-12d3-a456-426614174001'), WeeklyJourneys=10, DiscountPercentage=20)
    db_session_mock.query().all.return_value = [discount1_mock, discount2_mock]
    repository = DiscountRepository(db_session_mock)

    discounts = repository.GetDiscounts()

    assert len(discounts) == 2
    assert discounts[0].DiscountID == UUID('123e4567-e89b-12d3-a456-426614174000')
    assert discounts[1].DiscountID == UUID('123e4567-e89b-12d3-a456-426614174001')

def test_delete_discount(db_session_mock):
    # Configure query to return a discount object
    discount_obj = MagicMock()
    db_session_mock.query.return_value.filter.return_value.first.return_value = discount_obj
    db_session_mock.delete = MagicMock()
    db_session_mock.commit = MagicMock()

    repository = DiscountRepository(db_session_mock)
    discount_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    deleted = repository.DeleteDiscount(discount_id)

    assert deleted is True
    db_session_mock.delete.assert_called_once_with(discount_obj)
    db_session_mock.commit.assert_called_once()

def test_delete_discount_not_found(db_session_mock):
    # Configure query to return None (discount not found)
    db_session_mock.query.return_value.filter.return_value.first.return_value = None
    db_session_mock.delete = MagicMock()
    db_session_mock.commit = MagicMock()

    repository = DiscountRepository(db_session_mock)
    discount_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    deleted = repository.DeleteDiscount(discount_id)

    assert deleted is False
    # Ensure delete and commit are not called when discount is not found
    db_session_mock.delete.assert_not_called()
    db_session_mock.commit.assert_not_called()

def test_create_discount_exception(db_session_mock):
 
    db_session_mock.add = MagicMock()
    db_session_mock.commit = MagicMock(side_effect=Exception("Database error"))
    repository = DiscountRepository(db_session_mock)

    with pytest.raises(Exception) as exc_info:
        repository.CreateDiscount(weekly_journeys=5, discount_percentage=0.10)

    assert "name 'SQLAlchemyError'" in str(exc_info.value)

def test_delete_discount_exception(db_session_mock):
    # Simulate exception during query
    db_session_mock.query.side_effect = Exception("Database error")
    db_session_mock.rollback = MagicMock()
    repository = DiscountRepository(db_session_mock)
    discount_id = UUID('123e4567-e89b-12d3-a456-426614174000')

    result = repository.DeleteDiscount(discount_id)
    assert result is False
    db_session_mock.rollback.assert_called_once()