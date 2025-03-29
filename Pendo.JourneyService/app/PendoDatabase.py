from typing import List, Optional

from sqlalchemy import Boolean, CHAR, Column, DECIMAL, Float, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, Unicode, Uuid, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class BookingStatus(Base):
    __tablename__ = 'BookingStatus'
    __table_args__ = (
        PrimaryKeyConstraint('BookingStatusId', name='PK__BookingS__54F9C05D74A30BE8'),
        {'schema': 'booking'}
    )

    BookingStatusId = mapped_column(Integer, Identity(start=1, increment=1))
    Status = mapped_column(Unicode(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    Description = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))

    Booking: Mapped[List['Booking']] = relationship('Booking', uselist=True, back_populates='BookingStatus_')


class UserType(Base):
    __tablename__ = 'UserType'
    __table_args__ = (
        PrimaryKeyConstraint('UserTypeId', name='PK__UserType__40D2D81658BF604D'),
        {'schema': 'identity'}
    )

    UserTypeId = mapped_column(Integer, Identity(start=1, increment=1))
    Type = mapped_column(Unicode(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False)
    Description = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))

    User: Mapped[List['User']] = relationship('User', uselist=True, back_populates='UserType_')


class Discounts(Base):
    __tablename__ = 'Discounts'
    __table_args__ = (
        PrimaryKeyConstraint('DiscountID', name='PK__Discount__E43F6DF627B08CEC'),
        {'schema': 'payment'}
    )

    DiscountID = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    WeeklyJourneys = mapped_column(Integer, nullable=False)
    DiscountPercentage = mapped_column(Float(53), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))

    Journey: Mapped[List['Journey']] = relationship('Journey', uselist=True, back_populates='Discounts_')


class Configuration(Base):
    __tablename__ = 'Configuration'
    __table_args__ = (
        PrimaryKeyConstraint('ConfigurationId', name='PK__Configur__95AA53BB1403DF28'),
        Index('UQ__Configur__C41E02896558D695', 'Key', unique=True),
        {'schema': 'shared'}
    )

    ConfigurationId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    Key = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Value = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))


class User(Base):
    __tablename__ = 'User'
    __table_args__ = (
        ForeignKeyConstraint(['UserTypeId'], ['identity.UserType.UserTypeId'], name='FK_User_UserType'),
        PrimaryKeyConstraint('UserId', name='PK__tmp_ms_x__1788CC4CBF03BA51'),
        Index('IX_User_UserType', 'UserTypeId'),
        Index('UQ__tmp_ms_x__A9D10534F96C98F2', 'Email', unique=True),
        {'schema': 'identity'}
    )

    UserId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    Email = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UserRating = mapped_column(Float(53), nullable=False, server_default=text('((-1))'))
    UserTypeId = mapped_column(Integer, nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    FirstName = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    LastName = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))

    UserType_: Mapped['UserType'] = relationship('UserType', back_populates='User')
    OtpLogin: Mapped[List['OtpLogin']] = relationship('OtpLogin', uselist=True, back_populates='User_')
    Journey: Mapped[List['Journey']] = relationship('Journey', uselist=True, back_populates='User_')
    Booking: Mapped[List['Booking']] = relationship('Booking', uselist=True, back_populates='User_')


class OtpLogin(Base):
    __tablename__ = 'OtpLogin'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_OtpLogin_User'),
        PrimaryKeyConstraint('OtpLoginId', name='PK__OtpLogin__C597BB318BCC0BDE'),
        Index('IX_OtpLogin_UserId', 'UserId'),
        {'schema': 'identity'}
    )

    OtpLoginId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    UserId = mapped_column(Uuid, nullable=False)
    CodeHash = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    HashSalt = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ExpiryDate = mapped_column(DATETIME2, nullable=False)
    Verified = mapped_column(Boolean, nullable=False, server_default=text('((0))'))
    IssueDate = mapped_column(DATETIME2)

    User_: Mapped['User'] = relationship('User', back_populates='OtpLogin')


