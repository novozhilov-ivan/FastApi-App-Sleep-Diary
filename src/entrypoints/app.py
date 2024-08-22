from flask import Flask

from src.configs import Settings
from src.entrypoints.api import init_api


def init_app() -> Flask:
    app = Flask("sleep_diary_app")
    app.config.from_object(Settings())
    # metadata.create_all(engine)
    api_bp = init_api()
    app.register_blueprint(api_bp, url_prefix="/api")
    return app
