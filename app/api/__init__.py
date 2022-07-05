from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
bp = Blueprint('api', __name__)

from app.api import view, errors
