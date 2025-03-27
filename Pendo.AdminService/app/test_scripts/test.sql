-- Test Data Setup Script

USE [Pendo.Database];

DELETE FROM [booking].[BookingAmmendment]
DELETE FROM [booking].[Booking]
DELETE FROM [journey].[Journey]
DELETE FROM [identity].[OtpLogin]
DELETE FROM [identity].[User]
DELETE FROM [payment].[Transaction]
DELETE FROM [payment].[Discounts]

-- Declare User IDs
DECLARE @PassengerId1 UNIQUEIDENTIFIER = '11856ed2-e4b2-41a3-aae7-de4966800e95'
DECLARE @PassengerId2 UNIQUEIDENTIFIER = '22967fa3-5cb3-42b4-bf88-e05a77911f06'  -- Added a second passenger
DECLARE @DriverId1 UNIQUEIDENTIFIER = '5800a98a-066b-45a3-8e64-a42b8a6d831a'
DECLARE @DriverId2 UNIQUEIDENTIFIER = '6911b09b-177c-46c5-9f23-b16c987e202b'    -- Added a second driver

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
( @PassengerId1, 'jameskinley24+passenger1@gmail.com', 'James', 'Test', 1),
( @PassengerId2, 'jameskinley24+passenger2@gmail.com', 'Alice', 'Test', 1),  -- Added second passenger
( @DriverId1, 'jameskinley24+driver1@gmail.com', 'Senor', 'Test', 1),
( @DriverId2, 'jameskinley24+driver2@gmail.com', 'Bob', 'Test', 1)      -- Added second driver

-- Declare Journey IDs
DECLARE @OnetimeId1 UNIQUEIDENTIFIER = '1025c943-62f2-4692-885c-4e064f7f486b'
DECLARE @OnetimeId2 UNIQUEIDENTIFIER = 'c1c2d3d4-e5e6-47a8-b9b0-c2c3d4d5e6e7'  -- Added a second one-time journey
DECLARE @CommuterId1 UNIQUEIDENTIFIER = '094d53f9-5f3b-4de8-af7d-89972d31e2af'
DECLARE @CommuterId2 UNIQUEIDENTIFIER = 'd1d2e3e4-f5f6-48b9-a0a1-e2e3f4f5f6f7'  -- Added a second commuter journey

-- Declare Location Variables
DECLARE @StartLat1 FLOAT = 53.8129997253418
DECLARE @StartLong1 FLOAT = -1.5748614072799683
DECLARE @StartName1 NVARCHAR(MAX) = '189 Cardigan Lane, Hyde Park, Leeds LS6 1DX, England'

DECLARE @EndLat1 FLOAT = 53.80797576904297
DECLARE @EndLong1 FLOAT = -1.5533339977264404
DECLARE @EndName1 NVARCHAR(MAX) = 'University of, Sir William Henry Bragg Building, Woodhouse Ln, Leeds LS2 9JT'

DECLARE @StartLat2 FLOAT = 53.4000000000000
DECLARE @StartLong2 FLOAT = -2.9000000000000
DECLARE @StartName2 NVARCHAR(MAX) = 'Liverpool Lime Street Station'

DECLARE @EndLat2 FLOAT = 53.4080000000000
DECLARE @EndLong2 FLOAT = -2.9910000000000
DECLARE @EndName2 NVARCHAR(MAX) = 'Anfield Stadium, Liverpool'

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
( @OnetimeId1, @DriverId1, 11.99, @StartName1, @StartLong1, @StartLat1, @EndName1, @EndLong1, @EndLat1, 1, @StartDate, NULL, NULL, @StartTime, 3, 'WU60XGA'),
( @OnetimeId2, @DriverId2, 15.00, @StartName2, @StartLong2, @StartLat2, @EndName2, @EndLong2, @EndLat2, 1, @StartDate, NULL, NULL, '14:00:00', 2, 'XYZ123'), -- Added a second one-time journey with different details
( @CommuterId1, @DriverId1, 15.99, @StartName1, @StartLong1, @StartLat1, @EndName1, @EndLong1, @EndLat1, 2, @StartDate, @RepeatUntil, '*/1 * * * *', @StartTime, 3, 'WU60XGA'),
( @CommuterId2, @DriverId2, 12.50, @StartName2, @StartLong2, @StartLat2, @EndName2, @EndLong2, @EndLat2, 2, '2025-03-22', @RepeatUntil, '*/1 * * * *', '09:00:00', 3, 'ABC456')  -- Added a second commuter journey with different details

-- New alternate location variables with slightly different values:
DECLARE @AltStartLat FLOAT = 53.8135000000000,
        @AltStartLong FLOAT = -1.5750000000000,
        @AltStartName NVARCHAR(MAX) = 'New Location',
        @AltEndLat FLOAT = 53.8085000000000,
        @AltEndLong FLOAT = -1.5540000000000,
        @AltEndName NVARCHAR(MAX) = 'New End Location';

