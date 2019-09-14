
CREATE DATABASE TestDB;
GO

USE TestDB;
GO

/* (1) Create accounts table*/
CREATE TABLE dbo.Users (
	userid int NOT NULL IDENTITY(1,1) PRIMARY KEY,
	joindate datetime NOT NULL,
	username varchar(25) NOT NULL,
	password varchar(192) NOT NULL
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
	userid int NOT NULL FOREIGN KEY REFERENCES Users(userid),
	rating int NOT NULL,
    ip_addr VARCHAR(16) NOT NULL
);
GO


/* (4) Insert admin data*/
INSERT INTO dbo.Users (joindate, username,password)
VALUES (CURRENT_TIMESTAMP,'admin',  '099ef1b4b271f2aa04d2e20b04b69acb8ab953fd5a85088ef0cc98328ab78eb39c491227e4406a2c6bb0fb0429f5638ef8f05c6b386f19b0a6ba8e3e57e2501992263763a917ac2d2d55b6403b1d4c313b53854796acc9598c4d01358cc27f31');

INSERT INTO dbo.Users (joindate, username,password)
VALUES (CURRENT_TIMESTAMP,'tester',  '5b1d0f355b876b8909f1d08972b966c725b54dbad0db7dd05f5fb7a9c94b262f3998cd8594f4d35a5a9cb8cce429323f63e623d30b1e13095506e9294c9156e6f2a068e7ebc43ae0bc7debff01e9aa7ab4649a8e126faf15ebff21ef00ee2697');

GO

