/*
Author: James Kinley
Created: 05/02/2025
Description: Creates all additional indexes not defined in the table definitions.
*/

CREATE NONCLUSTERED INDEX IX_User_UserType ON [identity].[User]([UserTypeId]);

GO;

CREATE INDEX IX_OtpLogin_UserId ON [identity].[OtpLogin] (UserId)

GO;

-- Messaging Service Indexes
CREATE INDEX IX_Messages_ConversationId ON [messaging].[Messages]([ConversationId]);

GO;

CREATE INDEX IX_Messages_SenderId ON [messaging].[Messages]([SenderId]);

GO;

CREATE INDEX IX_ConversationParticipants_UserId ON [messaging].[ConversationParticipants]([UserId]);

GO;