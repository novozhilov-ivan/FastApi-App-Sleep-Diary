from flask import Flask

from src.application.api.api import init_api
from src.settings import Settings


def init_app() -> Flask:
    app = Flask("sleep_diary_app")
    app.config.from_object(Settings())
    # metadata.create_all(engine)
    api_bp = init_api()
    app.register_blueprint(api_bp, url_prefix="/api")
    return app
