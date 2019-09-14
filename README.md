#### Newsfeed-Automation
docker-compose, python, flask, mssql

This is a demo to use docker-compose to build up a newsfeed automation website. It is implemented by using Python Flask(web server) and MSSQL(database).

#### Folder structure 

Newsfeed<br/>
├──README.md<br/>
└──src<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──Dockerfile<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──docker-compose.yml<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──db_src<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──entrypoint.sh<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──init.sql<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──updateRate.sh<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──interface_src<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──requirements.txt<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──run.py<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──app<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──views.py<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──...<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──static<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──...<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──templates<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──...<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──web_crawling<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Europe.xml<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Technology.xml<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──...<br/>          

#### Steps to start docker-compose and try the web template

1. Go to directoary of src
2. Start Docker daemon
3. Builds images if needed, type this in the terminal:
```docker-compose up --build```
If you want to build and run containers in the background)
```docker-compose up -d```
4. To check the existence of docker image (Repository names: src_web, python, mcr.microsoft.com/mssql/server), type this in the terminal:
```docker images```
5. To check the docker container is running (Container names:src_web_1, src_db_1), type this in the terminal:
```docker ps```
6. Finally, access the web interface by default ip and port
```0.0.0.0:5000``` or ```http://localhost/```
7. Access MSSQL server by default ip and port
    ```local ip:1433```   or  ```0.0.0.0:1433```
    and ```Login: sa```   ```Password: Admin_password123```
    

#### Notes about docker 
* In case an image but not running, type this in the terminal:
    * Show all stopped containers:
        ```docker ps -a```
    * Run the stopped containers:
    ```docker start -ai <container_name>```
         
* To interact with a running container in the terminal, type this in the terminal:
    ```docker exec -it <container_name>  "bash"```
    
* To remove all stop and running containers, type this in the terminal:
    ```docker stop $(docker ps -a -q)```
    ```docker rm $(docker ps -a -q)```
    
    
####  Features about web interface 
* Imports news feeds from the resources (Europe.xml, Technology.xml)
* Displays the imported feeds from the database
* Endpoint to news articles in JSON
* Cronjob to update best-rated articles
* Registration panel to register new users, encrypt and hash the password in the database
* Login panel for non-admin users to read news articles, rate individual news articles and download in JSON
    * username: tester  ; password: tester
* Login panel for the admin user to rate individual, read news articles with arbitrary publish date intervals and download in JSON (Limited to admin user)
    * username: admin  ; password: admin
    
    
####  Main architectural and design decisions 
To achieve simplicity and objectives, Flask framework in Python and Microsoft SQL Server are used for implementation. 

Note: Docker-compose simultaneously builds up the images for database and web app. 

For database, docker-compose pulls the image of MSSQL and creates a container based on the /dc_src/entrypoint.sh. The script includes instruction to create Database with <database=TestDB> <password=Admin_password123>. Three tables will be created based on the needs for newsfeed automation. This script also generates a cron job to update the table <News> by sum up data in the table <Ratings>.

Tables:    
```
Users: userid(int) [PRIMARY KEY], joindate(datetime), username(nvarchar, password(nvarchar)\
News: newsid(int) [PRIMARY KEY], date_added(datetime), total_rating(int), category(category), creator(nvarchar), description(nvarchar), link(nvarchar), media_credit(nvarchar), media_description(nvarchar), media_url(nvarchar), pubDate(datetime), title(nvarchar)\
Ratings: rateid(int) [PRIMARY KEY], date_rated(datetime), newsid(int) [Foreign Key: News(newsid)], userid(int) [Foreign Key: Users(userid)],rating(int), ip_addr(varchar)
```
    
For web app, docker-compose will use the Dockerfile to pull python:3.7.4 image, install ODBC for mssql and install requirements.txt. It will create a new image called "src_web". When creating the container of it, its entrypoint is set to bash a script to wait for the database created. Then it will take command to run "/interface_src/run.py". 

In web app, python will crawl all news feeds from the resources (Europe.xml, Technology.xml) and store into the database first. Then it will ask the database every five minutes for data to generate the web interface. This web app will also generate JSON endpoint by this data. 

Note that the JSON endpoint in the admin panel is only available after login.

