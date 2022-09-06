import datetime
import socket
import os
import time
import json
from datetime import datetime
import flask
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask import current_app as app
from . import main
from surferslookout.data.models import Country, State, Region, Location, Cam

@main.route('/', methods=["GET"])
def home():
    app.logger.info("Accessing home page")

    return render_template('home.html')

@main.route('/beaches', methods=["GET", "POST"])
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


@main.route('/location/<locationid>', methods=["GET"])
def location(locationid):
    app.logger.info("Accessing Location page for locationid {0}", str(locationid))
    _cams={}
    if locationid != 0:
        _location = Location.get_ById(locationid)
        _locations = Location.get_ByRegion(_location.region_id)
        _cams = Cam.get(locationid)

    return render_template('location.html', locationid=locationid, location=_location, 
                                            locations=_locations, cams=_cams) 


@main.route('/forum', methods=["GET", "POST"])
def forum():
    app.logger.info("Accessing Forum page")
    return render_template('forum.html')

@main.route('/about', methods=["GET"])
def about():
    app.logger.info("Accessing About page")
    return render_template('about.html')


@main.route('/search/<location>', methods=["GET"])
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



@main.context_processor
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

    def locationnames_asdict():
        _request = Location.get_AllNamesSerialized()
        return _request

    return dict(camlist=camlist, item_count=item_count, 
                    getvideoid=getvideoid, getwgsite=getwgsite, 
                    rowstart=rowstart, rowend=rowend, 
                    locationsbyregion_asdict=locationsbyregion_asdict, 
                    locationsbycountry_asdict=locationsbycountry_asdict,
                    locationsbystate_asdict=locationsbystate_asdict,
                    locationnames_asdict=locationnames_asdict)


