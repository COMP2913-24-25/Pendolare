-- Test Data Setup Script

-- Clear existing data to ensure clean slate
DELETE FROM [payment].[Transaction]
DELETE FROM [booking].[BookingAmmendment]
DELETE FROM [payment].[UserBalance]
DELETE FROM [booking].[Booking]
DELETE FROM [journey].[Journey]
DELETE FROM [identity].[OtpLogin]
DELETE FROM [identity].[User]

-- Declare User IDs
DECLARE @PassengerId1 UNIQUEIDENTIFIER = NEWID()
DECLARE @DriverId1 UNIQUEIDENTIFIER = NEWID()
DECLARE @PassengerId2 UNIQUEIDENTIFIER = NEWID()
DECLARE @DriverId2 UNIQUEIDENTIFIER = NEWID()

-- Declare Journey IDs
DECLARE @Journey1Id UNIQUEIDENTIFIER = NEWID()
DECLARE @Journey2Id UNIQUEIDENTIFIER = NEWID()

-- Declare Booking IDs
DECLARE @Booking1Id UNIQUEIDENTIFIER = NEWID()
DECLARE @Booking2Id UNIQUEIDENTIFIER = NEWID()

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
( @PassengerId1, 'james.passenger1@example.com', 'James', 'Passenger', 1),
( @DriverId1, 'john.driver1@example.com', 'John', 'Driver', 2),
( @PassengerId2, 'sarah.passenger2@example.com', 'Sarah', 'Traveler', 1),
( @DriverId2, 'mike.driver2@example.com', 'Mike', 'Rider', 2)

-- Insert User Balances
INSERT INTO [payment].[UserBalance]
(
    UserId,
    Pending,
    NonPending
)
VALUES
( @PassengerId1, 50.00, 100.00),
( @DriverId1, 25.50, 200.00),
( @PassengerId2, 30.00, 75.50),
( @DriverId2, 15.75, 180.25)

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
    StartTime,
    MaxPassengers,
    RegPlate
)
VALUES
( @Journey1Id, @DriverId1, 15.50, 'Leeds City Centre', -1.5490, 53.8008, 'University of Leeds', -1.5533, 53.8078, 1, '2025-06-15', '2025-12-31', '2025-06-15 09:00:00', 3, 'AB12 CDE'),
( @Journey2Id, @DriverId2, 12.75, 'Manchester Central', -2.2474, 53.4794, 'Manchester University', -2.2335, 53.4668, 1, '2025-06-16', '2025-12-31', '2025-06-16 10:30:00', 2, 'XY23 DEF')

-- Insert Bookings
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
( @Booking1Id, @PassengerId1, @Journey1Id, 1, 0.05, '2025-06-15 09:00:00', 1),
( @Booking2Id, @PassengerId2, @Journey2Id, 1, 0.04, '2025-06-16 10:30:00', 1)

-- Insert Booking Amendments
INSERT INTO [booking].[BookingAmmendment]
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
( @Booking1Id, 15.50, 'Leeds City Centre', -1.5490, 53.8008, 'University of Leeds', -1.5533, 53.8078, '2025-06-15 09:00:00', 0, 1, 1),
( @Booking2Id, 12.75, 'Manchester Central', -2.2474, 53.4794, 'Manchester University', -2.2335, 53.4668, '2025-06-16 10:30:00', 0, 1, 1)

-- Verify Inserted Data
SELECT * FROM [identity].[User]
SELECT * FROM [journey].[Journey]
SELECT * FROM [booking].[Booking]
SELECT * FROM [booking].[BookingAmmendment]
SELECT * FROM [payment].[UserBalance]