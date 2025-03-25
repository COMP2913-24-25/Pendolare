from typing import List

from sqlalchemy import Boolean, CHAR, Column, DECIMAL, Float, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, Unicode, Uuid, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class BookingStatus(Base):
    __tablename__ = 'BookingStatus'
    __table_args__ = (
        PrimaryKeyConstraint('BookingStatusId', name='PK__BookingS__54F9C05D1416A3EF'),
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
        PrimaryKeyConstraint('UserTypeId', name='PK__UserType__40D2D816F5FB6F9D'),
        {'schema': 'identity'}
    )

    UserTypeId = mapped_column(Integer, Identity(start=1, increment=1))
    Type = mapped_column(Unicode(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False)
    Description = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))

    User: Mapped[List['User']] = relationship('User', uselist=True, back_populates='UserType_')


class Conversations(Base):
    __tablename__ = 'Conversations'
    __table_args__ = (
        PrimaryKeyConstraint('ConversationId', name='PK__Conversa__C050D877485655A0'),
        {'schema': 'messaging'}
    )

    ConversationId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    Type = mapped_column(Unicode(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    Name = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))

    ConversationParticipants: Mapped[List['ConversationParticipants']] = relationship('ConversationParticipants', uselist=True, back_populates='Conversations_')
    Messages: Mapped[List['Messages']] = relationship('Messages', uselist=True, back_populates='Conversations_')


class TransactionStatus(Base):
    __tablename__ = 'TransactionStatus'
    __table_args__ = (
        PrimaryKeyConstraint('TransactionStatusId', name='PK__Transact__57B5E183C0C1C4ED'),
        Index('UQ__Transact__3A15923FD3962333', 'Status', unique=True),
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
        PrimaryKeyConstraint('TransactionTypeId', name='PK__Transact__20266D0B6CDAF3CC'),
        Index('UQ__Transact__F9B8A48BF5517BAA', 'Type', unique=True),
        {'schema': 'payment'}
    )

    TransactionTypeId = mapped_column(Integer, Identity(start=1, increment=1))
    Type = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    Description = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Transaction: Mapped[List['Transaction']] = relationship('Transaction', uselist=True, back_populates='TransactionType_')


