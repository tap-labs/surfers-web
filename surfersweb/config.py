import os
from os import path
import sys

basedir = os.getcwd()

class Binding:
    HOST = "localhost"
    USERNAME = "user"
    PASSWORD = "password"
    PORT = 3306
    DATABASE = "db"
    SQLALCHEMY_DATABASE_URI = ""

    def getDBURL(self, bindingFolder):
        print('Binding folder: {0}'.format(bindingFolder), file=sys.stdout)

        if path.exists(bindingFolder):
            print('Binding found', file=sys.stdout)
            i = 0
            for _key in os.listdir(bindingFolder):
                valueFile = bindingFolder + "/" + _key
                match _key:
                    case 'port':
                        self.PORT = open(valueFile).read()
                        i = i + 1
                    case 'database':
                        self.DATABASE = open(valueFile).read()
                        i = i + 1
                    case 'host':
                        self.HOST = open(valueFile).read()
                        i = i + 1
                    case 'username':
                        self.USERNAME = open(valueFile).read()
                        i = i + 1
                    case 'password':
                        self.PASSWORD = open(valueFile).read()
                        i = i + 1
            if i >= 4:
                self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
                print('Binding DB URI: {0}'.format(self.SQLALCHEMY_DATABASE_URI), file=sys.stdout)
                return self.SQLALCHEMY_DATABASE_URI
            else:
                return None
        else:
            return None


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SESSION_COOKIE_HTTPONLY = False
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    ENV = 'unset'
    PORT = os.environ.get('PORT') or 80
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('DB_TRACK_MODIFICATIONS') or False
    DATA_FILE = os.environ.get('DATA_FILE') or 'surferslookout/data/data.json'
    API_HOST = os.environ.get('API_HOST') or "surfersreport"
    API_PORT = os.environ.get('API_PORT') or "80"
    SERVICE_BINDING = os.environ.get('BINDING_NAME') or 'surferslookout-binding'
    BINDING_ASSIGNED = False
    if os.path.exists("bindings"):
        BINDING_ROOT = "bindings/"
    else:
        BINDING_ROOT = "/bindings/"
    BINDING_FOLDER = BINDING_ROOT + SERVICE_BINDING
    if path.exists(BINDING_FOLDER):
        _binding = Binding()
        SQLALCHEMY_DATABASE_URI = _binding.getDBURL(BINDING_FOLDER)

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    ENV = 'production'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:user@192.168.0.10/surferslookout'    

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'
    if Config.SQLALCHEMY_DATABASE_URI is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite://'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
