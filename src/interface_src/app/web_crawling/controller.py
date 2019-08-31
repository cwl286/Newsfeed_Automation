from .database import * #run from run.py add dot
from .crawler import *


class Controller:
    db = None    
    def __init__(self, driver, server, db, user, pwd):
        self.db = Database(driver, server, db, user, pwd)
        
    def crawlXML(self, path):   
        if self.db.getConnection():
            crawler = NytimesCrawler(path)      
            df1 = crawler.crawlData()
            self.db.bulkInsert("News", df1)
            return True
        return False
    
    def getData(self, tableName):
        df = pd.DataFrame()        
        if self.db.getConnection():
            df = self.db.bulkSelect(tableName)
        return df
    
    def rateNews(self, newsid, rating, ip_addr):
        if self.db.getConnection():
            df = self.db.InsertUpdate("Ratings", 
                                        {'date_rated':datetime.datetime.now(),
                                        'newsid': newsid, 
                                         'rating': rating,
                                         'ip_addr':ip_addr}, 
                                        {'ip_addr':ip_addr,
                                         'newsid': newsid}
                                      )        
        return 
    
if False:
    newsid = 5
    rating = 1
    ip_addr = '0.0.0.0'
    driver = '{ODBC Driver 17 for SQL Server}'
    server = '127.0.0.1,1433'
    db = 'TestDB'
    user = 'sa'
    pwd = 'Admin_password123'
    conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};\
        SERVER=127.0.0.1,1433;\
        DATABASE=TestDB;\
        UID=sa;\
        PWD=Admin_password123'
    top_news = 5
    update_time_interval = 3000
    controller = Controller(driver, server, db, user, pwd)
    controller.rateNews(newsid, rating, ip_addr)
    
    
    
    