# import pytest
# from unittest.mock import Mock, MagicMock
# from src.endpoints.ViewBalanceCmd import ViewBalanceCommand
# from src.booking_repository import Booking
# import uuid

# @pytest.fixture
# def mock_request():
#     request = MagicMock(UserId = uuid.uuid4())
#     return request

# @pytest.fixture
# def mock_logger():
#     return Mock()

# @pytest.fixture
# def mock_payment_repository():
#     return Mock()

# @pytest.fixture
# def view_balance_command(mock_request, mock_logger, mock_payment_repository):
#     command = ViewBalanceCommand(mock_request, mock_logger)
#     command.payment_repository = mock_payment_repository
#     return command

# def test_get_bookings_success(get_bookings_command, mock_payment_repository, mock_request):
#     mock_payment_repository.GetBalanceSheet.return_value = []
#     bookings = get_bookings_command.Execute()
#     assert len(bookings) == 2
#     get_bookings_command.logger.debug.assert_called_with(f"Retrieved [2] Bookings for user {mock_request.UserId} successfully.")

# def test_get_bookings_no_bookings(get_bookings_command, mock_payment_repository, mock_request):
#     mock_payment_repository.GetBookingsForUser.return_value = []
#     bookings = get_bookings_command.Execute()
#     assert bookings == []
#     get_bookings_command.logger.debug.assert_called_with(f"Retrieved [0] Bookings for user {mock_request.UserId} successfully.")

# def test_get_bookings_none(get_bookings_command, mock_payment_repository, mock_request):
#     mock_payment_repository.GetBookingsForUser.return_value = None
#     bookings = get_bookings_command.Execute()
#     assert bookings == []
#     get_bookings_command.logger.debug.assert_called_with(f"Retrieved [0] Bookings for user {mock_request.UserId} successfully.")