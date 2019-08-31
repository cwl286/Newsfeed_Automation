from flask import Flask
import os,  secrets
from .web_crawling.database import * #run from run.py add dot
from .web_crawling.crawler import * #run from run.py add dot
from .web_crawling.controller import * #run from run.py add dot

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#Initial all the newsfeed from the source
current_dir = os.path.dirname(os.path.realpath(__file__))
xml1 = current_dir + "/web_crawling/Technology.xml"
xml2 = current_dir + "/web_crawling/Europe.xml"
driver = '{ODBC Driver 17 for SQL Server}'
#CONTAINER_NAME, CONTAINER_PORT
server = 'db,1433'
db = 'TestDB'
user = 'sa'
pwd = 'Admin_password123'
'''
#Connection string for sql server
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};\
    SERVER=127.0.0.1,1433;\
    DATABASE=TestDB;\
    UID=sa;\
    PWD=Admin_password123'
'''
top_news = 5
update_time_interval = 3000
controller = Controller(driver, server, db, user, pwd)

#Initialize database data from Nytimes XML
isCrawl1 = controller.crawlXML(xml1)
isCrawl2 = controller.crawlXML(xml2)
print("News1 is saved = ", isCrawl1)
print("News2 is saved = ", isCrawl2)


from app import views