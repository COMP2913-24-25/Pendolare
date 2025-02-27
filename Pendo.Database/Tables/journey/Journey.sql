/*
Author: Catherine Weightman
Created: 11/02/2025
Description: Creates Journey Table
*/

CREATE TABLE [journey].[Journey]
(
  [JourneyId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [UserId] UNIQUEIDENTIFIER NOT NULL,
  [AdvertisedPrice] DECIMAL(18,8) NOT NULL,
  [CurrencyCode] CHAR(3) NOT NULL DEFAULT 'GBP',
  [StartName] NVARCHAR(100) NOT NULL,
  [StartLong] FLOAT NOT NULL,
  [StartLat] FLOAT NOT NULL,
  [EndName] NVARCHAR(100) NOT NULL,
  [EndLong] FLOAT NOT NULL,
  [EndLat] FLOAT NOT NULL,
  [JourneyType] INT NOT NULL DEFAULT 1, -- 1 = One time only, 2 = Commuter (implied by having a cron + RepeatUntil)
  [StartDate] DATETIME2 NOT NULL,
  [RepeatUntil] DATETIME2 NOT NULL,
  [Recurrance] NVARCHAR(100) NULL, -- This will be a cron expression - see https://en.wikipedia.org/wiki/Cron
  [StartTime] DATETIME2 NOT NULL,
  [JourneyStatusId] INT NOT NULL DEFAULT 1, -- 1 = Advertised, 2 = Booked (For now!)
  [MaxPassengers] INT NOT NULL,
  [RegPlate] NVARCHAR(100) NOT NULL,
  [BootWidth] FLOAT NULL,
  [BootHeight] FLOAT NULL,
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
  [UpdateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
  [LockedUntil] DATETIME2 NULL, --Set this to hide the journey from booking until the set datetime

  CONSTRAINT FK_Journeys_UserId FOREIGN KEY ([UserId]) 
  REFERENCES [identity].[User](UserId)
)