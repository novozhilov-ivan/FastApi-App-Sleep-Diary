from flask import Flask

from src.configs import Settings


def init_app() -> Flask:
    app = Flask(import_name="sleep_diary_app")
    app.config.from_object(obj=Settings())

    return app
