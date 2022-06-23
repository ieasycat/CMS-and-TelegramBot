import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    POSTS_PER_PAGE = int(os.getenv('POSTS_PER_PAGE'))
    YOUR_ACCESS_KEY = os.getenv('YOUR_ACCESS_KEY')


CONFIG = Config()
