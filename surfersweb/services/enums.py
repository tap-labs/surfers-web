from enum import Enum, unique
from flask import current_app as app

@unique
class API_URL(Enum):
    ALERTS = f"{app.config['API_URL']}/weather/alert"
    SWELL = f"{app.config['API_URL']}/surf/swell/"
    WATER = f"{app.config['API_URL']}/surf/water/"
    LOCATION = f"{app.config['API_URL']}/weather/locations/"
    WEATHER_CURRENT = f"{app.config['API_URL']}/weather/observation/"
    HEALTHZ = f"{app.config['API_URL']}/healthz"

    def set_location(self, locationid):
        _url = f"{self.value}{locationid}"
        return _url
