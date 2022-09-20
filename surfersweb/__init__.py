from flask import Flask
from surfersweb import config
from flask_sqlalchemy import SQLAlchemy
from .data.utilities import DataManager


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
    with app.app_context():
        app.logger.info('Setup Data Models')
        from surfersweb.data.models import db
        db.init_app(app)
        DataManager.initDB()

        app.logger.info('Import blueprints')
        from surfersweb.blueprints import bp as main_blueprint
        app.register_blueprint(main_blueprint)

    return app

