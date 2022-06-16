from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import CONFIG

app = Flask(__name__)
app.config.from_object(CONFIG)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.models import dbmodels
from app.views import view
from app.views.view import mod

app.register_blueprint(mod)
