from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.application.api.exceptions.register import register_exception_handlers
from src.application.api.router import router as api_router
from src.application.ui.router import router as ui_router
from src.project.containers import config, get_container


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sleep Diary",
        debug=True,
        # openapi_url=None,
        # docs_url=None,
        # redoc_url=None,
    )
    app.include_router(api_router)
    app.include_router(ui_router)
    register_exception_handlers(app)
    app.mount(
        path=config.ui.app_static_path,
        app=config.ui.static_files,
        name="static",
    )
    return app


def create_production_app() -> FastAPI:
    app = create_app()
    setup_dishka(
        container=get_container(),
        app=app,
    )
    return app
