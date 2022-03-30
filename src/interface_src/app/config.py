'''
- To register configs on the app and to be accessible from any part of the application.

'''
import secrets, os

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    HOST = '0.0.0.0'
    DEBUG = False
    SECRET_KEY = secrets.token_urlsafe(16)
    # check for modifications of the template source and reload it automatically.
    TEMPLATES_AUTO_RELOAD = True

    '''
    - Connection string for MSSQL server
        conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};\
        SERVER=127.0.0.1,1433;\
        DATABASE=TestDB;\
        UID=sa;\
        PWD=Admin_password123'
    - If running in docker-compose, \
        use the Alias  <CONTAINER_NAME, CONTAINER_PORT> 
        in the docker-compose.yml instead
    '''
    DRIVER = '{ODBC Driver 17 for SQL Server}'
    #SERVER = 'db,1433' 
    #SERVER = '127.0.0.1,1433'
    SERVER = '127.0.0.1,1433'
    DB_NAME = 'TestDB'
    USER = 'sa'
    PWD = 'Admin_password123'
    
    # Initialize all the newsfeed paths from the source
    current_dir = os.path.dirname(os.path.realpath(__file__))
    XML1 = current_dir + "/controller/resources/Technology.xml"
    XML2 = current_dir + "/controller/resources/Europe.xml"
    
    # Numbers of top hit to display in the web interface
    TOP_NEWS = 5
    # Seconds to wait and refresh the web interface
    UPDATE_TIME_INTERVAL = 300

class DockerConfig(DevelopmentConfig):
    SERVER = 'db,1433' 
    