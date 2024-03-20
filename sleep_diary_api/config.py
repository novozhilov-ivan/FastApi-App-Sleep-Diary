from os import path, environ

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

load_dotenv()

# DB
DB_DRIVER = environ.get('DB_DRIVER')
DB_EXTEND_DRIVER = environ.get('DB_EXTEND_DRIVER')
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')
DB_NAME = environ.get('DB_NAME')
DB_EXTEND_DRIVER = f"+{DB_EXTEND_DRIVER}" if DB_EXTEND_DRIVER else ''


class Config:
    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_APP = environ.get('FLASK_APP')

    # Database
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = "{}{}://{}:{}@{}:{}/{}".format(
        DB_DRIVER,
        DB_EXTEND_DRIVER,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # etc
    MAX_CONTENT_LENGTH = 1024 * 1024
    DB_URL = SQLALCHEMY_DATABASE_URI
