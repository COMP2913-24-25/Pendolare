/*
Author: Lara Glenn
Created: 12/03/2025
Description: Creates Discounts Table
*/

CREATE TABLE [discounts].[Discounts]
(
    [DiscountID] UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    [WeeklyJourneys]  INT NOT NULL,
    [DiscountPercentage] FLOAT NOT NULL,
    [CreateData] DATETIME2 NOT NULL DEFAULT GETUCTDATE(),

    CONSTRAINT CHECK_DiscountPercentage CHECK (DiscountPercentage >= 0 AND DiscountPercentage <= 1)
);