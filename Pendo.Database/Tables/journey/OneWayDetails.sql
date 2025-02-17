/*
Author: Catherine Weightman
Created: 16/02/2025
Description: Creates One Way Journey Details Table
*/

CREATE TABLE [journey].[CommutingDetails]
(
  [OneTimeId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [JourneyId] INT NOT NULL,
  [JourneyDate] DATE NOT NULL,
  [JourneyTime] NVARCHAR(100) NULL,

  CONSTRAINT FK_OneWayDetails_JourneyId FOREIGN KEY ([JourneyId]) 
  REFERENCES [journey].[Journeys](JourneyId)
)