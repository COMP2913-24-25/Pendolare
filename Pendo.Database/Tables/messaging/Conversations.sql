/*
Author: Josh Mundray
Created: 12/03/2025
Description: Creates Messages table for messaging service.
*/

CREATE TABLE [messaging].[Conversations]
(
    [ConversationId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    [Name] NVARCHAR(100) NULL,
    [Type] NVARCHAR(20) NOT NULL CHECK (Type IN ('direct', 'group', 'support')),
    [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    [UpdateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE()
)
