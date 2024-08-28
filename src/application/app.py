from flask import Flask

from src.application.api.api import init_api_blueprint
from src.infrastructure.database import Database
from src.infrastructure.orm import metadata
from src.settings import Settings


def init_app() -> Flask:
    app = Flask("sleep_diary_app")
    settings = Settings()
    app.config.from_object(settings)
    database = Database(settings.POSTGRES_DB_URL)
    metadata.create_all(database.engine)
    app.register_blueprint(
        blueprint=init_api_blueprint(),
        url_prefix="/api",
    )
    return app
