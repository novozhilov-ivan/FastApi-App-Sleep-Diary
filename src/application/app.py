from flask import Flask

from src.application.api.api import init_api_blueprint
from src.settings import Settings


def init_app() -> Flask:
    app = Flask("sleep_diary_app")
    app.config.from_object(obj=Settings())
    # metadata.create_all(engine)

    app.register_blueprint(
        blueprint=init_api_blueprint(),
        url_prefix="/api",
    )
    return app
