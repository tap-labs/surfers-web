import datetime
import socket
import os
import time
from datetime import datetime
from wtforms import Form, BooleanField, StringField, validators
import flask
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask import current_app as app
from . import main
from surferslookout.data.models import Country, State, Region, Location, Cam

@main.route('/', methods=["GET"])
def home():
    app.logger.info("Accessing home page")

    return render_template('home.html')

@main.route('/sites', methods=["GET", "POST"])
def sites():
    app.logger.info("Accessing sites page")
    _countries = Country.query.all()
    _countryid = 0
    _states={}
    _stateid = 0
    _regions={}
    _regionid = 0
    _locations={}

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

    return render_template('sites.html', countries=_countries, countryid=_countryid,
                                        states=_states, stateid=_stateid,
                                        regions=_regions, regionid=_regionid,
                                        locations=_locations)


@main.route('/location/<locationid>', methods=["GET"])
def location(locationid):
    app.logger.info("Accessing Location page for locationid {0}", str(locationid))
    _cams={}
    _wgsite=0
    if locationid != 0:
        _location = Location.get_ById(locationid)
        _locations = Location.get_ByRegion(_location.region_id)
        _wgsite = _location.wg_site
        _cams = Cam.get(locationid)

    return render_template('location.html', locationid=locationid, location=_location, 
                                            locations=_locations, cams=_cams)

@main.route('/tools', methods=["GET"])
def tools():
    app.logger.info("Accessing Tools page")
    return render_template('tools.html')


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
 
    return dict(camlist=camlist, item_count=item_count, getvideoid=getvideoid, getwgsite=getwgsite, rowstart=rowstart, rowend=rowend)


##class SearchForm(Form):
##    location     = StringField('Location', [validators.Length(min=1, max=60)])
##    accept_rules = BooleanField('Search', [validators.InputRequired()])
