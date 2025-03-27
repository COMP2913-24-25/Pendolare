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
DECLARE @PassengerId2 UNIQUEIDENTIFIER = '22967fa3-5cb3-42b4-bf88-e05a77911f06'
DECLARE @DriverId1 UNIQUEIDENTIFIER = '5800a98a-066b-45a3-8e64-a42b8a6d831a'
DECLARE @DriverId2 UNIQUEIDENTIFIER = '6911b09b-177c-46c5-9f23-b16c987e202b'

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
( @PassengerId2, 'jameskinley24+passenger2@gmail.com', 'Alice', 'Test', 1),
( @DriverId1, 'jameskinley24+driver1@gmail.com', 'Senor', 'Test', 1),
( @DriverId2, 'jameskinley24+driver2@gmail.com', 'Bob', 'Test', 1);

-- Insert Test Data for Discounts Table
INSERT INTO [payment].[Discounts] (WeeklyJourneys, DiscountPercentage)
VALUES
(1, 0.05),  -- 5% discount for 1 journey per week
(3, 0.10),  -- 10% discount for 3 journeys per week
(5, 0.15),  -- 15% discount for 5 journeys per week
(7, 0.20),  -- 20% discount for 7 journeys per week
(10, 0.25); -- 25% discount for 10 journeys per week

-- Verify Data
SELECT * FROM [payment].[Discounts];
