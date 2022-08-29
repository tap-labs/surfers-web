import json
import sys
from surferslookout import app
import surferslookout
from . import models


class DataManager():

    @staticmethod
    def importData():
        with open(app.config['DATA_FILE'], 'r') as f:
            app.logger.info('Importing data')
            table = json.loads(f.read())
            for _country in table['country']:
                _cn = models.Country(name=_country['name'], 
                                    longitude=_country['longitude'],
                                    latitude=_country['latitude']).add()
                for _state in _country['state']:
                    _st = models.State(name=_state['name'],
                                        longitude=_state['longitude'],
                                        latitude=_state['latitude'], 
                                        postal=_state['postal'], 
                                        country_id=_cn).add()
                    for _region in _state['region']:
                        _re = models.Region(name=_region['name'], 
                                            longitude=_region['longitude'], 
                                            latitude=_region['latitude'], 
                                            state_id=_st).add()
                        for _location in _region['location']:
                            _lo = models.Location(name=_location['name'], 
                                                longitude=_location['longitude'], 
                                                latitude=_location['latitude'], 
                                                wg_site=_location['wg_site'], 
                                                region_id=_re).add()
                            for _cam in _location['cam']:
                                _ca = models.Cam(site=_cam['site'], url=_cam['url'], location_id=_lo).add()
