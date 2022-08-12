import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("://", "ql://", 1)
    SQLALCHEMY_DB_HOST = os.getenv('DB_HOST')
    SQLALCHEMY_DB_USER = os.getenv('DB_USER')
    SQLALCHEMY_DB_PASSWORD = os.getenv('DB_PASSWORD')
    SQLALCHEMY_DATABASE = os.getenv('DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    POSTS_PER_PAGE = int(os.getenv('POSTS_PER_PAGE'))
    YOUR_ACCESS_KEY = os.getenv('YOUR_ACCESS_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
    TOKEN = os.environ.get('TOKEN')
    HEADERS = {'Authorization': f'Bearer {os.environ.get("API_TOKEN")}'}
    URL = os.environ.get('URL')


CONFIG = Config()
