from flask import Flask
#If start from run.py, then add dot
from .controller.database import *
from .controller.crawler import *
from .controller.controller import Controller 
from .config import Config, DevelopmentConfig, DockerConfig, ProductionConfig

#Create Flask object
app = Flask(__name__)
#Import the config class
app.config.from_object("app.config:DockerConfig") 
if app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")
elif app.config["ENV"] == "docker":
    app.config.from_object("config.DockerConfig")


top_news = app.config["TOP_NEWS"]
update_time_interval = app.config["UPDATE_TIME_INTERVAL"]

#Initialize controller for crawling
controller = Controller(app.config["DRIVER"],\
                        app.config["SERVER"],\
                        app.config["DB_NAME"],\
                        app.config["USER"],\
                        app.config["PWD"],\
                        app.config["TOP_NEWS"]
                        )

#Initialize database data from Nytimes XML
isCrawl1 = controller.crawlXML(app.config["XML1"])
isCrawl2 = controller.crawlXML(app.config["XML2"])

#Initialize news content
controller.updateNews(top_news)

#Finally import the views.py for web interface
from app import views