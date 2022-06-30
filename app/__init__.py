from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import CONFIG

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to see this page!'
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_class=CONFIG):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    from app.auth.authorization import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from app.views.view import main, bp
    app.register_blueprint(main)
    app.register_blueprint(bp, url_prefix='/employee')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.models import dbmodels

    return app
