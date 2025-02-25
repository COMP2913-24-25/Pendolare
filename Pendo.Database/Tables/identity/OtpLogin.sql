/*
Author: James Kinley
Created: 11/02/2025
Description: Creates Otp Login table to keep track of user logins.
*/

CREATE TABLE [identity].[OtpLogin]
(
  [OtpLoginId] UNIQUEIDENTIFIER PRIMARY KEY NOT NULL DEFAULT NEWSEQUENTIALID(),
  [UserId] UNIQUEIDENTIFIER NOT NULL,
  [CodeHash] NVARCHAR(255) NOT NULL,
  [HashSalt] NVARCHAR(255) NOT NULL,
  [IssueDate] DATETIME2 NULL,
  [ExpiryDate] DATETIME2 NOT NULL,
  [Verified] BIT NOT NULL DEFAULT 0,

  CONSTRAINT FK_OtpLogin_User FOREIGN KEY (UserId) REFERENCES [identity].[User](UserId)
)