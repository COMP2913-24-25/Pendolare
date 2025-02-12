/*
Author: Catherine Weightman
Created: 11/02/2025
Description: Creates Journeys Table
*/

CREATE TABLE [journey].[Journeys]
(
  [JourneyId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [UserId] INT NOT NULL,
  [Cost] DECIMAL(18,8) NOT NULL,
  [StartLocation] NVARCHAR(100) NULL,
  [EndLocation] NVARCHAR(100) NULL,
  [JourneyType] NVARCHAR(100) NULL,
  [JourneyDate] DATE NOT NULL,
  [StartTime] INT NOT NULL,
  [EndTime] INT NOT NULL,
  [MaxPassengers] INT NOT NULL,
  [RegPlate] NVARCHAR(100) NULL,
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

  CONSTRAINT FK_Journeys_UserId FOREIGN KEY ([UserId]) 
  REFERENCES [identity].[User](UserId)
)

