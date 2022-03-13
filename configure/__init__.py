import os

from dotenv import load_dotenv

from helpers import ROOT_DIR

dotenv_path = os.path.join(ROOT_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class BaseConfig:
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''
    DEBUG = True
    TESTING = False
    ENV = 'development'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    DEBUG = False
    TESTING = False
    ENV = 'production'


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = False
    TESTING = True
    ENV = 'testing'


config_mode = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}


def detect_configuration():
    """
    Detect config mode from environment variable and return it.
    :return: Configuration mode
    """
    
    configuration_mode = os.environ['CONFIG_MODE']
    
    if configuration_mode not in config_mode.keys():
        print('Invalid configuration mode: {}'.format(configuration_mode))
        return
    
    print('{}: configuration mode detected'.format(configuration_mode))
    return configuration_mode


def load_configuration(app, mode):
    """
    Load configuration from object and instance folder
    :param app: The flask application
    :param mode: The configuration mode to load
    :return: None
    """
    
    configuration = config_mode[mode]
    
    app.config.from_object(configuration)
    
    app.config.from_pyfile('config', silent=True)
