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

-- Populate Booking Statuses
MERGE INTO [booking].[BookingStatus] AS target
USING (VALUES 
    ('Pending', 'The booking has been created but not finalised.'),
    ('Confirmed', 'The booking is confirmed.'),
    ('Cancelled', 'The booking has been cancelled.')
) AS source (Status, Description)
ON target.Status = source.Status
WHEN NOT MATCHED THEN
    INSERT (Status, Description)
    VALUES (source.Status, source.Description);

GO

-- Populate Transaction Statuses
MERGE INTO [payment].[TransactionStatus] AS target
USING (VALUES 
    ('Pending', 'Transaction has been created, advertiser has recieved pending balance'),
    ('Finalised', 'Transaction price has been finalised, booking has completed'),
    ('Billed', 'Request has been sent to stripe'),
    ('Failed', 'Stripe payment has failed'),
    ('Paid', 'Complete, any balances set to non-pending')
) AS source (Status, Description)
ON target.Status = source.Status
WHEN NOT MATCHED THEN
    INSERT (Status, Description)
    VALUES (source.Status, source.Description);

GO

-- Populate Transaction Types
MERGE INTO [payment].[TransactionType] AS target
USING (VALUES 
    ('PendingAddition', 'Addition of Pending balance'),
    ('PendingSubtraction', 'Deduction of Pending balance'),
    ('NonPendingAddition', 'Addition of NonPending balance'),
    ('NonPendingSubtraction', 'Deduction of NonPending balance'),
    ('StripeSubtraction', 'A charge via stripe')
) AS source (Type, Description)
ON target.Type = source.Type
WHEN NOT MATCHED THEN
    INSERT (Type, Description)
    VALUES (source.Type, source.Description);

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

DECLARE @ManagerWhitelist NVARCHAR(MAX) = '
{
    "Whitelist": 
    [
        "jameskinley24@gmail.com",
        "sc23jk2@leeds.ac.uk",
        "mundrayj@gmail.com",
        "shayodonnell8@icloud.com"
    ]
}'

DECLARE @BookingEmailConfiguration NVARCHAR(MAX) = '
{
    "apiKey": "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",
    "fromEmail": "pendolare-dev@clsolutions.dev",
    "pendingTemplateId": "d-f8a5d7c50b4a489ca2ecdc2c333e9b57",
    "confirmedTemplateId": "d-0cd496b0ec5c4aaca9b72449dcb9d1be",
    "cancelledTemplateId": "d-fd645e276ceb4cafa14dae1d678b5b93"
}'

DECLARE @StripeConfiguration NVARCHAR(MAX) = '
{
    "secret": "sk_test_51R01XVJJfevYXm7DQZlpUnTFEirQaRSDQfy6TJZ3kBdf2oVXnjl3hV1TSzfUiiSdmuXuZoOP6tBlKsn9hJbkdha900jFkB9ZZ8",
    "publishable": "pk_test_51R01XVJJfevYXm7Da0LZSLPl85sFVvKX4ef9g0JnePgfzcdbbErjnaDs0E6CzZqUdMvpCLTkMOhYRoggxrS4WBFB00GndBkKYb"
}'

DECLARE @DvlaApiKey NVARCHAR(MAX) = 'bfehQJlOAs6trMLuOaahb4ZAS1STeM5n5yk6XvM2'

MERGE INTO [shared].[Configuration] AS target
USING (VALUES
    ('Identity.OtpConfiguration', @OtpConfiguration),
    ('Identity.JwtConfiguration', @JwtConfiguration),
    ('Identity.ManagerConfiguration', @ManagerWhitelist),
    ('Booking.DvlaApiKey', @DvlaApiKey),
    ('Booking.EmailConfiguration', @BookingEmailConfiguration),
    ('Booking.FeeMargin', '0.05'),
    ('Payment.StripeConfiguration', @StripeConfiguration)
) AS source ([Key], [Value])
ON target.[Key] = source.[Key]
WHEN NOT MATCHED THEN
    INSERT ([Key], [Value])
    VALUES (source.[Key], source.[Value])
WHEN MATCHED AND target.[Value] <> source.[Value] THEN
    UPDATE SET target.[Value] = source.[Value];

GO