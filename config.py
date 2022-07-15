import os

from dotenv import load_dotenv
from datetime import timedelta
load_dotenv(verbose=True)

basedir = os.path.abspath(os.path.dirname(__file__))

print(os.getenv('SQLALCHEMY_DATABASE_URI'))

class Config(object):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'please-remember-to-change-me'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)