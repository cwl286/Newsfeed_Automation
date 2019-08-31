#!/bin/bash
# File name: updateRate.


database=TestDB
password=Admin_password123
wait_time=2s


# Update
/opt/mssql-tools/bin/sqlcmd -S 0.0.0.0 -U sa -P $password -Q"
USE ${database};
GO
UPDATE dbo.News
SET dbo.News.total_rating = b.total_rating FROM (
	SELECT dbo.Ratings.newsid, SUM (dbo.Ratings.rating) AS total_rating
	 FROM dbo.Ratings
	GROUP BY newsid
)  AS b
INNER JOIN dbo.News as a           
	ON a.newsid = b.newsid;
GO"


