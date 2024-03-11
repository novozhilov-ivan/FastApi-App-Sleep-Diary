import os

from dotenv import load_dotenv

load_dotenv()

# DB
DB_DRIVER = os.getenv('DB_DRIVER')
DB_EXTEND_DRIVER = os.getenv('DB_EXTEND_DRIVER')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_EXTEND_DRIVER = f"+{DB_EXTEND_DRIVER}" if DB_EXTEND_DRIVER else ''


class Config:
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
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_ECHO = True if os.getenv('SQLALCHEMY_ECHO') == 'True' else None
    MAX_CONTENT_LENGTH = 1024 * 1024
    
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')

