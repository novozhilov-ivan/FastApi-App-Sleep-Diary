from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


api = Api()
db = SQLAlchemy(model_class=Base)
