from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(configuration_mode):
    """
    The flask application instance
    :param configuration_mode: configuration mode to load for the flask app
    :return: the flask app
    """
    
    app = Flask(__name__, instance_relative_config=True)
    
    from configure import load_configuration
    
    load_configuration(app, configuration_mode)
    
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    
    return app
