from flask import Blueprint
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
bp = Blueprint('api', __name__)

from app.api import view, errors, tokens
