/*
Author: Josh Mundray
Created: 12/03/2025
Description: Creates Messages table for messaging service.
*/

CREATE TABLE [messaging].[Messages]
(
    [MessageId] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    [ConversationId] UNIQUEIDENTIFIER NOT NULL,
    [SenderId] UNIQUEIDENTIFIER NOT NULL,
    [MessageType] NVARCHAR(50) NOT NULL,
    [Content] NVARCHAR(MAX) NOT NULL,
    [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    [EditedAt] DATETIME2 NULL,
    [IsDeleted] BIT NOT NULL DEFAULT 0,
    CONSTRAINT FK_Messages_Conversations FOREIGN KEY ([ConversationId])
        REFERENCES [messaging].[Conversations](ConversationId) ON DELETE CASCADE,
    CONSTRAINT FK_Messages_Sender FOREIGN KEY ([SenderId])
        REFERENCES [identity].[User](UserId)
)
