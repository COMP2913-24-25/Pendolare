/*
Author: Alexander McCall
Created: 17/02/2025
Description: Creates User's Balance table.
*/

CREATE TABLE [payment].[UserBalance]
(
  [UserId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
  [Pending] DECIMAL(18,8) NOT NULL DEFAULT 0,
  [NonPending] DECIMAL(18,8) NOT NULL DEFAULT 0,
  [UpdatedDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

  CONSTRAINT FK_User_UserId FOREIGN KEY ([UserId]) 
  REFERENCES [identity].[User](UserId)
)
