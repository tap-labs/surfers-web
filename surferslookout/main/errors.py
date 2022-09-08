from flask import current_app, render_template
from . import main
from surferslookout.data.models import Location

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error_description=e.description, locationnames=locationnames())

@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html', error_description=e.description, locationnames=locationnames())

def locationnames():
    _request = Location.get_AllNamesSerialized()
    return _request
