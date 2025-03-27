/*
Author: James Kinley
Created: 05/02/2025
Description: Creates User Table
*/

CREATE TABLE [identity].[User]
(
  [UserId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [Email] NVARCHAR(255) UNIQUE NOT NULL,
  [FirstName] NVARCHAR(255) NULL,
  [LastName] NVARCHAR(255) NULL,
  [UserRating] FLOAT NOT NULL DEFAULT -1,
  [UserTypeId] INT NOT NULL,
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
  [UpdateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

  CONSTRAINT FK_User_UserType FOREIGN KEY ([UserTypeId]) 
  REFERENCES [identity].[UserType](UserTypeId)
);