class Journey(Base):
    __tablename__ = 'Journey'
    __table_args__ = (
        ForeignKeyConstraint(['DiscountID'], ['payment.Discounts.DiscountID'], name='FK_Journeys_DiscountID'),
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Journeys_UserId'),
        PrimaryKeyConstraint('JourneyId', name='PK__tmp_ms_x__4159B9EFEEC326ED'),
        {'schema': 'journey'}
    )

    JourneyId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    UserId = mapped_column(Uuid, nullable=False)
    AdvertisedPrice = mapped_column(DECIMAL(18, 8), nullable=False)
    CurrencyCode = mapped_column(CHAR(3, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, server_default=text("('GBP')"))
    StartName = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    StartLong = mapped_column(Float(53), nullable=False)
    StartLat = mapped_column(Float(53), nullable=False)
    EndName = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    EndLong = mapped_column(Float(53), nullable=False)
    EndLat = mapped_column(Float(53), nullable=False)
    JourneyType = mapped_column(Integer, nullable=False, server_default=text('((1))'))
    StartDate = mapped_column(DATETIME2, nullable=False)
    RepeatUntil = mapped_column(DATETIME2, nullable=False)
    StartTime = mapped_column(DATETIME2, nullable=False)
    JourneyStatusId = mapped_column(Integer, nullable=False, server_default=text('((1))'))
    MaxPassengers = mapped_column(Integer, nullable=False)
    RegPlate = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    Recurrance = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    BootWidth = mapped_column(Float(53))
    BootHeight = mapped_column(Float(53))
    DiscountID = mapped_column(Uuid)
    LockedUntil = mapped_column(DATETIME2)

    Discounts_: Mapped[Optional['Discounts']] = relationship('Discounts', back_populates='Journey')
    User_: Mapped['User'] = relationship('User', back_populates='Journey')
    Booking: Mapped[List['Booking']] = relationship('Booking', uselist=True, back_populates='Journey_')


class Booking(Base):
    __tablename__ = 'Booking'
    __table_args__ = (
        ForeignKeyConstraint(['BookingStatusId'], ['booking.BookingStatus.BookingStatusId'], name='FK_Booking_BookingStatus'),
        ForeignKeyConstraint(['JourneyId'], ['journey.Journey.JourneyId'], name='FK_Booking_Journey'),
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Booking_User'),
        PrimaryKeyConstraint('BookingId', name='PK__Booking__73951AED844907A0'),
        {'schema': 'booking'}
    )

    BookingId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    UserId = mapped_column(Uuid, nullable=False)
    JourneyId = mapped_column(Uuid, nullable=False)
    BookingStatusId = mapped_column(Integer, nullable=False)
    FeeMargin = mapped_column(DECIMAL(18, 8), nullable=False)
    RideTime = mapped_column(DATETIME2, nullable=False)
    DriverApproval = mapped_column(Boolean, nullable=False, server_default=text('((0))'))
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    BookedWindowEnd = mapped_column(DATETIME2)

    BookingStatus_: Mapped['BookingStatus'] = relationship('BookingStatus', back_populates='Booking')
    Journey_: Mapped['Journey'] = relationship('Journey', back_populates='Booking')
    User_: Mapped['User'] = relationship('User', back_populates='Booking')
    BookingAmmendment: Mapped[List['BookingAmmendment']] = relationship('BookingAmmendment', uselist=True, back_populates='Booking_')


class BookingAmmendment(Base):
    __tablename__ = 'BookingAmmendment'
    __table_args__ = (
        ForeignKeyConstraint(['BookingId'], ['booking.Booking.BookingId'], name='FK_BookingAmmendment_Booking'),
        PrimaryKeyConstraint('BookingAmmendmentId', name='PK__tmp_ms_x__59DE3C6A423B292A'),
        {'schema': 'booking'}
    )

    BookingAmmendmentId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    BookingId = mapped_column(Uuid, nullable=False)
    CancellationRequest = mapped_column(Boolean, nullable=False, server_default=text('((0))'))
    DriverApproval = mapped_column(Boolean, nullable=False, server_default=text('((0))'))
    PassengerApproval = mapped_column(Boolean, nullable=False, server_default=text('((0))'))
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    ProposedPrice = mapped_column(DECIMAL(18, 8))
    StartName = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    StartLong = mapped_column(Float(53))
    StartLat = mapped_column(Float(53))
    EndName = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    EndLong = mapped_column(Float(53))
    EndLat = mapped_column(Float(53))
    StartTime = mapped_column(DATETIME2)
    Recurrance = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))

    Booking_: Mapped['Booking'] = relationship('Booking', back_populates='BookingAmmendment')
