# 
# RefundPayment Implementation
# Author: Catherine Weightman
#

from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction, UserBalance
from ..returns.PaymentReturns import StatusResponse
from datetime import datetime, timedelta
import logging
from decimal import Decimal

class RefundPaymentCommand:
    def __init__(self, logger, BookingId, CancelledById, LatestPrice, CancellationTime, JourneyTime):
        """
        Constructor for RefundPaymentCommand class.
        
        :param logger: Logger instance for tracking events and errors
        :param BookingId: Unique identifier for the booking
        :param CancelledById: ID of the user cancelling the booking
        :param LatestPrice: Price of the booking
        :param CancellationTime: Time of cancellation
        :param JourneyTime: Scheduled journey time
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger

        self.BookingId = BookingId
        self.CancelledById = CancelledById
        self.LatestPrice = LatestPrice
        self.CancellationTime = CancellationTime
        self.JourneyTime = JourneyTime

    def _safe_bool_conversion(self, value):
        """
        Safely convert various input types to a boolean value with comprehensive logging.
        
        :param value: Input value to convert to boolean
        :return: Boolean representation of the input
        """
        try:

            self.logger.info(f"Converting value to boolean: {value} (Type: {type(value)})")

            if value is None:
                self.logger.info("Value is None, returning False")
                return False
            
            if isinstance(value, bool):
                self.logger.info(f"Value is already a boolean: {value}")
                return value
            
            if isinstance(value, str):
                lower_value = value.lower().strip()
                bool_result = lower_value in ['1', 'true', 'yes', 'y']
                self.logger.info(f"String conversion: '{value}' -> {bool_result}")
                return bool_result
            
            if isinstance(value, (int, float)):
                bool_result = bool(value)
                self.logger.info(f"Numeric conversion: {value} -> {bool_result}")
                return bool_result
            
            try:
                bool_result = bool(value)
                self.logger.info(f"Generic conversion: {value} -> {bool_result}")
                return bool_result
            except Exception as conv_error:
                self.logger.error(f"Failed to convert value to boolean. Error: {conv_error}")
                return False

        except Exception as e:
            self.logger.error(f"Unexpected error in _safe_bool_conversion: {e}")
            return False

    def Execute(self):
        """
        Execute method creates a transaction record after refunding items.
        :return: status of operation
        """
        try:
            self.logger.info(f"Starting Refund Process for BookingId: {self.BookingId}")
            self.logger.info(f"Cancelled By: {self.CancelledById}")
            self.logger.info(f"Latest Price: {self.LatestPrice}")
            self.logger.info(f"Cancellation Time: {self.CancellationTime}")
            self.logger.info(f"Journey Time: {self.JourneyTime}")

            DecimalLatestPrice = Decimal(str(self.LatestPrice))

            if not self.BookingId or not self.CancelledById:
                self.logger.error("BookingId or CancelledById is missing")
                raise ValueError("BookingId and CancelledById must be provided")

            booking = self.PaymentRepository.GetBookingById(self.BookingId)
            if booking is None:
                error_msg = f"Booking not found for BookingId: {self.BookingId}"
                self.logger.error(error_msg)
                return StatusResponse(Status="fail", Error=error_msg)

            self.logger.info(f"Booking found: {booking}")
            
            UserType = self.PaymentRepository.GetUserType(self.CancelledById, self.BookingId)
            self.logger.info(f"User Type: {UserType}")
            
            if not UserType:
                self.logger.error(f"Could not determine user type for CancelledById: {self.CancelledById}")
                raise ValueError(f"Could not determine user type for CancelledById: {self.CancelledById}")
            
            driver_approval = self._safe_bool_conversion(getattr(booking, 'DriverApproval', False))
            self.logger.info(f"Driver Approval Status: {driver_approval}")
            
            if not driver_approval:
                self.logger.warning("Booking does not have driver approval")
                raise ValueError("Booking does not have driver approval")
            
            try:
                DriverId = booking.Journey_.UserId
                PassengerId = booking.UserId
                self.logger.info(f"Driver ID: {DriverId}, Passenger ID: {PassengerId}")
            except AttributeError as ae:
                self.logger.error(f"Failed to extract user IDs: {ae}")
                raise ValueError("Cannot extract driver or passenger ID")

            AdminFee = booking.FeeMargin
            self.logger.info(f"Admin Fee: {AdminFee}")

            self.PaymentRepository.UpdatePendingBalance(DriverId, -1 * DecimalLatestPrice)
            self.logger.info(f"Updated pending balance for driver {DriverId}")

            driver_transaction = Transaction(
                UserId=DriverId, 
                Value=float(DecimalLatestPrice),
                CurrencyCode="gbp",
                TransactionStatusId=1,
                TransactionTypeId=1,
                CreateDate=datetime.now(),
                UpdateDate=datetime.now()
            )
            self.PaymentRepository.CreateTransaction(driver_transaction)
            self.logger.info(f"Created driver transaction: {driver_transaction}")

            if UserType == "Passenger":
                TimeDifference = self.JourneyTime - self.CancellationTime
                self.logger.info(f"Time Difference: {TimeDifference}")

                if TimeDifference <= timedelta(minutes=15):
                    RefundableAmount = DecimalLatestPrice * Decimal('0.75')
                    
                    self.PaymentRepository.UpdateNonPendingBalance(PassengerId, -1 * RefundableAmount)
                    self.logger.info(f"Updated non-pending balance for passenger {PassengerId}")

                    passenger_transaction = Transaction(
                        UserId=PassengerId, 
                        Value=float(RefundableAmount),
                        CurrencyCode="gbp",
                        TransactionStatusId=1,
                        TransactionTypeId=3,
                        CreateDate=datetime.now(),
                        UpdateDate=datetime.now()
                    )
                    self.PaymentRepository.CreateTransaction(passenger_transaction)
                    self.logger.info(f"Created passenger transaction: {passenger_transaction}")

                    NewPrice = DecimalLatestPrice * Decimal('0.75')
                    Margin = round(AdminFee * NewPrice, 2)
                    Price = NewPrice - Margin
                    self.logger.info(f"New Price: {NewPrice}, Margin: {Margin}, Final Price: {Price}")

                    self.PaymentRepository.UpdateNonPendingBalance(DriverId, Price)
                    self.logger.info(f"Updated non-pending balance for driver {DriverId}")

                    driver_final_transaction = Transaction(
                        UserId=DriverId, 
                        Value=float(Price),
                        CurrencyCode="gbp",
                        TransactionStatusId=1,
                        TransactionTypeId=2,
                        CreateDate=datetime.now(),
                        UpdateDate=datetime.now()
                    )
                    self.PaymentRepository.CreateTransaction(driver_final_transaction)
                    self.logger.info(f"Created final driver transaction: {driver_final_transaction}")

            self.PaymentRepository.UpdateBookingStatus(self.BookingId, 2)
            
            self.logger.info("Refund process completed successfully")
            return StatusResponse(Status="success")

        except Exception as e:
            if "Booking not found" not in str(e):
                self.logger.error(f"Error in Refund Booking. Error: {str(e)}", exc_info=True)
            return StatusResponse(Status="fail", Error=str(e))