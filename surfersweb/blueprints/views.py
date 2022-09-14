import json
from enum import Enum, unique
from datetime import datetime
from flask import render_template, request, redirect
from flask import current_app as app
from . import bp
from surfersweb.data.models import *
from surfersweb.services import web


@bp.route('/', methods=["GET"])
def home():
    app.logger.info("Accessing home page")

    try:
        _alerts = web.get(API_URL.ALERTS.value)
        _message = "<b>Current Marine Weather Warnings:<b>&emsp;&emsp;&emsp;&emsp;"
        for _alert in _alerts:
            _message = _message + "<a href='" + _alert['link'] + "'>" + _alert['title'] + "</a>&emsp;&emsp;&emsp;&emsp;"
        app.logger.info("Weather Banner: {}".format(_message))
    except:
        app.logger.error("Weather Banner Generation failed")
        _message = ""


    return render_template('home.html', message=_message)

@bp.route('/beaches', methods=["GET", "POST"])
def beaches():
    app.logger.info("Accessing sites page")
    _countries = Country.query.all()
    _countryid = 0
    _states={}
    _stateid = 0
    _regions={}
    _regionid = 0
    _locations={}
    _x = "-24.971391128601727"
    _y = "135.88779862421478"
    _zoom = 2

    if request.method == "POST":
        app.logger.info("Form Post")
        _locationid = int(request.form["location"])
        if _locationid != 0:
            return redirect(f'/location/{_locationid}')
        else:
            _countryid = int(request.form["country"])
            if _countryid != 0:
                _states = State.get_ByCountry(_countryid)
                _stateid = int(request.form["state"])
                if _stateid != 0:
                    _regions = Region.get_ByState(_stateid)
                    _regionid = int(request.form["region"])
                    if _regionid != 0:
                        _locations = Location.get_ByRegion(_regionid)
                        _x = Region.query.get(_regionid).latitude
                        _y = Region.query.get(_regionid).longitude
                    else:
                        _x = State.query.get(_stateid).latitude
                        _y = State.query.get(_stateid).longitude
                else:
                    _x = Country.query.get(_countryid).latitude
                    _y = Country.query.get(_countryid).longitude
    else:
        # added logic to default to Australia if first access
        _countryid = 1
        _states = State.get_ByCountry(_countryid)
        _x = Country.query.get(_countryid).latitude
        _y = Country.query.get(_countryid).longitude

    return render_template('beaches.html', countries=_countries, countryid=_countryid,
                                        states=_states, stateid=_stateid,
                                        regions=_regions, regionid=_regionid,
                                        locations=_locations, x=_x, y=_y)


@bp.route('/location/<locationid>', methods=["GET"])
def location(locationid):
    app.logger.info("Accessing Location page for locationid {0}", str(locationid))
    _cams={}

    if locationid != 0:
        _location = Location.get_ById(locationid)
        _locations = Location.get_ByRegion(_location.region_id)
        _cams = Cam.get(locationid)
        _swell = web.get(API_URL.SWELL.set_location(_location.bom_geo_tag))
        _water = web.get(API_URL.WATER.set_location(_location.bom_geo_tag))

    return render_template('location.html', locationid=locationid, location=_location, 
                                            locations=_locations, cams=_cams, 
                                            swell=_swell, water=_water) 


@bp.route('/forum', methods=["GET", "POST"])
def forum():
    app.logger.info("Accessing Forum page")
    return render_template('forum.html')

@bp.route('/about', methods=["GET"])
def about():
    app.logger.info("Accessing About page")
    return render_template('about.html')


@bp.route('/search/<location>', methods=["GET"])
def search(location):
    app.logger.info("Search requested - {}".format(location))
    if "," in location:
        _entries = location.split(',')
        _town = _entries[0].strip()
        _state = _entries[1].strip()
        _results = Location.find(_town, _state)
    else:
        _results = Location.find(location.strip())
    
    for item in json.loads(_results):
        _url = '/location/{}'.format(item['id'])
    return redirect(_url)


## Jinja Variables
@bp.context_processor
def inject_locationnames():
    _request = Location.get_AllNamesSerialized()
    return dict(locationnames=_request)

## Jinja Functions 
@bp.context_processor
def utilities():
    def item_count(list):
        return len(list)

    def camlist(locationid):
        _cams = {}
        if locationid != 0:
            _cams = Cam.get(locationid)
        return _cams

    def getvideoid(id):
        return 'video-{0}'.format(id)

    def getwgsite(locationid):
        _location = Location.get_id(locationid)
        return _location.wg_site

    def rowstart(entry):
        if entry%2 == 0:
            return f'<td style="border:none;">'
        else:
            return f'<tr><td style="border:none;">'

    def rowend(entry):
        if entry%2 == 0:
            return f'</td></tr>'
        else:
            return f'</td>'

    def locationsbyregion_asdict(regionid):
        _request = Location.get_ByRegionSerialized(regionid)
        return _request

    def locationsbycountry_asdict(countryid):
        _request = Location.get_ByCountrySerialized(countryid)
        return _request

    def locationsbystate_asdict(stateid):
        _request = Location.get_ByStateSerialized(stateid)
        return _request


    return dict(camlist=camlist, 
                item_count=item_count, 
                getvideoid=getvideoid, 
                getwgsite=getwgsite, 
                rowstart=rowstart, 
                rowend=rowend, 
                locationsbyregion_asdict=locationsbyregion_asdict, 
                locationsbycountry_asdict=locationsbycountry_asdict,
                locationsbystate_asdict=locationsbystate_asdict)

@unique
class API_URL(Enum):
    ALERTS = 'http://{}:{}/api/v1/forecast/alert'.format(app.config['API_HOST'], app.config['API_PORT'])
    SWELL = 'http://{}:{}/api/v1/forecast/swell/'.format(app.config['API_HOST'], app.config['API_PORT'])
    WATER = 'http://{}:{}/api/v1/forecast/water/'.format(app.config['API_HOST'], app.config['API_PORT'])
    WEATHER = 'http://{}:{}/api/v1/forecast/weather/'.format(app.config['API_HOST'], app.config['API_PORT'])

    def set_location(self, locationid):
        _url = f"{self.value}{locationid}"
        return _url
