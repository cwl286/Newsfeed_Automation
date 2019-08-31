
CREATE DATABASE TestDB;
GO

USE TestDB;
GO

/* (1) Create accounts table*/
CREATE TABLE dbo.Users (
	userid int NOT NULL IDENTITY(1,1) PRIMARY KEY,
	joindate datetime NOT NULL,
	username nvarchar(25) NOT NULL,
	password nvarchar(20) NOT NULL
);
GO

/* (2) Create News table*/
CREATE TABLE dbo.News (
	newsid int NOT NULL IDENTITY(1,1) PRIMARY KEY,
	date_added datetime NOT NULL DEFAULT (CURRENT_TIMESTAMP),
	total_rating int NOT NULL DEFAULT ('0'),    
	category nvarchar(max),
	creator nvarchar(50),
	description nvarchar(max),
	link nvarchar(max),
	media_credit nvarchar(max),
	media_description nvarchar(max),
	media_url nvarchar(max),
	pubDate datetime,
	title nvarchar(max),
);
GO
/* (3) Create Ratings table*/
CREATE TABLE dbo.Ratings (
	rateid int NOT NULL IDENTITY(1,1) PRIMARY KEY, 
	date_rated datetime NOT NULL DEFAULT (CURRENT_TIMESTAMP),
	newsid int NOT NULL FOREIGN KEY REFERENCES News(newsid),
	rating int NOT NULL,
    ip_addr VARCHAR(16) NOT NULL
);
GO


/* (4) Insert Tesing data*/
INSERT INTO dbo.Users (joindate, username,password)
VALUES (CURRENT_TIMESTAMP,'admin',  'admin');
INSERT INTO dbo.Users (joindate, username,password)
VALUES (CURRENT_TIMESTAMP,'tester1', 'tester1');
INSERT INTO dbo.Users (joindate, username,password)
VALUES (CURRENT_TIMESTAMP,'tester2', 'tester2');
INSERT INTO dbo.Users (joindate, username,password)
VALUES (CURRENT_TIMESTAMP,'t', 't');
GO

