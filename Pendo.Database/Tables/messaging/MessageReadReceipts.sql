/*
Author: Josh Mundray
Created: 12/03/2025
Description: Creates Read Receipts table for messaging service.
*/

CREATE TABLE [messaging].[MessageReadReceipts]
(
    [MessageId] UNIQUEIDENTIFIER NOT NULL,
    [UserId] UNIQUEIDENTIFIER NOT NULL,
    [ReadAt] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    PRIMARY KEY ([MessageId], [UserId]),
    CONSTRAINT FK_MessageReadReceipts_Messages FOREIGN KEY ([MessageId])
        REFERENCES [messaging].[Messages](MessageId) ON DELETE CASCADE,
    CONSTRAINT FK_MessageReadReceipts_Users FOREIGN KEY ([UserId])
        REFERENCES [identity].[User](UserId)
)
