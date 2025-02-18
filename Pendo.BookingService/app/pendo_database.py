from typing import List

from sqlalchemy import Boolean, Column, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, Unicode, Uuid, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class UserType(Base):
    __tablename__ = 'UserType'
    __table_args__ = (
        PrimaryKeyConstraint('UserTypeId', name='PK__UserType__40D2D816B9BC8D7B'),
        {'schema': 'identity'}
    )

    UserTypeId = mapped_column(Integer, Identity(start=1, increment=1))
    Type = mapped_column(Unicode(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False)
    Description = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))

    User: Mapped[List['User']] = relationship('User', uselist=True, back_populates='UserType_')


class Journey(Base):
    __tablename__ = 'Journey'
    __table_args__ = (
        PrimaryKeyConstraint('JourneyId', name='PK__Journey__4159B9EFAD771F37'),
        {'schema': 'journey'}
    )

    JourneyId = mapped_column(Uuid, server_default=text('(newsequentialid())'))

    Booking: Mapped[List['Booking']] = relationship('Booking', uselist=True, back_populates='Journey_')


class ApiClient(Base):
    __tablename__ = 'ApiClient'
    __table_args__ = (
        PrimaryKeyConstraint('ApiClientId', name='PK__ApiClien__FDC5B7C8FE635A06'),
        Index('UQ__ApiClien__E67E1A258BCBA206', 'ClientId', unique=True),
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
        PrimaryKeyConstraint('ConfigurationId', name='PK__Configur__95AA53BBA24C240A'),
        Index('UQ__Configur__C41E028996836B0C', 'Key', unique=True),
        {'schema': 'shared'}
    )

    ConfigurationId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    Key = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Value = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))


class User(Base):
    __tablename__ = 'User'
    __table_args__ = (
        ForeignKeyConstraint(['UserTypeId'], ['identity.UserType.UserTypeId'], name='FK_User_UserType'),
        PrimaryKeyConstraint('UserId', name='PK__User__1788CC4CDA6BA344'),
        Index('IX_User_UserType', 'UserTypeId'),
        Index('UQ__User__A9D1053499042E96', 'Email', unique=True),
        {'schema': 'identity'}
    )

    UserId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    Email = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FirstName = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    LastName = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UserTypeId = mapped_column(Integer, nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))

    UserType_: Mapped['UserType'] = relationship('UserType', back_populates='User')
    Booking: Mapped[List['Booking']] = relationship('Booking', uselist=True, back_populates='User_')


class Booking(Base):
    __tablename__ = 'Booking'
    __table_args__ = (
        ForeignKeyConstraint(['JourneyId'], ['journey.Journey.JourneyId'], name='FK_Booking_Journey'),
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Booking_User'),
        PrimaryKeyConstraint('BookingId', name='PK__Booking__73951AED299B75A6'),
        {'schema': 'booking'}
    )

    BookingId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    UserId = mapped_column(Uuid, nullable=False)
    JourneyId = mapped_column(Uuid, nullable=False)
    Status = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, server_default=text("('pending')"))
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))

    Journey_: Mapped['Journey'] = relationship('Journey', back_populates='Booking')
    User_: Mapped['User'] = relationship('User', back_populates='Booking')
