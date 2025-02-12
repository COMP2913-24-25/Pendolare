/*
Author: Catherine Weightman
Created: 11/02/2025
Description: Creates Commuting Details Table
*/

CREATE TABLE [journey].[CommutingDetails]
(
  [CommutingId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [JourneyId] INT NOT NULL,
  [RepeatFrequency] NVARCHAR(100) NULL,
  [RepeatUntilDate] DATE NOT NULL,
  [DayOfWeek] NVARCHAR(100) NULL,
  [Time] INT NOT NULL,

  CONSTRAINT FK_CommutingDetails_JourneyId FOREIGN KEY ([JourneyId]) 
  REFERENCES [journey].[Journeys](JourneyId)
)
