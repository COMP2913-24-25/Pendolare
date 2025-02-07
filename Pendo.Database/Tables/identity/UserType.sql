/*
Author: James Kinley
Created: 05/02/2025
Description: Creates UserType Table
*/

CREATE TABLE [identity].[UserType]
(
  [UserTypeId] INT NOT NULL PRIMARY KEY IDENTITY(1,1),
  [Type] NVARCHAR(20) NOT NULL,
  [Description] NVARCHAR(100) NULL,
  [CreateDate] DATETIME2 NOT NULL
)