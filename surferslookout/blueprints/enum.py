from enum import Enum
from flask import current_app as app


class API_URL(Enum):
    ALERTS = 'http://{}:{}/api/v1/forecast/alert'.format(app.config['API_HOST'], app.config['API_PORT'])
    SWELL = 'http://{}:{}/api/v1/forecast/swell/{}'.format(app.config['API_HOST'], app.config['API_PORT'])
    WATER = 'http://{}:{}/api/v1/forecast/water/{}'.format(app.config['API_HOST'], app.config['API_PORT'])
    WEATHER = 'http://{}:{}/api/v1/forecast/weather/{}'.format(app.config['API_HOST'], app.config['API_PORT'])
