from pathlib import Path
from typing import ClassVar

from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.templating import Jinja2Templates


class UISettings(BaseSettings):
    _env_prefix: ClassVar[str] = "UI_"

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix=_env_prefix,
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )
    _BASE_DIR: ClassVar[Path] = Path(__file__).parent.parent.parent.parent

    app_static_path: str = "/static"
    static_path: Path = _BASE_DIR / "src" / "application" / "ui" / "static"
    templates_path: Path = _BASE_DIR / "src" / "application" / "ui" / "templates"

    @property
    def static_files(self) -> StaticFiles:
        return StaticFiles(
            directory=self.static_path,
        )

    @property
    def templates(self) -> Jinja2Templates:
        return Jinja2Templates(
            directory=self.templates_path,
        )
