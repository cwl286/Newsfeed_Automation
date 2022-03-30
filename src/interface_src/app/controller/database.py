import pandas as pd
import pyodbc
import datetime as datetime


class Database:
    '''
    pyodbc method
    '''
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
        isSuccess = True
        try:
            conn_str = f"DRIVER={self._driver};SERVER={self._server};DATABASE={self._db_name};UID={self._user};PWD={self._pwd}"
            self._cnxn = pyodbc.connect(conn_str)
        except Exception as e:
            print("Could not connect to database")
            print(e)       
            isSuccess = False
        return isSuccess
    
    def querying(self, table_name, equal_conditions = None): 
        #args: string, dict
        #return dataframe
        df = pd.DataFrame()      
        if not self._cnxn:
            return df         
        isSuccess = True 
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
            isSuccess = False
        return isSuccess
            
    def bulkInsert(self, table_name, df):    
        #args: string, dataframe
        cursor = None  
        isSuccess = True 
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
            isSuccess = False 
        finally:
            cursor.commit()
            cursor.close()
        return isSuccess  
            
    def insertOrUpdate(self, table_name, data, conditions):
        #args: string, dict, dict
        '''        
        update Ratings set rating='2' where ip_addr =  '0.0.0.1'
        IF @@ROWCOUNT=0
           insert into Ratings values (CURRENT_TIMESTAMP,1, 1, '0.0.0.1');
        '''
        query = ""
        args = []
        cursor = None
        isSuccess = True 
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
            isSuccess = False 
        finally:
            cursor.commit()
            cursor.close()
        return isSuccess

    def closeConnection(self):        
        self._cnxn.close()

        
import sqlalchemy as db
import urllib
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

class ORM_database:
    '''
    sqlalchemy method
    '''
    #Reference: https://www.pythonsheets.com/notes/python-sqlalchemy.html
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
            
    def getConnection(self):
        isSuccess = True 
        try:
            conn_str = f'DRIVER={self._driver};SERVER={self._server};DATABASE={self._db_name};UID={self._user};PWD={self._pwd}'
            params = urllib.parse.quote_plus(conn_str)
            self._engine = db.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        except Exception as e:
            print("Could not create engine")
            print(e)     
            isSuccess = False 
        
        return isSuccess
    
    def querying(self, table_name, conditions=None):
        '''
        args: str, dict
        simple: select * from table_name (where ...)
        Reflection approach
        return dataframe
        '''
        df = pd.DataFrame()      
        conn, session = None, None
        isSuccess = True 
        if not self._engine:
            return df          
        try:
            # To reflect an existing database into a new model.
            # Generating Mappings from an Existing MetaData
            conn = self._engine.connect()
            # produce our MetaData object
            metadata = db.MetaData()
            # reflect it ourselves from a database
            metadata.reflect(self._engine) #.reflect(self._engine, only=['Users', 'News'])
            # mapped classes are ready
            table = db.Table(table_name, metadata, autoload=True, autoload_with=self._engine)
            session = Session(self._engine)
            query = ''
            if conditions:
                query = session.query(table).filter_by(**conditions)
            else:
                query = session.query(table)
            #Convert to dataframe
            df = pd.read_sql(sql = query.statement, con = session.bind)
        except Exception as e:
            print("Could not select a table from database error:  ", e)
        finally:
            if session:
                session.close()
            if conn: 
                conn.close()
        return df
    
    def insert(self, table_name, df):
        '''
        df = values
        return True or false
        '''   
        conn, session = None, None
        isSuccess = True 
        if not self._engine:
            return False  
        # To reflect an existing database into a new model.
        #Generating Mappings from an Existing MetaData
        conn = self._engine.connect()
        args_list = df.to_dict('records')
        try:
            # produce our MetaData object
            metadata = db.MetaData()
            # reflect it ourselves from a database
            metadata.reflect(self._engine) #.reflect(self._engine, only=['Users', 'News'])
            # mapped classes are ready
            table = db.Table(table_name, metadata, autoload=True, autoload_with=self._engine) 
            conn.execute(table.insert(), args_list)
        except Exception as e:
            print("Could not insert a table from database error:  ", e)
            isSuccess = False
        finally:
            if session:
                session.close()
            if conn: 
                conn.close()
        return isSuccess
    
    def insertOrUpdate(self, table_name, data, conditions):
        '''
        table_name = str
        data, conditions = dict
        return True or false
        '''   
        if not self._engine:
            return False  
        # To reflect an existing database into a new model.
        #Generating Mappings from an Existing MetaData
        isSuccess = True
        conn, session = None, None
        
        try:
            if self.querying(table_name, conditions).empty:
                #insert:
                self.insert(table_name, pd.DataFrame([data], columns=data.keys()))
            else:
                #update
                conn = self._engine.connect()
                # produce our MetaData object
                metadata = db.MetaData()
                # reflect it ourselves from a database
                metadata.reflect(self._engine) #.reflect(self._engine, only=['Users', 'News'])
                # mapped classes are ready
                table = db.Table(table_name, metadata, autoload=True, autoload_with=self._engine)    
                session = Session(self._engine)
                  
                where_clauses = [db.text(str(item[0]) + "=" + str(item[1])) for item in conditions.items()]
                session.execute(db.update(table).where(db.and_(*where_clauses)).values(**data))
                session.commit()
                
        except Exception as e:
            print("Could not insert a table from database error:  ", e)
            isSuccess = False
        finally:
            if session:
                session.close()
            if conn: 
                conn.close()
        return isSuccess
        
    def closeConnection(self):        
        self._engine.dispose()


