-- Test Data Setup Script

DELETE FROM [payment].[UserBalance]
DELETE FROM [identity].[User]

DECLARE @PassengerId UNIQUEIDENTIFIER = '11856ed2-e4b2-41a3-aae7-de4966800e95'
DECLARE @DriverId UNIQUEIDENTIFIER = '5800a98a-066b-45a3-8e64-a42b8a6d831a'

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
( @DriverId, 'jameskinley24+driver@gmail.com', 'Señor', 'Pendo', 1)