class Configuration(Base):
    __tablename__ = 'Configuration'
    __table_args__ = (
        PrimaryKeyConstraint('ConfigurationId', name='PK__Configur__95AA53BB45C5F8A0'),
        Index('UQ__Configur__C41E0289317BF8DB', 'Key', unique=True),
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
        PrimaryKeyConstraint('UserId', name='PK__User__1788CC4C1A2C762B'),
        Index('IX_User_UserType', 'UserTypeId'),
        Index('UQ__User__A9D10534E084D742', 'Email', unique=True),
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
    ConversationParticipants: Mapped[List['ConversationParticipants']] = relationship('ConversationParticipants', uselist=True, back_populates='User_')
    Messages: Mapped[List['Messages']] = relationship('Messages', uselist=True, back_populates='User_')
    Transaction: Mapped[List['Transaction']] = relationship('Transaction', uselist=True, back_populates='User_')
    Booking: Mapped[List['Booking']] = relationship('Booking', uselist=True, back_populates='User_')


class OtpLogin(Base):
    __tablename__ = 'OtpLogin'
    __table_args__ = (
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_OtpLogin_User'),
        PrimaryKeyConstraint('OtpLoginId', name='PK__OtpLogin__C597BB311E265A7D'),
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
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Journeys_UserId'),
        PrimaryKeyConstraint('JourneyId', name='PK__Journey__4159B9EF0E1B7E52'),
        {'schema': 'journey'}
    )

    JourneyId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    UserId = mapped_column(Uuid, nullable=False)
    AdvertisedPrice = mapped_column(DECIMAL(18, 8), nullable=False)
    CurrencyCode = mapped_column(CHAR(3, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, server_default=text("('GBP')"))
    StartName = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    StartLong = mapped_column(Float(53), nullable=False)
    StartLat = mapped_column(Float(53), nullable=False)
    EndName = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    EndLong = mapped_column(Float(53), nullable=False)
    EndLat = mapped_column(Float(53), nullable=False)
    JourneyType = mapped_column(Integer, nullable=False, server_default=text('((1))'))
    StartDate = mapped_column(DATETIME2, nullable=False)
    StartTime = mapped_column(DATETIME2, nullable=False)
    JourneyStatusId = mapped_column(Integer, nullable=False, server_default=text('((1))'))
    MaxPassengers = mapped_column(Integer, nullable=False)
    RegPlate = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    UpdateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    RepeatUntil = mapped_column(DATETIME2)
    Recurrance = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    BootWidth = mapped_column(Float(53))
    BootHeight = mapped_column(Float(53))
    LockedUntil = mapped_column(DATETIME2)

    User_: Mapped['User'] = relationship('User', back_populates='Journey')
    Booking: Mapped[List['Booking']] = relationship('Booking', uselist=True, back_populates='Journey_')


class ConversationParticipants(Base):
    __tablename__ = 'ConversationParticipants'
    __table_args__ = (
        ForeignKeyConstraint(['ConversationId'], ['messaging.Conversations.ConversationId'], ondelete='CASCADE', name='FK_ConversationParticipants_Conversations'),
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_ConversationParticipants_Users'),
        PrimaryKeyConstraint('ConversationId', 'UserId', name='PK__Conversa__112854B398DE4EE1'),
        Index('IX_ConversationParticipants_UserId', 'UserId'),
        {'schema': 'messaging'}
    )

    ConversationId = mapped_column(Uuid, nullable=False)
    UserId = mapped_column(Uuid, nullable=False)
    JoinedAt = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    LeftAt = mapped_column(DATETIME2)

    Conversations_: Mapped['Conversations'] = relationship('Conversations', back_populates='ConversationParticipants')
    User_: Mapped['User'] = relationship('User', back_populates='ConversationParticipants')


class Messages(Base):
    __tablename__ = 'Messages'
    __table_args__ = (
        ForeignKeyConstraint(['ConversationId'], ['messaging.Conversations.ConversationId'], ondelete='CASCADE', name='FK_Messages_Conversations'),
        ForeignKeyConstraint(['SenderId'], ['identity.User.UserId'], name='FK_Messages_Sender'),
        PrimaryKeyConstraint('MessageId', name='PK__Messages__C87C0C9CC7F08CF7'),
        Index('IX_Messages_ConversationId', 'ConversationId'),
        Index('IX_Messages_SenderId', 'SenderId'),
        {'schema': 'messaging'}
    )

    MessageId = mapped_column(Uuid, server_default=text('(newsequentialid())'))
    ConversationId = mapped_column(Uuid, nullable=False)
    SenderId = mapped_column(Uuid, nullable=False)
    MessageType = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Content = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreateDate = mapped_column(DATETIME2, nullable=False, server_default=text('(getutcdate())'))
    IsDeleted = mapped_column(Boolean, nullable=False, server_default=text('((0))'))
    EditedAt = mapped_column(DATETIME2)

    Conversations_: Mapped['Conversations'] = relationship('Conversations', back_populates='Messages')
    User_: Mapped['User'] = relationship('User', back_populates='Messages')

class Transaction(Base):
    __tablename__ = 'Transaction'
    __table_args__ = (
        ForeignKeyConstraint(['TransactionStatusId'], ['payment.TransactionStatus.TransactionStatusId'], name='FK_Transaction_TransactionStatus'),
        ForeignKeyConstraint(['TransactionTypeId'], ['payment.TransactionType.TransactionTypeId'], name='FK_Transaction_TransactionType'),
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Transaction_UserId'),
        PrimaryKeyConstraint('TransactionId', name='PK__Transact__55433A6B9A03CACE'),
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


class Booking(Base):
    __tablename__ = 'Booking'
    __table_args__ = (
        ForeignKeyConstraint(['BookingStatusId'], ['booking.BookingStatus.BookingStatusId'], name='FK_Booking_BookingStatus'),
        ForeignKeyConstraint(['JourneyId'], ['journey.Journey.JourneyId'], name='FK_Booking_Journey'),
        ForeignKeyConstraint(['UserId'], ['identity.User.UserId'], name='FK_Booking_User'),
        PrimaryKeyConstraint('BookingId', name='PK__Booking__73951AEDA8F2838F'),
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

    BookingStatus_: Mapped['BookingStatus'] = relationship('BookingStatus', back_populates='Booking')
    Journey_: Mapped['Journey'] = relationship('Journey', back_populates='Booking')
    User_: Mapped['User'] = relationship('User', back_populates='Booking')
    BookingAmmendment: Mapped[List['BookingAmmendment']] = relationship('BookingAmmendment', uselist=True, back_populates='Booking_')


class BookingAmmendment(Base):
    __tablename__ = 'BookingAmmendment'
    __table_args__ = (
        ForeignKeyConstraint(['BookingId'], ['booking.Booking.BookingId'], name='FK_BookingAmmendment_Booking'),
        PrimaryKeyConstraint('BookingAmmendmentId', name='PK__BookingA__59DE3C6ABB887240'),
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