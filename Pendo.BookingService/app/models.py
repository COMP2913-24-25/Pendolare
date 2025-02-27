from typing import List

from sqlalchemy import Boolean, CHAR, Column, DECIMAL, Float, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, Unicode, Uuid, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class BookingStatus(Base):
    __tablename__ = 'BookingStatus'
    __table_args__ = (
        PrimaryKeyConstraint('BookingStatusId', name='PK__BookingS__54F9C05D08F365B1'),
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
        PrimaryKeyConstraint('UserTypeId', name='PK__UserType__40D2D816516A6BAF'),
        {'schema': 'identity'}
    )

    UserTypeId = mapped_column(Integer, Identity(start=1, increment=1))
    Type = mapped_column(Unicode(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False)
    Description = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))

    User: Mapped[List['User']] = relationship('User', uselist=True, back_populates='UserType_')


class ApiClient(Base):
    __tablename__ = 'ApiClient'
    __table_args__ = (
        PrimaryKeyConstraint('ApiClientId', name='PK__ApiClien__FDC5B7C888A9CD96'),
        Index('UQ__ApiClien__E67E1A259C16CB29', 'ClientId', unique=True),
        {'schema': 'shared'}
    )

    ApiClientId = mapped_column(Integer, Identity(start=1, increment=1))
    ApiName = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ClientId = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ClientSecret = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IsActive = mapped_column(Boolean, nullable=False, server_default=text('((1))'))
    CreateDate = mapped_column(DATETIME2, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, server_default=text('(getutcdate())'))


class Configuration(Base):
    __tablename__ = 'Configuration'
    __table_args__ = (
        PrimaryKeyConstraint('ConfigurationId', name='PK__Configur__95AA53BB316B46EA'),
        Index('UQ__Configur__C41E02892DD76308', 'Key', unique=True),
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
        PrimaryKeyConstraint('UserId', name='PK__User__1788CC4C56FE41B7'),
        Index('IX_User_UserType', 'UserTypeId'),
        Index('UQ__User__A9D1053444ACF208', 'Email', unique=True),
        {'schema': 'identity'}
    )

    UserId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    Email = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
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
        PrimaryKeyConstraint('OtpLoginId', name='PK__OtpLogin__C597BB3125B8E061'),
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
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Journeys_UserId'),
        PrimaryKeyConstraint('JourneyId', name='PK__Journey__4159B9EF42D75CA4'),
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
    LockedUntil = mapped_column(DATETIME2)

    User_: Mapped['User'] = relationship('User', back_populates='Journey')
    Booking: Mapped[List['Booking']] = relationship('Booking', uselist=True, back_populates='Journey_')


class Booking(Base):
    __tablename__ = 'Booking'
    __table_args__ = (
        ForeignKeyConstraint(['BookingStatusId'], ['booking.BookingStatus.BookingStatusId'], name='FK_Booking_BookingStatus'),
        ForeignKeyConstraint(['JourneyId'], ['journey.Journey.JourneyId'], name='FK_Booking_Journey'),
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Booking_User'),
        PrimaryKeyConstraint('BookingId', name='PK__tmp_ms_x__73951AEDC08300A2'),
        {'schema': 'booking'}
    )

    BookingId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    UserId = mapped_column(Uuid, nullable=False)
    JourneyId = mapped_column(Uuid, nullable=False)
    BookingStatusId = mapped_column(Integer, nullable=False)
    FeeMargin = mapped_column(DECIMAL(18, 8), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))

    BookingStatus_: Mapped['BookingStatus'] = relationship('BookingStatus', back_populates='Booking')
    Journey_: Mapped['Journey'] = relationship('Journey', back_populates='Booking')
    User_: Mapped['User'] = relationship('User', back_populates='Booking')
    BookingAmmendment: Mapped[List['BookingAmmendment']] = relationship('BookingAmmendment', uselist=True, back_populates='Booking_')


class BookingAmmendment(Base):
    __tablename__ = 'BookingAmmendment'
    __table_args__ = (
        ForeignKeyConstraint(['BookingId'], ['booking.Booking.BookingId'], name='FK_BookingAmmendment_Booking'),
        PrimaryKeyConstraint('BookingAmmendmentId', name='PK__tmp_ms_x__59DE3C6ADA729EE5'),
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

    Booking_: Mapped['Booking'] = relationship('Booking', back_populates='BookingAmmendment')
