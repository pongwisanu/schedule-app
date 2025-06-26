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
        self.__ConfigPath = os.path.abspath(__file__)
        self.ROOT_PATH = os.path.split(self.__ConfigPath)[0]
        self.JOB_PATH = os.path.join(self.ROOT_PATH , "celery_trigger")
        if(not os.path.isdir(self.JOB_PATH)):
            print("celery_trigger is not exist")
            os.mkdir(self.JOB_PATH)
            print("Create celery_trigger success")
            # raise Exception("Directory 'celery_trigger' is not exist in app path")
        
        self.DB_USERNAME = os.environ.get('MONGODB_USER')
        self.DB_PASSWORD = os.environ.get('MONGODB_PASS')
        self.DB_DATABASE = os.environ.get('MONGODB_DATABASE')
        self.DB_DOMAIN = os.environ.get('MONGODB_HOST', 'mongo')
        self.DB_PORT = os.environ.get('MONGODB_PORT', '27017')
    
        self.DSN = f"mongodb://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_DOMAIN}:{self.DB_PORT}/"
        
        self.BROKER_TYPE = os.environ.get('BROKER_TYPE', 'redis')
        self.BROKER_HOST = os.environ.get('BROKER_HOST', 'localhost')
        self.BROKER_PORT = os.environ.get('BROKER_PORT', '6379')
        self.BROKER_USER = os.environ.get('BROKER_USER', '')
        self.BROKER_PASS = os.environ.get('BROKER_PASS', '')
        self.BROKER_PATH = os.environ.get('BROKER_PATH', '0')
        if (self.BROKER_TYPE == "redis"):
            self.BROKER_URL = f"redis://{self.BROKER_USER}:{self.BROKER_PASS}@{self.BROKER_HOST}:{self.BROKER_PORT}/{self.BROKER_PATH}"
        elif (self.BROKER_TYPE == "rabbitmq"):
            self.BROKER_URL = f"amqp://{self.BROKER_USER}:{self.BROKER_PASS}@{self.BROKER_HOST}:{self.BROKER_PORT}/{self.BROKER_PATH}"
        else:
            raise Exception("Broker type not exist must be 'redis' or 'rabbitmq'")
        
settings = AllConfig()