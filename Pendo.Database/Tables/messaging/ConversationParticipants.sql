/*
Author: Josh Mundray
Created: 12/03/2025
Description: Creates Conversation Participants table for messaging service.
*/

CREATE TABLE [messaging].[ConversationParticipants]
(
    [ConversationId] UNIQUEIDENTIFIER NOT NULL,
    [UserId] UNIQUEIDENTIFIER NOT NULL,
    [JoinedAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    [LeftAt] DATETIME2 NULL,
    PRIMARY KEY ([ConversationId], [UserId]),
    CONSTRAINT FK_ConversationParticipants_Conversations FOREIGN KEY ([ConversationId])
        REFERENCES [messaging].[Conversations](ConversationId) ON DELETE CASCADE,
    CONSTRAINT FK_ConversationParticipants_Users FOREIGN KEY ([UserId])
        REFERENCES [identity].[User](UserId)
)
