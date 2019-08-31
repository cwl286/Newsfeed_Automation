#!/bin/bash

apt-get update && apt-get install -y cron curl && apt-get clean && apt-get install nano

database=TestDB
password=Admin_password123
wait_time=2s

# wait for SQL Server to come up
echo importing data will start in $wait_time...
sleep $wait_time
echo importing data...

# run the init script to create the DB and the tables in /table
/opt/mssql-tools/bin/sqlcmd -S 0.0.0.0 -U sa -P $password -i ./init.sql

#Example
#/opt/mssql-tools/bin/sqlcmd -S 0.0.0.0 -U sa -P Admin_password123

#Add crontab to update every 5 minutes by sql
echo "*/1 * * * *  /bin/bash /usr/src/app/updateRate.sh" | crontab -

#Start crontab
echo "service cron start"  | bash -