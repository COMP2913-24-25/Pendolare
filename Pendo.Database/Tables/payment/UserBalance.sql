/*
Author: Alexander McCall
Created: 17/02/2025
Description: Creates User's Balance table.
*/

CREATE TABLE [payment].[UserBalance]
(
  [UserId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
  [Pending] FLOAT NOT NULL DEFAULT 0,
  [NonPending] FLOAT NOT NULL DEFAULT 0,
  [UpdateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

  CONSTRAINT FK_User_UserId FOREIGN KEY ([UserId]) 
  REFERENCES [identity].[User](UserId)
)
