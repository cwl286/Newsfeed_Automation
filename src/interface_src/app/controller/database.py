import pandas as pd
import sqlalchemy as db
import pyodbc
import urllib

class Database:
    _cnxn = None
    _driver = ''
    _server = ''
    _db_name = ''
    _user = ''
    _pwd = ''
    
    def __init__(self, driver, server, db_name, user, pwd):
        self._driver = driver
        self._server = server
        self._db_name = db_name
        self._user = user
        self._pwd = pwd
        
            
    def getConnection(self):
        #drivers = [item for item in pyodbc.drivers()]    
        try:
            conn_str = f'DRIVER={self._driver};SERVER={self._server};DATABASE={self._db_name};UID={self._user};PWD={self._pwd}'
            self._cnxn = pyodbc.connect(conn_str)
        except Exception as e:
            print("Could not connect to database")
            print(e)        
            return False
        return True
    
    def bulkSelect(self, table_name): 
        #args: string
        #return dataframe
        df = pd.DataFrame()      
        if not self._cnxn:
            return df          
        try:
            query = f"SELECT * FROM dbo.{table_name}"
            df = pd.read_sql(query, self._cnxn)
            return df   
        except Exception as e:
            print("Could not select a table from database")
            print(e)
        return df
            
    def bulkInsert(self, table_name, df):    
        #args: string, dataframe
        cursor = None
        if not self._cnxn:
            return False          
        try:
            headers = list(df)            
            query = f"INSERT INTO dbo.{table_name} ({','.join(headers)})" +\
                    f"values({'?' + ',?' * (len(headers) - 1)})"    
            cursor = self._cnxn.cursor()
            for index,row in df.iterrows():
                args = tuple(row)
                cursor.execute(query, args)
        except Exception as e:
            print("Could not insert to database")
            print(e)
            return False
        finally:
            cursor.commit()
            cursor.close()
            return True
            
    def InsertOrUpdate(self, table_name, data, conditions):
        #args: string, dict, dict
        '''        
        update Ratings set rating='2' where ip_addr =  '0.0.0.1'
        IF @@ROWCOUNT=0
           insert into Ratings values (CURRENT_TIMESTAMP,1, 1, '0.0.0.1');
        '''
        query = ""
        args = []
        cursor = None
        if not self.cnxn:
            return False
        try:     
            if conditions:                
                conditions_keys = list(conditions.keys())
                my_dict = [ str(k) + "=" + str(v) for k, v in zip(list(data.keys()), list(data.values()))]
                query = query + f"UPDATE dbo.{table_name} set {'=?,'.join(data.keys())}=? WHERE " +\
                        f" {'=? and '.join(conditions.keys())}=?"  +\
                        f" IF @@ROWCOUNT=0 "                          
                args = args + list(data.values()) + list(conditions.values())                        
            query = query + f" INSERT INTO dbo.{table_name} ({','.join(data.keys())})" +\
                    f" values({'?' + ',?' * (len(data.keys()) - 1)});"     
            args = args + list(data.values())
            cursor = self._cnxn.cursor()
            cursor.execute(query, args)
        except Exception as e:
            print("Could not insert to database")
            print(e)
            return False
        finally:
            cursor.commit()
            cursor.close()
            return True
        return False

    def closeConnection(self):        
        self._cnxn.close()
        
        
class ORM_database:
    _engine = None
    _driver = ''
    _server = ''
    _db_name = ''
    _user = ''
    _pwd = ''
    
    def __init__(self, driver, server, db_name, user, pwd):
        self._driver = driver
        self._server = server
        self._db_name = db_name
        self._user = user
        self._pwd = pwd
            
    def createEngine(self):
        #drivers = [item for item in pyodbc.drivers()]    
        try:
            conn_str = f'DRIVER={self._driver};SERVER={self._server};DATABASE={self._db_name};UID={self._user};PWD={self._pwd}'
            params = urllib.parse.quote_plus(conn_str)
            self._engine = db.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        except Exception as e:
            print("Could not create engine")
            print(e)        
            return False
        return True
    
    def querying(self, table_name):
        #args: string
        #return dataframe
        df = pd.DataFrame()      
        if not self._engine:
            return df          
        try:
            conn = self._engine.connect()
            metadata = db.MetaData()
            table = db.Table(table_name, metadata, autoload=True, autoload_with=self._engine)
            query = db.select([table])
            ResultProxy = conn.execute(query)
            ResultSet = ResultProxy.fetchall()
            #Convert results to dataframe
            df = pd.DataFrame(ResultSet)
            df.columns = ResultSet[0].keys()
            
            ResultProxy.close()
            conn.close()
            return df   
        except Exception as e:
            print("Could not select a table from database")
            print(e)
        return df
    
    def closeConnection(self):        
            self._engine.dispose()
     