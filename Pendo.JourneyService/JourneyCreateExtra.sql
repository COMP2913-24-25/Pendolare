-- Test Data Setup Script

-- Clean up existing data
DELETE FROM [identity].[User];
DELETE FROM [journey].[Journey];

-- Declare User IDs
DECLARE @PassengerId UNIQUEIDENTIFIER = '11856ed2-e4b2-41a3-aae7-de4966800e95';
DECLARE @DriverId UNIQUEIDENTIFIER = '5800a98a-066b-45a3-8e64-a42b8a6d831a';

-- Insert Users
INSERT INTO [identity].[User]
(
    UserId,
    Email,
    FirstName,
    LastName,
    UserTypeId
)
VALUES
( @PassengerId, 'jameskinley24+passenger@gmail.com', 'First', 'Last', 1),
( @DriverId, 'jameskinley24+driver@gmail.com', 'Señor', 'Pendo', 1);

-- Select to verify users are inserted correctly
SELECT * FROM [identity].[User];

-- Verify that users are inserted
IF EXISTS (SELECT 1 FROM [identity].[User] WHERE UserId = @PassengerId) AND
   EXISTS (SELECT 1 FROM [identity].[User] WHERE UserId = @DriverId)
BEGIN
    -- Declare Journey Data
    DECLARE @Journey1Id UNIQUEIDENTIFIER = NEWID();
    DECLARE @Journey2Id UNIQUEIDENTIFIER = NEWID();
    DECLARE @Journey3Id UNIQUEIDENTIFIER = NEWID();
    DECLARE @Journey4Id UNIQUEIDENTIFIER = NEWID();
    DECLARE @Journey5Id UNIQUEIDENTIFIER = NEWID();
    DECLARE @Journey6Id UNIQUEIDENTIFIER = NEWID();

    -- Insert Journey Records
    INSERT INTO [journey].[Journey]
    (
        JourneyId, UserId, AdvertisedPrice, CurrencyCode, StartName, StartLong, StartLat, EndName, EndLong, EndLat, 
        JourneyType, StartDate, StartTime, JourneyStatusId, MaxPassengers, RegPlate, CreateDate, UpdateDate
    )
    VALUES
    ( @Journey1Id, @PassengerId, 100.00, 'GBP', 'London', -0.1276, 51.5074, 'Manchester', -2.2426, 53.4808, 
      1, '2025-03-10', '2025-03-10 08:00:00', 1, 4, 'ABC123', GETUTCDATE(), GETUTCDATE() ),

    ( @Journey2Id, @PassengerId, 120.50, 'GBP', 'Bristol', -2.5879, 51.4545, 'Cardiff', -3.1791, 51.4816, 
      1, '2025-03-11', '2025-03-11 10:00:00', 1, 3, 'DEF456', GETUTCDATE(), GETUTCDATE() ),

    ( @Journey3Id, @DriverId, 150.00, 'GBP', 'Leeds', -1.5491, 53.8008, 'Liverpool', -2.9784, 53.4084, 
      1, '2025-03-12', '2025-03-12 12:00:00', 1, 2, 'GHI789', GETUTCDATE(), GETUTCDATE() ),

    ( @Journey4Id, @DriverId, 200.00, 'GBP', 'Newcastle', -1.6170, 54.9784, 'Sheffield', -1.4659, 53.3811, 
      1, '2025-03-13', '2025-03-13 14:00:00', 1, 5, 'JKL012', GETUTCDATE(), GETUTCDATE() ),

    ( @Journey5Id, @PassengerId, 90.75, 'GBP', 'Oxford', -1.2578, 51.7548, 'Cambridge', 0.1218, 52.2053, 
      1, '2025-03-14', '2025-03-14 16:00:00', 1, 4, 'MNO345', GETUTCDATE(), GETUTCDATE() ),

    ( @Journey6Id, @DriverId, 250.00, 'GBP', 'Glasgow', -4.2518, 55.8642, 'Edinburgh', -3.1883, 55.9533, 
      1, '2025-03-15', '2025-03-15 18:00:00', 1, 6, 'PQR678', GETUTCDATE(), GETUTCDATE() );

    -- Select to verify the journeys
    SELECT * FROM [journey].[Journey];
END
ELSE
BEGIN
    PRINT 'User insertion failed. Cannot insert journey records.';
END