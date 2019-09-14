import pandas as pd
import pyodbc

class Database:
    cnxn = None
    driver = ''
    server = ''
    db = ''
    user = ''
    pwd = ''
    
    def __init__(self, driver, server, db, user, pwd):
        self.driver = driver
        self.server = server
        self.db = db
        self.user = user
        self.pwd = pwd
            
    def getConnection(self):
        #drivers = [item for item in pyodbc.drivers()]    
        try:
            conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.db};UID={self.user};PWD={self.pwd}'
            self.cnxn = pyodbc.connect(conn_str)
        except Exception as e:
            print("Could not connect to database")
            print(e)        
            return False
        return True
    
    def bulkSelect(self, table_name): 
        #args: string
        #return dataframe
        df = pd.DataFrame()      
        if not self.cnxn:
            return df          
        try:
            query = f"SELECT * FROM dbo.{table_name}"
            df = pd.read_sql(query, self.cnxn)
            return df   
        except Exception as e:
            print("Could not select a table from database")
            print(e)
        return df
            
    def bulkInsert(self, table_name, df):    
        #args: string, dataframe
        cursor = None
        try:
            headers = list(df)            
            query = f"INSERT INTO dbo.{table_name} ({','.join(headers)})" +\
                    f"values({'?' + ',?' * (len(headers) - 1)})"    
            cursor = self.cnxn.cursor()
            for index,row in df.iterrows():
                args = tuple(row)
                cursor.execute(query, args)
        except Exception as e:
            print("Could not insert to database")
            print(e)
        finally:
            cursor.commit()
            cursor.close()
            print(table_name + ' is saved.')
            
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
            cursor = self.cnxn.cursor()
            cursor.execute(query, args)
        except Exception as e:
            print("Could not insert to database")
            print(e)
        finally:
            cursor.commit()
            cursor.close()
        return

    def close(self):        
        self.cnxn.close()
