import json
import sys
from flask import jsonify
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
from surflookout import app, db

app.logger.info('Define DB Models')

## Table that stores regional data
class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
            app.logger.info('Country Record Added: %s', self.name)
        except IntegrityError:
            db.session.rollback()

        _resp = Country.query.with_entities(Country.id).filter(Country.name == self.name).first()
        _id = _resp["id"]

        return _id


## Table that stores regional data
class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    postal = db.Column(db.String(16), unique=True, index=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
            app.logger.info('State Record Added: %s', self.name)
        except IntegrityError:
            db.session.rollback()

        _resp = State.query.with_entities(State.id).filter(State.name == self.name).first()
        _id = _resp["id"]

        return _id


## Table that stores regional data
class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
            app.logger.info('Region Record Added: %s', self.name)
        except IntegrityError:
            db.session.rollback()

        _resp = Region.query.with_entities(Region.id).filter(Region.name == self.name).first()
        _id = _resp["id"]

        return _id


## Table that stores or general location information
class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    cam = db.Column(db.Text)
    gps = db.Column(db.Text)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

    def __repr__(self):
        return self.id

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
            app.logger.info('Location Record Added: %s', self.name)
        except IntegrityError:
            db.session.rollback()

        _resp = Location.query.with_entities(Location.id).filter(Location.name == self.name).first()
        _id = _resp["id"]

        return _id

    def get_id(self):
        _resp = Location.query.with_entities(Location.id).filter(Location.name == self.name).first()
        if(_resp is None):
            _id = self.add()
        else:
            _id = _resp["id"]
        return _id


## Class that stores all camera installations, Locations can have 1 or more cameras
class Cam(db.Model):
    __tablename__ = 'cam'
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(64), unique=True, index=True)
    url = db.Column(db.Text)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
            app.logger.info('Cam Record Added: %s', self.site)
        except IntegrityError:
            db.session.rollback()

        return self.id


def importData():
    with open('surflookout/data/data.json', 'r') as f:
        table = json.loads(f.read())
        for _country in table['country']:
            _cn = Country(name=_country['name']).add()
            for _state in _country['state']:
                _st = State(name=_state['name'], postal=_state['postal'], country_id=_cn).add()
                for _region in _state['region']:
                    _re = Region(name=_region['name'], state_id=_st).add()
                    for _location in _region['location']:
                        _lo = Location(name=_location['name'], gps=_location['gps'], region_id=_re).add()
                        for _cam in _location['cam']:
                            _ca = Cam(site=_cam['site'], url=_cam['url'], location_id=_lo).add()


app.logger.info('DB URI: %s',app.config['SQLALCHEMY_DATABASE_URI'])
app.logger.info('Create DB')
with app.app_context():
    db.create_all()
    db.session.commit()
    importData()




