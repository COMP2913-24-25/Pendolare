from typing import List

from sqlalchemy import Boolean, CHAR, Column, DECIMAL, Float, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, Unicode, Uuid, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class UserType(Base):
    __tablename__ = 'UserType'
    __table_args__ = (
        PrimaryKeyConstraint('UserTypeId', name='PK__UserType__40D2D81688198308'),
        {'schema': 'identity'}
    )

    UserTypeId = mapped_column(Integer, Identity(start=1, increment=1))
    Type = mapped_column(Unicode(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False)
    Description = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))

    User: Mapped[List['User']] = relationship('User', uselist=True, back_populates='UserType_')


class TransactionStatus(Base):
    __tablename__ = 'TransactionStatus'
    __table_args__ = (
        PrimaryKeyConstraint('TransactionStatusId', name='PK__Transact__57B5E183E768F271'),
        Index('UQ__Transact__3A15923FDAFD136F', 'Status', unique=True),
        {'schema': 'payment'}
    )

    TransactionStatusId = mapped_column(Integer, Identity(start=1, increment=1))
    Status = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    Description = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Transaction: Mapped[List['Transaction']] = relationship('Transaction', uselist=True, back_populates='TransactionStatus_')


class TransactionType(Base):
    __tablename__ = 'TransactionType'
    __table_args__ = (
        PrimaryKeyConstraint('TransactionTypeId', name='PK__Transact__20266D0B7A9DF9AF'),
        Index('UQ__Transact__F9B8A48BAA4F2873', 'Type', unique=True),
        {'schema': 'payment'}
    )

    TransactionTypeId = mapped_column(Integer, Identity(start=1, increment=1))
    Type = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    Description = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Transaction: Mapped[List['Transaction']] = relationship('Transaction', uselist=True, back_populates='TransactionType_')


class ApiClient(Base):
    __tablename__ = 'ApiClient'
    __table_args__ = (
        PrimaryKeyConstraint('ApiClientId', name='PK__ApiClien__FDC5B7C88CC0C63A'),
        Index('UQ__ApiClien__E67E1A256E4AF289', 'ClientId', unique=True),
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
        PrimaryKeyConstraint('ConfigurationId', name='PK__Configur__95AA53BBF0A2BF33'),
        Index('UQ__Configur__C41E0289B09E9D07', 'Key', unique=True),
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
        PrimaryKeyConstraint('UserId', name='PK__User__1788CC4C3DDEDE83'),
        Index('IX_User_UserType', 'UserTypeId'),
        Index('UQ__User__A9D1053483D9390A', 'Email', unique=True),
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
    Transaction: Mapped[List['Transaction']] = relationship('Transaction', uselist=True, back_populates='User_')


class Transaction(Base):
    __tablename__ = 'Transaction'
    __table_args__ = (
        ForeignKeyConstraint(['TransactionStatusId'], ['payment.TransactionStatus.TransactionStatusId'], name='FK_Transaction_TransactionStatus'),
        ForeignKeyConstraint(['TransactionTypeId'], ['payment.TransactionType.TransactionTypeId'], name='FK_Transaction_TransactionType'),
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Transaction_UserId'),
        PrimaryKeyConstraint('TransactionId', name='PK__Transact__55433A6B8AF4ED30'),
        {'schema': 'payment'}
    )

    TransactionId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    UserId = mapped_column(Uuid, nullable=False)
    Value = mapped_column(DECIMAL(18, 8), nullable=False)
    CurrencyCode = mapped_column(CHAR(3, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TransactionStatusId = mapped_column(Integer, nullable=False)
    TransactionTypeId = mapped_column(Integer, nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False)
    UpdateDate = mapped_column(DATETIME2, nullable=False)

    TransactionStatus_: Mapped['TransactionStatus'] = relationship('TransactionStatus', back_populates='Transaction')
    TransactionType_: Mapped['TransactionType'] = relationship('TransactionType', back_populates='Transaction')
    User_: Mapped['User'] = relationship('User', back_populates='Transaction')


class UserBalance(User):
    __tablename__ = 'UserBalance'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_User_UserId'),
        PrimaryKeyConstraint('UserId', name='PK__UserBala__1788CC4C83D4CE91'),
        {'schema': 'payment'}
    )

    UserId = mapped_column(Uuid)
    Pending = mapped_column(Float(53), nullable=False, server_default=text('((0))'))
    NonPending = mapped_column(Float(53), nullable=False, server_default=text('((0))'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
