from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import POSTGRES_USER, POSTGRES_PASSWORD, DB_NAME
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.models import dbmodels
from app.views import view
