from dataclasses import dataclass
from typing import ClassVar

from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.domain.sleep_diary.dtos import AboutInfo


@dataclass
class AboutPage:
    template_file_name: ClassVar[str] = "about.html"

    request: Request
    templates: Jinja2Templates
    about_info: AboutInfo

    def __call__(self) -> HTMLResponse:
        return self.templates.TemplateResponse(
            request=self.request,
            name=self.template_file_name,
            context={
                "request": self.request,
                "about_info": self.about_info,
            },
        )
