from dotenv import load_dotenv
import os

APP_ROOT = os.path.join(os.path.dirname(__file__))

APP_ENV = os.getenv('APP_ENV' , 'development')

ENVIRONMENTS = {
    'production': '.prod.env',
    'development': '.env'
}

dotenv_path = os.path.join(APP_ROOT, ENVIRONMENTS.get(APP_ENV) or '.env' )

load_dotenv(dotenv_path)

class AllConfig():
    def __init__(self):
        self.APP_ENV = APP_ENV
        self.API_ENDPOINT = os.environ.get('API_ENDPOINT', 'localhost:5001')
        self.__ConfigPath = os.path.abspath(__file__)
        self.ROOT_PATH = os.path.split(self.__ConfigPath)[0]  
        
        self.DB_USERNAME = os.environ.get('MONGODB_USER')
        self.DB_PASSWORD = os.environ.get('MONGODB_PASS')
        self.DB_DATABASE = os.environ.get('MONGODB_DATABASE')
        self.DB_DOMAIN = os.environ.get('MONGODB_HOST', 'mongo')
        self.DB_PORT = os.environ.get('MONGODB_PORT', '27017')

        self.DSN = f"mongodb://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_DOMAIN}:{self.DB_PORT}/"
    
settings = AllConfig()