-------------------------------
-- Bookings for Week 1 (March 16th - 22nd)
-------------------------------
-- Booking 1 - OneTime journey for Passenger 1
DECLARE @BookingId1 UNIQUEIDENTIFIER;
DECLARE @NewBooking1 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking1
VALUES
        (@PassengerId1, @OnetimeId1, 1, 0.10, '2025-03-17 12:00:00', 0); -- Monday
SELECT @BookingId1 = BookingId FROM @NewBooking1;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId1, 12.50, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

-- Booking 2 - Commuter journey for Passenger 2
DECLARE @BookingId2 UNIQUEIDENTIFIER;
DECLARE @NewBooking2 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking2
VALUES
        (@PassengerId2, @CommuterId1, 2, 0.0875, '2025-03-18 09:00:00', 0); -- Tuesday
SELECT @BookingId2 = BookingId FROM @NewBooking2;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId2, 9.00, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

--  Additional bookings for Week 1
-- Booking 7 - OneTime journey for Passenger 1
DECLARE @BookingId7 UNIQUEIDENTIFIER;
DECLARE @NewBooking7 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking7
VALUES
        (@PassengerId1, @OnetimeId2, 1, 0.10, '2025-03-19 15:00:00', 0); -- Wednesday
SELECT @BookingId7 = BookingId FROM @NewBooking7;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId7, 11.00, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

-------------------------------
-- Bookings for Week 2 (March 23rd - 29th)
-------------------------------
-- Booking 3 - OneTime journey for Passenger 2
DECLARE @BookingId3 UNIQUEIDENTIFIER;
DECLARE @NewBooking3 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking3
VALUES
        (@PassengerId2, @OnetimeId1, 1, 0.10, '2025-03-24 14:00:00', 0); -- Monday
SELECT @BookingId3 = BookingId FROM @NewBooking3;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId3, 12.50, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

-- Booking 4 - Commuter journey for Passenger 1
DECLARE @BookingId4 UNIQUEIDENTIFIER;
DECLARE @NewBooking4 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking4
VALUES
        (@PassengerId1, @CommuterId2, 2, 0.0875, '2025-03-26 11:00:00', 0); -- Wednesday
SELECT @BookingId4 = BookingId FROM @NewBooking4;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId4, 9.00, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

-- Additional bookings for Week 2
-- Booking 8 - OneTime journey for Passenger 2
DECLARE @BookingId8 UNIQUEIDENTIFIER;
DECLARE @NewBooking8 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking8
VALUES
        (@PassengerId2, @OnetimeId2, 1, 0.10, '2025-03-27 16:00:00', 0); -- Thursday
SELECT @BookingId8 = BookingId FROM @NewBooking8;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId8, 11.50, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

-------------------------------
-- Bookings for Week 3 (March 30th - April 5th)
-------------------------------
-- Booking 5 - OneTime journey for Driver 1
DECLARE @BookingId5 UNIQUEIDENTIFIER;
DECLARE @NewBooking5 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking5
VALUES
        (@DriverId1, @OnetimeId1, 3, 0.1125, '2025-04-01 16:00:00', 1); -- Tuesday
SELECT @BookingId5 = BookingId FROM @NewBooking5;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId5, 13.00, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 1, 0);

-- Booking 9 - Commuter journey for Passenger 2
DECLARE @BookingId9 UNIQUEIDENTIFIER;
DECLARE @NewBooking9 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking9
VALUES
        (@PassengerId2, @CommuterId1, 2, 0.0875, '2025-04-03 10:00:00', 0); -- Thursday
SELECT @BookingId9 = BookingId FROM @NewBooking9;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId9, 10.00, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

--------------------------------
-- Bookings for Week 4 (April 6th - 12th)
--------------------------------
-- Booking 6 - Commuter journey for Passenger 1
DECLARE @BookingId6 UNIQUEIDENTIFIER;
DECLARE @NewBooking6 TABLE (BookingId UNIQUEIDENTIFIER);
INSERT INTO [booking].[Booking]
        (UserId, JourneyId, BookingStatusId, FeeMargin, RideTime, DriverApproval)
OUTPUT INSERTED.BookingId INTO @NewBooking6
VALUES
        (@PassengerId1, @CommuterId2, 2, 0.0875, '2025-04-07 10:00:00', 0); -- Tuesday
SELECT @BookingId6 = BookingId FROM @NewBooking6;
INSERT INTO [booking].[BookingAmmendment]
        (BookingId, ProposedPrice, StartName, StartLong, StartLat,
         EndName, EndLong, EndLat, StartTime, CancellationRequest, DriverApproval, PassengerApproval)
VALUES
        (@BookingId6, 9.00, @AltStartName, @AltStartLong, @AltStartLat,
         @AltEndName, @AltEndLong, @AltEndLat, GETDATE(), 0, 0, 1);

-- Booking 10

SELECT * FROM [identity].[User]
SELECT * FROM [journey].[Journey]
SELECT * FROM [booking].[Booking]
SELECT * FROM [booking].[BookingAmmendment]