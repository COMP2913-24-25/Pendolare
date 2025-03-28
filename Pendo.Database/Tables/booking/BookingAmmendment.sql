/*
Author: James Kinley
Created: 27/02/2025
Description: Creates Booking Ammendment Table
*/

CREATE TABLE [booking].[BookingAmmendment]
(
  [BookingAmmendmentId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [BookingId] UNIQUEIDENTIFIER NOT NULL,
  [ProposedPrice] DECIMAL(18, 8) NULL, -- Will use the same currency code as the journey
  [StartName] NVARCHAR(MAX) NULL,
  [StartLong] FLOAT NULL,
  [StartLat] FLOAT NULL,
  [EndName] NVARCHAR(MAX) NULL,
  [EndLong] FLOAT NULL,
  [EndLat] FLOAT NULL,
  [StartTime] DATETIME2 NULL,
  [CancellationRequest] BIT NOT NULL DEFAULT 0,
  [DriverApproval] BIT NOT NULL DEFAULT 0,
  [PassengerApproval] BIT NOT NULL DEFAULT 0,
  [Recurrance] NVARCHAR(100) NULL,
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
  [UpdateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

  CONSTRAINT FK_BookingAmmendment_Booking FOREIGN KEY ([BookingId])
  REFERENCES [booking].[Booking](BookingId)
);