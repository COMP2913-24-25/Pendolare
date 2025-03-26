-- Clear existing data
DELETE FROM [booking].[BookingAmendment]
DELETE FROM [payment].[UserBalance]
DELETE FROM [booking].[Booking]
DELETE FROM [journey].[Journey]
DELETE FROM [identity].[User]

-- Declare user IDs
DECLARE @PassengerId UNIQUEIDENTIFIER = '11856ed2-e4b2-1111-aae7-de4966800e95'
DECLARE @DriverId UNIQUEIDENTIFIER = '5800a98a-066b-1111-8e64-a42b8a6d831a'
DECLARE @WeirdId UNIQUEIDENTIFIER = '00000000-0000-1111-1111-000000000000'

-- Insert Users
INSERT INTO [identity].[User]
(
    UserId,
    Email,
    FirstName,
    LastName,
    UserTypeId,
    UserRating
)
VALUES
( @PassengerId, 'jameskinley24+passenger@gmail.com', 'James', 'Test', 1, -1),
( @DriverId, 'jameskinley24+driver@gmail.com', 'Senor', 'Test', 1, -1),
( @WeirdId, 'driver@gmail.com', 'Test', 'NoSheet', 1, -1)

-- Insert User Balances
INSERT INTO [payment].[UserBalance]
(
    UserId,
    Pending,
    NonPending
)
VALUES
( @PassengerId, 24.99, 51.25),
( @DriverId, 12.34, 56.78)

-- Declare journey-specific variables
DECLARE @OnetimeId UNIQUEIDENTIFIER = '1025c943-62f2-4692-885c-4e064f7f486b'
DECLARE @CommuterId UNIQUEIDENTIFIER = '094d53f9-5f3b-4de8-af7d-89972d31e2af'

DECLARE @StartLat FLOAT = 53.8129997253418
DECLARE @StartLong FLOAT = -1.5748614072799683
DECLARE @StartName NVARCHAR(MAX) = '189 Cardigan Lane, Hyde Park, Leeds LS6 1DX, England'

DECLARE @EndLat FLOAT = 53.80797576904297
DECLARE @EndLong FLOAT = -1.5533339977264404
DECLARE @EndName NVARCHAR(MAX) = 'University of, Sir William Henry Bragg Building, Woodhouse Ln, Leeds LS2 9JT'

DECLARE @StartDate DATETIME2 = '2025-03-20'
DECLARE @StartTime DATETIME2 = '2025-03-20 10:10:00'

DECLARE @RepeatUntil DATETIME2 = '2025-10-20'

-- Insert Journeys
INSERT INTO [journey].[Journey]
(
    JourneyId,
    UserId,
    AdvertisedPrice,
    StartName,
    StartLong,
    StartLat,
    EndName,
    EndLong,
    EndLat,
    JourneyType,
    StartDate,
    RepeatUntil,
    Recurrance,
    StartTime,
    MaxPassengers,
    RegPlate
)
VALUES
( @OnetimeId, @DriverId, 11.99, @StartName, @StartLong, @StartLat, @EndName, @EndLong, @EndLat, 1, @StartDate, @StartDate, NULL, @StartTime, 3, 'WU60XGA'),
( @CommuterId, @DriverId, 15.99, @StartName, @StartLong, @StartLat, @EndName, @EndLong, @EndLat, 2, @StartDate, @RepeatUntil, '*/1 * * * *', @StartTime, 3, 'WU60XGA')

-- Alternate location variables
DECLARE @AltStartLat FLOAT = 53.8135000000000,
        @AltStartLong FLOAT = -1.5750000000000,
        @AltStartName NVARCHAR(MAX) = 'New Location',
        @AltEndLat FLOAT = 53.8085000000000,
        @AltEndLong FLOAT = -1.5540000000000,
        @AltEndName NVARCHAR(MAX) = 'New End Location'

-------------------------------
-- Booking 1 - OneTime journey for Passenger
-------------------------------
DECLARE @BookingId1 UNIQUEIDENTIFIER = NEWID()

INSERT INTO [booking].[Booking]
(
    BookingId,
    UserId, 
    JourneyId, 
    BookingStatusId, 
    FeeMargin, 
    RideTime, 
    DriverApproval
)
VALUES
(
    @BookingId1,
    @PassengerId, 
    @OnetimeId, 
    1, 
    0.05, 
    GETDATE(), 
    0
)

-- Insert a corresponding amendment for Booking 1
INSERT INTO [booking].[BookingAmendment]
(
    BookingId, 
    ProposedPrice, 
    StartName, 
    StartLong, 
    StartLat,
    EndName, 
    EndLong, 
    EndLat, 
    StartTime, 
    CancellationRequest, 
    DriverApproval, 
    PassengerApproval
)
VALUES
(
    @BookingId1, 
    12.50, 
    @AltStartName, 
    @AltStartLong, 
    @AltStartLat,
    @AltEndName, 
    @AltEndLong, 
    @AltEndLat, 
    GETDATE(), 
    0, 
    1, 
    1
)

-- More Booking inserts (similar to the first one)...

-- Verify inserted data
SELECT * FROM [identity].[User]
SELECT * FROM [journey].[Journey]
SELECT * FROM [booking].[Booking]
SELECT * FROM [booking].[BookingAmendment]
SELECT * FROM [payment].[UserBalance]