from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class ES_server:
    _es = None
    def __init__(self, nodes_lst):
        '''
        Elasticsearch low-level client. Provides a straightforward mapping from Python to ES REST endpoints.
        '''
        es = None
        try:
            es  = Elasticsearch(nodes_lst)
        except Exception as e:
            print("Could not create Elasticsearch:  ", e)
        finally:
            self._es = es
    
    def querying(self, index, body={"query": {"match_all": {}}}):
        '''
        Execute a search query and get back search hits that match the query.
        '''
        df = pd.DataFrame()
        
        if not self._es:
            return df
        try:
            res = self._es.search(index=index, body=body)
            lst = [{"id":x["_id"], **x["_source"]} for x in res["hits"]["hits"]]
            df = pd.DataFrame(lst)
        except Exception as e:
            print("Could not query Elasticsearch:  ", e)
        finally:
            return df
        return df
           
    def createIndex(self, index, body={}):
        success = False
        if not self._es:
            return success
        try:
            self._es.indices.create(index=index,body=body)
        except Exception as e:
            print("Could not create index Elasticsearch:  ", e)
        finally:
            success = True
        return success
        
    def bulkInsert(self, index, df, docType):    
        #args: string, dataframe , string
        isSuccess = False 
        if not self._es:
            return isSuccess   
        def gendata(documents):
            for i in range(0, len(documents)):
                print(documents[i])
                yield {
                    "_index": "employees",
                    "_type": "employee",
                    "_id": f"{i}",
                    "doc": [documents[i]]
                }
        try:
            # Bulk inserting documents. Each row in the DataFrame will be a document in ElasticSearch
            documents = df.to_dict(orient='records')
            #bulk(self._es, documents, index=index,doc_type=docType, raise_on_error=True)
            bulk(self._es, gendata(documents))
        except Exception as e:
            print("Could not bulk insert to Elasticsearch:", e)
            isSuccess = False 
        finally:
            isSuccess = False
        return isSuccess  
    
    def insertDict(self, index, doc, docType=None): 
        #args: string, dict , string
        res=""
        if not self._es:
            return res
        try:
            if docType:
                res = self._es.index(index=index,body=doc, doc_type=docType, refresh=True)
            else:
                res = self._es.index(index=index,body=doc, refresh=True)
        except Exception as e:
            print("Could not index Elasticsearch:  ", e)
        finally:
            print(res['result'])
            return res
        return res
        
if True:
    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.datetime.now(),
    }
    x = 'test'
    es = ES_server(['http://localhost:9200/'])
    
    data = [['tom', 11], ['nick', 12], ['juli', 14]] 
    df = pd.DataFrame(data, columns = ['Name', 'Age']) 
    es.bulkInsert(index="employees", df=df, docType="employee")
    print(es.querying("employees"))
    
    mapping = {
                       "mappings":{
                          "properties":{
                                 "name": { "type":"text"},
                                 "date":{ "type":"date"},
                                 "balance":{ "type":"double"},
                                 "liability":{ "type":"double"}
                          }
                       }
                     }
    
    #es.createIndex("test5")
    doc = {
        'name': 'kimchy',
        'date': datetime.datetime.now(),
        'balance': 11,
        'liability': 12
    }
    
    #es.insertDict("test4", doc, "_doc")
    
    