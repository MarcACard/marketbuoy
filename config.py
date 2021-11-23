"""FLASK configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Set Flask Config Variables."""

    FLASK_APP = "wsgi.py"
    SECRET_KEY = environ.get("SECRET_KEY")

    # Flask
    TESTING = True
    DEBUG = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "postgresql:///marketbuoy"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
