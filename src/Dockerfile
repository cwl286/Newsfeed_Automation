#Download Python
FROM python:3.7.4
  
WORKDIR /code

#nstall cron and curl — 
RUN     apt-get update && apt-get install -y cron curl && apt-get clean && apt-get install nano && apt-get install -y netcat


# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get -y install msodbcsql17
RUN apt-get -y install unixodbc unixodbc-dev

#Create directory and copy code
ADD interface_src /code
RUN pip3 install -r requirements.txt


#Exec form of ENTRYPOINT allows you to set commands and parameters
ENTRYPOINT ["/bin/bash"]

#You can also set CMD default command which will be executed when running container without specifying a command. 
#CMD python3 run.py

