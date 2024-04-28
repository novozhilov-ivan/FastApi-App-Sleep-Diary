from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager


class Base(DeclarativeBase):
    pass


api = Api(
    prefix='/api',
    doc='/doc'
)
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
