/*
Author: Alexander McCall
Created: 17/02/2025
Description: Creates User's Balance table.
*/

CREATE TABLE [payment].[UserBalance]
(
  [BalanceId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [UserId] UNIQUEIDENTIFIER NOT NULL,
  [Pending] DECIMAL(18,8) NOT NULL DEFAULT 0,
  [NonPending] DECIMAL(18,8) NOT NULL DEFAULT 0,
  [UpdatedDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

  CONSTRAINT FK_UserBalance_UserId FOREIGN KEY ([UserId])
  REFERENCES [identity].[User](UserId)
)
