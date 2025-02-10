/*
Author: James Kinley
Created: 05/02/2025
Description: Creates API Client table to store api credentials.
*/

CREATE TABLE [shared].[ApiClient]
(
  [ApiClientId] INT NOT NULL PRIMARY KEY IDENTITY(1,1),
  [ApiName] NVARCHAR(255) UNIQUE NOT NULL,
  [ClientId] NVARCHAR(255) NULL,
  [ClientSecret] NVARCHAR(255) NOT NULL,
  [IsActive] BIT NOT NULL DEFAULT 1,
  [CreateDate] DATETIME2 DEFAULT GETUTCDATE(),
  [UpdateDate] DATETIME2 DEFAULT GETUTCDATE(),
)