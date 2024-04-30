from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


api = Api(prefix="/api", doc="/doc", ordered=True, validate=True)
db = SQLAlchemy(model_class=Base)
