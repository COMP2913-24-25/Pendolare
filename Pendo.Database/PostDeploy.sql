/*
Author: James Kinley
Created: 05/02/2025
Description: Completes all post-deploy tasks.
*/

-- Populate User Types
MERGE INTO [identity].[UserType] AS target
USING (VALUES 
    ('User', 'Standard App User'),
    ('Manager', 'Able to manage all standard users and see analytics.')
) AS source (Type, Description)
ON target.Type = source.Type
WHEN NOT MATCHED THEN
    INSERT (Type, Description, CreateDate)
    VALUES (source.Type, source.Description, GETUTCDATE());

GO

DECLARE @OtpConfiguration NVARCHAR(MAX) = '
{
    "OtpLength": 6,
    "SendGridApiKey": "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",
    "SendGridFromEmail": "pendolare-dev@clsolutions.dev",
    "SendGridOtpTemplateId": "d-436ef8715e9e4e1caa1773204eac9434"
}';

DECLARE @JwtConfiguration NVARCHAR(MAX) = '
{
    "Issuer": "Pendo.IdentityService",
    "AppAudience": "Pendo.MobileApp",
    "ManagerAudience": "Pendo.ManagerDashboard",
    "SecretKey": "d8d5304c4624d4ee3461edde3a7df1d2a2a7aec0aaa689b7ef6ca563ae3a67bb",
    "ExpiresInMinutes": 60
}';

MERGE INTO [shared].[Configuration] AS target
USING (VALUES
    ('Identity.OtpConfiguration', @OtpConfiguration),
    ('Identity.JwtConfiguration', @JwtConfiguration)
) AS source ([Key], [Value])
ON target.[Key] = source.[Key]
WHEN NOT MATCHED THEN
    INSERT ([Key], [Value])
    VALUES (source.[Key], source.[Value])
WHEN MATCHED AND target.[Value] <> source.[Value] THEN
    UPDATE SET target.[Value] = source.[Value];

GO