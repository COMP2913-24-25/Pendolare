/*
Author: James Kinley
Created: 07/02/2025
Description: Creates Transaction Status table.
*/

CREATE TABLE [payment].[TransactionStatus]
(
  [TransactionStatusId] INT NOT NULL PRIMARY KEY IDENTITY(1,1),
  [Status] NVARCHAR(50) NOT NULL UNIQUE,
  [Description] NVARCHAR(255) NULL,
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE()
)