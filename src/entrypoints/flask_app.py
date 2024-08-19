from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


get_session = sessionmaker(
    bind=create_engine(
        url="",
    ),
)


def web_app_factory() -> Flask:
    return Flask(import_name="sleep_diary_app")
