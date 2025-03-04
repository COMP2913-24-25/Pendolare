/*
Author: James Kinley
Created: 25/02/2025
Description: Creates BookingStatus Table
*/

CREATE TABLE [booking].[BookingStatus]
(
  [BookingStatusId] INT NOT NULL PRIMARY KEY IDENTITY(1,1),
  [Status] NVARCHAR(20) NOT NULL,
  [Description] NVARCHAR(100) NULL,
  [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE()
)