/*
Author: James Kinley
Created: 07/02/2025
Description: Creates shared Configuration table.
*/

CREATE TABLE [shared].[Configuration]
(
  [ConfigurationId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
  [Key] NVARCHAR(100) NOT NULL UNIQUE,
  [Value] NVARCHAR(MAX) NOT NULL,
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
  [UpdateDate] DATETIME2 NOT NULL default GETUTCDATE()
)