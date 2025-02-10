/*
Author: James Kinley
Created: 05/02/2025
Description: Creates all necessary schema, representing individual microservice domains.
TESTING
*/

-- For shared tables, for instance configuration, API credentials.
CREATE SCHEMA [shared]
GO

-- Identity Service
CREATE SCHEMA [identity]
GO

-- Journey Service
CREATE SCHEMA [journey]
GO

-- Booking Service
CREATE SCHEMA [booking]
GO

-- Payment Service
CREATE SCHEMA [payment]
GO

-- Messaging Service
CREATE SCHEMA [messaging]
GO
