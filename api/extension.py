from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


api = Api(
    prefix='/api',
    doc='/doc'
)
db = SQLAlchemy(model_class=Base)
