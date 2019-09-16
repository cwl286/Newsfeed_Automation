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
            conn_str = f"DRIVER={self._driver};SERVER={self._server};DATABASE={self._db_name};UID={self._user};PWD={self._pwd}"
            self._cnxn = pyodbc.connect(conn_str)
        except Exception as e:
            print("Could not connect to database")
            print(e)        
            return False
        return True
    
    def bulkSelect(self, table_name, equal_conditions = None): 
        #args: string, dict
        #return dataframe
        df = pd.DataFrame()      
        if not self._cnxn:
            return df          
        try:
            if equal_conditions:
                clauses = [ str(k) + f"={'?'}" for k, v in zip(list(equal_conditions.keys()), list(equal_conditions.values()))]
                args = tuple(equal_conditions.values())
                query = f"""
                            SELECT * FROM dbo.{table_name} where { " and ".join(c for c in clauses)}
                            """
                df = pd.read_sql(sql=query, con=self._cnxn, params=args)
            else:
                query = f"""
                            SELECT * FROM dbo.{table_name}
                            """
                df = pd.read_sql(sql=query, con=self._cnxn)
                
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
            query = f"""
                        INSERT INTO dbo.{table_name} ({','.join(headers)})
                        values({'?' + ',?' * (len(headers) - 1)})
                         """
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
        if not self._cnxn:
            return False
        try:     
            if conditions:                
                #Update statement
                query = query + \
                        f"""UPDATE dbo.{table_name} set {'=?,'.join(data.keys())}=? WHERE {'=? and '.join(conditions.keys())}=?
                        IF @@ROWCOUNT=0 """                       
                args = args + list(data.values()) + list(conditions.values())                
            #Insert statement        
            query = query + \
                    f""" 
                    INSERT INTO dbo.{table_name} ({','.join(data.keys())})
                    values({'?' + ',?' * (len(data.keys()) - 1)});
                    """
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
        
        