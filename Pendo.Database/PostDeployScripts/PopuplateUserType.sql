/*
Author: James Kinley
Created: 05/02/2025
Description: Populates the 'UserType' table with valid values.
*/

MERGE INTO [identity].[UserType] AS target
USING (VALUES 
    ('User', 'Standard App User'),
    ('Manager', 'Able to manage all standard users and see analytics.')
) AS source (Type, Description)
ON target.Type = source.Type
WHEN NOT MATCHED THEN
    INSERT (Type, Description, CreateDate)
    VALUES (source.Type, source.Description, GETUTCDATE());