/*
Author: James Kinley
Created: 07/02/2025
Description: Creates transaction payment table.
*/

CREATE TABLE [payment].[Transaction]
(
  [TransactionId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [UserId] UNIQUEIDENTIFIER NOT NULL,
  [BookingId] UNIQUEIDENTIFIER NULL,
  [Value] DECIMAL(18,8) NOT NULL,
  [CurrencyCode] CHAR(3) NOT NULL,
  [TransactionStatusId] INT NOT NULL,
  [TransactionTypeId] INT NOT NULL,
  [CreateDate] DATETIME2 NOT NULL,
  [UpdateDate] DATETIME2 NOT NULL,

  CONSTRAINT FK_Transaction_UserId FOREIGN KEY ([UserId])
  REFERENCES [identity].[User](UserId),

  CONSTRAINT FK_Transaction_TransactionStatus FOREIGN KEY ([TransactionStatusId])
  REFERENCES [payment].[TransactionStatus](TransactionStatusId),

  CONSTRAINT FK_Transaction_TransactionType FOREIGN KEY ([TransactionTypeId])
  REFERENCES [payment].[TransactionType](TransactionTypeId),

  CONSTRAINT FK_Transaction_TransactionBooking FOREIGN KEY ([BookingId])
  REFERENCES [booking].[Booking](BookingId)
);