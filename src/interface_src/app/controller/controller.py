from .database import * #run from run.py add dot
from .crawler import *
from .encryption import Encryption
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
    encryption = Encryption()
    
    def __init__(self, driver, server, db_name, user, pwd, top_news):
        self._db = Database(driver, server, db_name, user, pwd)
        self._top_news = top_news
        
    def crawlXML(self, path):   
        if self._db.getConnection():
            crawler = NytimesCrawler(path)      
            df1 = crawler.crawlData()
            self._db.bulkInsert("News", df1)
            print("News is saved:  ", path)
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
    
    def rateNews(self, newsid, rating, userid, ip_addr):
        if self._db.getConnection():
            self._db.InsertOrUpdate("Ratings", 
                                                    {'date_rated': datetime.now(),
                                                    'newsid': newsid, 
                                                    'userid': userid, 
                                                     'rating': rating,
                                                     'ip_addr':ip_addr}, 
                                                    {'userid':userid,
                                                     'newsid': newsid}
                                                )
        return 

    def verifyRefreshInterface(self, update_time_interval):    
        diff = datetime.now() - self._last_update_time
        if  (diff.total_seconds() > update_time_interval):
            self.updateNews()
            
    def verifyLogin(self, usr, pwd):
        users_df = self.getData("Users")
        if not users_df.empty:
            user_df = users_df[( users_df["username"] == usr)]
            if len(user_df.index) > 0:
                stored_password = user_df.iloc[0]['password']
                if(self.encryption.verify_password(stored_password, pwd)):
                    return str(user_df.iloc[0]['userid'])
        return None
    
    def saveNewAccount(self, usr, pwd):
        users_df = self.getData("Users")
        user_df = users_df[( users_df["username"] == usr)]
        result = False
        if len(user_df.index) == 0:
            hash_password = self.encryption.hash_password(pwd)
            if self._db.getConnection():
                result =  self._db.InsertOrUpdate("Users", 
                                                                        {'username': usr,
                                                                        'password': hash_password,
                                                                        'joindate': datetime.now()
                                                                         }, 
                                                                        {'username':usr
                                                                         }
                                                                    )
        return result
    
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
    

    
    