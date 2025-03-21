/*
Author: James Kinley
Created: 21/03/2025
Description: Creates all necessary triggers, ensuring certain behaviour is implemented. Ideally, the Booking Service should handle this, but this is equally valid!
*/

IF OBJECT_ID('[booking].[trg_UpdateJourneyStatusOnBooking]', 'TR') IS NOT NULL
    DROP TRIGGER [booking].[trg_UpdateJourneyStatusOnBooking];
GO

CREATE TRIGGER [booking].[trg_UpdateJourneyStatusOnBooking]
ON [booking].[Booking]
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE j
    SET JourneyStatusId = 2
    FROM [journey].[Journey] AS j
    INNER JOIN inserted AS i
        ON j.JourneyId = i.JourneyId;
END;
GO
