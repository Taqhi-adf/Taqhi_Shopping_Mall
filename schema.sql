IF DB_ID(N'TaqhiShoppingMall') IS NULL
    CREATE DATABASE TaqhiShoppingMall;
GO

USE TaqhiShoppingMall;
GO

IF OBJECT_ID('dbo.TransportAssessments', 'U') IS NOT NULL DROP TABLE dbo.TransportAssessments;
IF OBJECT_ID('dbo.WeatherObservations', 'U') IS NOT NULL DROP TABLE dbo.WeatherObservations;
IF OBJECT_ID('dbo.AuditLogs', 'U') IS NOT NULL DROP TABLE dbo.AuditLogs;
IF OBJECT_ID('dbo.Products', 'U') IS NOT NULL DROP TABLE dbo.Products;
GO

CREATE TABLE dbo.Products (
    ProductID NVARCHAR(30) PRIMARY KEY,
    SKU NVARCHAR(50) NOT NULL,
    ProductName NVARCHAR(200) NOT NULL,
    Category NVARCHAR(100) NOT NULL,
    SubCategory NVARCHAR(100) NULL,
    Description NVARCHAR(1000) NULL,
    Perishable BIT NOT NULL DEFAULT 0,
    Hazardous BIT NOT NULL DEFAULT 0,
    ShelfLifeDays INT NULL,
    ManufactureDate DATE NULL,
    ExpiryDate DATE NULL,
    MinTempC FLOAT NULL,
    MaxTempC FLOAT NULL,
    MaxRelativeHumidity FLOAT NULL,
    MinPressureHpa FLOAT NULL,
    MaxPressureHpa FLOAT NULL,
    LightSensitive BIT NOT NULL DEFAULT 0,
    FreezeSensitive BIT NOT NULL DEFAULT 0,
    PackagingRequirement NVARCHAR(500) NULL,
    HandlingRequirement NVARCHAR(500) NULL,
    SourceNote NVARCHAR(500) NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.WeatherObservations (
    ObservationID BIGINT IDENTITY PRIMARY KEY,
    LocationName NVARCHAR(200),
    Latitude FLOAT,
    Longitude FLOAT,
    ObservationTime DATETIME2,
    TemperatureC FLOAT,
    RelativeHumidity FLOAT,
    SurfacePressureHpa FLOAT,
    WindSpeedKmh FLOAT,
    PrecipitationMm FLOAT,
    WeatherCode INT,
    Provider NVARCHAR(100),
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE dbo.TransportAssessments (
    AssessmentID BIGINT IDENTITY PRIMARY KEY,
    ProductID NVARCHAR(30) NOT NULL,
    ObservationID BIGINT NULL,
    ExpiryOK BIT NOT NULL,
    TemperatureOK BIT NULL,
    HumidityOK BIT NULL,
    PressureOK BIT NULL,
    RiskLevel NVARCHAR(30) NOT NULL,
    Status NVARCHAR(50) NOT NULL,
    Reason NVARCHAR(2000),
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_Assessment_Product FOREIGN KEY(ProductID) REFERENCES dbo.Products(ProductID),
    CONSTRAINT FK_Assessment_Weather FOREIGN KEY(ObservationID) REFERENCES dbo.WeatherObservations(ObservationID)
);

CREATE TABLE dbo.AuditLogs (
    AuditID BIGINT IDENTITY PRIMARY KEY,
    EventType NVARCHAR(100),
    Question NVARCHAR(2000),
    ResultSummary NVARCHAR(4000),
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
