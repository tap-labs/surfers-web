import sys
from flask import Flask
from surflookout import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
    db.init_app(app)

    app.logger.info('Import blueprints')
    from surflookout.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

