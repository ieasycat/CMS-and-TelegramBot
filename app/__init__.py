from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import CONFIG

app = Flask(__name__)

app.config.from_object(CONFIG)

login = LoginManager(app)
bootstrap = Bootstrap(app)
mail = Mail(app)

login.login_view = 'login'
login.login_message = 'Please log in to see this page!'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.models import dbmodels
from app.views import view, authorization
from app.views.view import mod

app.register_blueprint(mod)



