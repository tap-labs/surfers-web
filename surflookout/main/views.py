import datetime
import socket
import os
import time
from datetime import datetime
import flask
from flask import Blueprint, render_template, request, jsonify, session
from flask import current_app as app
from . import main
from surflookout.data.models import Country, State, Region, Location, Cam

@main.route('/', methods=["GET", "POST"])
def home():
    app.logger.info("Accessing home page")
    _countries = Country.query.all()
    _countryid = 0
    _states={}
    _stateid = 0
    _regions={}
    _regionid = 0
    _locations={}
    _locationid = 0
    _cams={}
    _camcount=0

    if request.method == "POST":
        app.logger.info("Form Post")
        _countryid = int(request.form["country"])
        if _countryid != 0:
            _states = State.get_ByCountry(_countryid)
            _stateid = int(request.form["state"])
            if _stateid != 0:
                _regions = Region.get_ByState(_stateid)
                _regionid = int(request.form["region"])
                if _regionid != 0:
                    _locations = Location.get_ByRegion(_regionid)
                    _locationid = int(request.form["location"])
                    if _locationid != 0:
                        _location = Location.get_ById(_locationid)
                        _cams = Cam.get(_locationid)

    return render_template('home.html', countries=_countries, countryid=_countryid,
                                        states=_states, stateid=_stateid,
                                        regions=_regions, regionid=_regionid,
                                        locations=_locations, locationid=_locationid, cams=_cams)

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

    return dict(camlist=camlist, item_count=item_count, getvideoid=getvideoid)
