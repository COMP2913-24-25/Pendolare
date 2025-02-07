/*
Author: James Kinley
Created: 05/02/2025
Description: Creates all additional indexes not defined in the table definitions.
*/

CREATE NONCLUSTERED INDEX IX_User_UserType ON [identity].[User]([UserTypeId]);