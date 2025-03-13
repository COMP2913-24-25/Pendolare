-- Test Data Setup Script

DELETE FROM [booking].[BookingAmmendment]
DELETE FROM [payment].[UserBalance]
DELETE FROM [booking].[Booking]
DELETE FROM [journey].[Journey]
DELETE FROM [identity].[OtpLogin]
DELETE FROM [identity].[User]
DELETE FROM [payment].[Transaction]

DECLARE @PassengerId UNIQUEIDENTIFIER = '11856ed2-e4b2-41a3-aae7-de4966800e95'
DECLARE @DriverId UNIQUEIDENTIFIER = '5800a98a-066b-45a3-8e64-a42b8a6d831a'
DECLARE @WeirdId UNIQUEIDENTIFIER = '00000000-0000-1111-0000-000000000000'

INSERT INTO [identity].[User]
(
    UserId,
    Email,
    FirstName,
    LastName,
    UserTypeId
)
VALUES
( @PassengerId, 'jameskinley24+passenger@gmail.com', 'James', 'Test', 1),
( @DriverId, 'jameskinley24+driver@gmail.com', 'Senor', 'Test', 1),
( @WeirdId, 'driver@gmail.com', 'Test', 'NoSheet', 1)


INSERT INTO [payment].[UserBalance]
(
    UserId,
    Pending,
    NonPending
)
VALUES
( @PassengerId, 24.99, 51.25),
( @DriverId, 12.34, 56.78)

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
( @OnetimeId, @DriverId, 11.99, @StartName, @StartLong, @StartLat, @EndName, @EndLong, @EndLat, 1, @StartDate, NULL, NULL, @StartTime, 3, 'WU60XGA'),
( @CommuterId, @DriverId, 15.99, @StartName, @StartLong, @StartLat, @EndName, @EndLong, @EndLat, 2, @StartDate, @RepeatUntil, '*/1 * * * *', @StartTime, 3, 'WU60XGA')

-- New alternate location variables with slightly different values:
DECLARE @AltStartLat FLOAT = 53.8135000000000,
        @AltStartLong FLOAT = -1.5750000000000,
        @AltStartName NVARCHAR(MAX) = 'New Location',
        @AltEndLat FLOAT = 53.8085000000000,
        @AltEndLong FLOAT = -1.5540000000000,
        @AltEndName NVARCHAR(MAX) = 'New End Location';

-------------------------------
-- Booking 1 - OneTime journey for Passenger
-------------------------------
DECLARE @BookingId1 UNIQUEIDENTIFIER;

DECLARE @NewBooking1 TABLE (BookingId UNIQUEIDENTIFIER);

INSERT INTO [booking].[Booking]
       (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking1
VALUES
       (@PassengerId, @OneTimeId, 1, 0.05, GETDATE(), 0);

SELECT @BookingId1 = BookingId FROM @NewBooking1;

-- Insert a corresponding amendment for Booking 1 using alternate location values
INSERT INTO [booking].[BookingAmmendment]
       (BookingId, ProposedPrice, StartName, StartLong, StartLat,
        EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
       (@BookingId1, 12.50, @AltStartName, @AltStartLong, @AltStartLat,
        @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 1, 1);

-------------------------------
-- Booking 2 - Commuter journey for Passenger
-------------------------------
DECLARE @BookingId2 UNIQUEIDENTIFIER;

DECLARE @NewBooking2 TABLE (BookingId UNIQUEIDENTIFIER);

INSERT INTO [booking].[Booking]
       (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking2
VALUES
       (@PassengerId, @CommuterId, 2, 0.025, GETDATE(), 0);

SELECT @BookingId2 = BookingId FROM @NewBooking2;

-- Insert a corresponding amendment for Booking 2 using alternate location values
INSERT INTO [booking].[BookingAmmendment]
       (BookingId, ProposedPrice, StartName, StartLong, StartLat,
        EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
       (@BookingId2, 9.00, @AltStartName, @AltStartLong, @AltStartLat,
        @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

-------------------------------
-- Booking 3 - OneTime journey for Driver (example scenario)
-------------------------------
DECLARE @BookingId3 UNIQUEIDENTIFIER;

DECLARE @NewBooking3 TABLE (BookingId UNIQUEIDENTIFIER);

INSERT INTO [booking].[Booking]
       (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking3
VALUES
       (@DriverId, @OneTimeId, 3, 0.115, GETDATE(), 1);

SELECT @BookingId3 = BookingId FROM @NewBooking3;

-- Insert a corresponding amendment for Booking 3 using alternate location values
INSERT INTO [booking].[BookingAmmendment]
       (BookingId, ProposedPrice, StartName, StartLong, StartLat,
        EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
       (@BookingId3, 13.00, @AltStartName, @AltStartLong, @AltStartLat,
        @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 1, 0);


SELECT * FROM [identity].[User]
SELECT * FROM [journey].[Journey]
SELECT * FROM [booking].[Booking]
SELECT * FROM [booking].[BookingAmmendment]
SELECT * FROM [payment].[UserBalance]