import sys
from flask import Flask
from surferslookout import config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

def create_app(config_name):
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)
    db.init_app(app)

    app.logger.info('Import blueprints')
    from surferslookout.blueprints import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

