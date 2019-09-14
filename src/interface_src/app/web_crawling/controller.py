from .database import * #run from run.py add dot
from .crawler import *
from datetime import datetime
import pandas as pd

class Controller:
    _db = None    
    _last_update_time = datetime.now()
    _current_date = _last_update_time.strftime("%A, %d %B %Y")

    _newsfeed = None
    _latest_newsfeed = pd.DataFrame()
    _top_newsfeed = pd.DataFrame()
    _top_news = 0
    
    def __init__(self, driver, server, db_name, user, pwd, top_news):
        self._db = Database(driver, server, db_name, user, pwd)
        self._top_news = top_news
        self.updateNews(top_news)
        
    def crawlXML(self, path):   
        if self._db.getConnection():
            crawler = NytimesCrawler(path)      
            df1 = crawler.crawlData()
            self._db.bulkInsert("News", df1)
            return True
        return False
    
    def getData(self, tableName):
        df = pd.DataFrame()        
        if self._db.getConnection():
            df = self._db.bulkSelect(tableName)
        return df
    
    def updateNews(self, top_news = None):
        if not top_news:
            top_news = self._top_news
        self._newsfeed = self.getData("News")
        if not self._newsfeed.empty:
            self._newsfeed = self._newsfeed.sort_values(by=['pubDate'], ascending=False)
            self._top_newsfeed = self._newsfeed.head(top_news)
            self._latest_newsfeed = self._newsfeed.head(top_news)
            print('Newsfeed updated')
        return
    
    def rateNews(self, newsid, rating, ip_addr):
        if self._db.getConnection():
            self._db.InsertOrUpdate("Ratings", 
                                                    {'date_rated': datetime.now(),
                                                    'newsid': newsid, 
                                                     'rating': rating,
                                                     'ip_addr':ip_addr}, 
                                                    {'ip_addr':ip_addr,
                                                     'newsid': newsid}
                                                )
        return 

    def verifyRefreshInterface(self, update_time_interval):    
        diff = datetime.now() - self._last_update_time
        if  (diff.total_seconds() > update_time_interval):
            self.updateNews()
    
    @property
    def newsfeed(self):
        return self._newsfeed
    @property
    def top_newsfeed(self):
        return self._top_newsfeed
    @property
    def latest_newsfeed(self):
        return self._latest_newsfeed
    @property
    def current_date(self):
        return self._current_date
    
    
    