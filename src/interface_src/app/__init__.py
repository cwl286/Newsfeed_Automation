from flask import Flask
#If start from run.py, then add dot
from .web_crawling.database import * 
from .web_crawling.crawler import *
from .web_crawling.controller import * 
from .config import Config, DevelopmentConfig, TestingConfig, ProductionConfig

#Create Flask object
app = Flask(__name__)
#Import the config class
app.config.from_object("app.config:DevelopmentConfig") 
top_news = app.config["TOP_NEWS"]
update_time_interval = app.config["UPDATE_TIME_INTERVAL"]
controller = Controller(app.config["DRIVER"], app.config["SERVER"],\
                        app.config["DB_NAME"], app.config["USER"], app.config["PWD"])


#Initialize database data from Nytimes XML
isCrawl1 = controller.crawlXML(app.config["XML1"])
isCrawl2 = controller.crawlXML(app.config["XML2"])
print("News1 is saved = ", isCrawl1)
print("News2 is saved = ", isCrawl2)


from app import views