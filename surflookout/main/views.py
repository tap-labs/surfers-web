import datetime
import socket
import os
import time
from datetime import datetime
import flask
from flask import Blueprint, render_template, request, jsonify, session
from flask import current_app as app
from . import main
from surflookout.data import Country

@main.route('/', methods=["GET"])
def home():
    app.logger.info("Accessing home page")

    return render_template('home.html')
