/*
Author: Shay O'Donnell
Created: 13/02/2025
Description: Creates Booking Table
*/

CREATE TABLE [booking].[Booking]
(
  [BookingId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [UserId] UNIQUEIDENTIFIER NOT NULL,
  [JourneyId] UNIQUEIDENTIFIER NOT NULL,
  [BookingStatusId] INT NOT NULL,
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
  [UpdateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

  CONSTRAINT FK_Booking_User FOREIGN KEY ([UserId]) 
  REFERENCES [identity].[User](UserId),

  CONSTRAINT FK_Booking_Journey FOREIGN KEY ([JourneyId]) 
  REFERENCES [journey].[Journey](JourneyId),

  CONSTRAINT FK_Booking_BookingStatus FOREIGN KEY ([BookingStatusId])
  REFERENCES [booking].[BookingStatus](BookingStatusId)
);