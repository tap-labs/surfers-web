import json
import sys
from flask import jsonify
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
from willisurf import db, app

app.logger.info('Define DB Models')

## Table that stores regional data
class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)


## Table that stores regional data
class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    postal = db.Column(db.String(16), unique=True, index=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))


## Table that stores regional data
class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))


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
    site = db.Column(db.Text)
    url = db.Column(db.Text)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    def add(self):
        _id = None
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        return self.id


app.logger.info('DB URI: %s',app.config['SQLALCHEMY_DATABASE_URI'])
app.logger.info('Create DB')
with app.app_context():
    db.create_all()
    db.session.commit()

