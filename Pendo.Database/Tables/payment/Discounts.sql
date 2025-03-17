/*
Author: Lara Glenn
Created: 12/03/2025
Description: Creates Discounts Table
*/

CREATE TABLE [payment].[Discounts]
(
    [DiscountID] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    [WeeklyJourneys]  INT NOT NULL,
    [DiscountPercentage] FLOAT NOT NULL,
    [CreateDate] DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    CONSTRAINT CHECK_DiscountPercentage CHECK (DiscountPercentage >= 0 AND DiscountPercentage <= 1)
);