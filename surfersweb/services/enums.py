from enum import Enum, unique
from surfersweb import app

@unique
class API_URL(Enum):
    ALERTS = f"http://{app.config['API_HOST']}:{app.config['API_PORT']}/api/v1/weather/alert"
    SWELL = f"http://{app.config['API_HOST']}:{app.config['API_PORT']}/api/v1/surf/swell/"
    WATER = f"http://{app.config['API_HOST']}:{app.config['API_PORT']}/api/v1/surf/water/"
    WEATHER_CURRENT = f"http://{app.config['API_HOST']}:{app.config['API_PORT']}/api/v1/weather/observation/"

    def set_location(self, locationid):
        _url = f"{self.value}{locationid}"
        return _url
