/*
Authors: Shay O'Donnell, James Kinley
Created: 13/02/2025
Description: Creates Booking Table
*/

CREATE TABLE [booking].[Booking]
(
  [BookingId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [UserId] UNIQUEIDENTIFIER NOT NULL, --The UserId of the passenger
  [JourneyId] UNIQUEIDENTIFIER NOT NULL,
  [BookingStatusId] INT NOT NULL,
  [FeeMargin] DECIMAL(18, 8) NOT NULL, --Set so this is set in stone at time of booking, not affected by platform changes made after this!
  [RideTime] DATETIME2 NOT NULL, --Must exist for sake of commuter journeys
  [DriverApproval] BIT NOT NULL DEFAULT 0, --Only relevant when no ammendments are made.
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
  [UpdateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
  [BookedWindowEnd] DATETIME2 NULL, --For commuter journeys only

  CONSTRAINT FK_Booking_User FOREIGN KEY ([UserId]) 
  REFERENCES [identity].[User](UserId),

  CONSTRAINT FK_Booking_Journey FOREIGN KEY ([JourneyId]) 
  REFERENCES [journey].[Journey](JourneyId),

  CONSTRAINT FK_Booking_BookingStatus FOREIGN KEY ([BookingStatusId])
  REFERENCES [booking].[BookingStatus](BookingStatusId)
);