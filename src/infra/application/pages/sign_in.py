from dataclasses import dataclass
from typing import ClassVar

from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates


@dataclass
class FetchSignInPage:
    template_file_name: ClassVar[str] = "sign_in.html"

    request: Request
    templates: Jinja2Templates

    def __call__(self) -> HTMLResponse:
        return self.templates.TemplateResponse(
            request=self.request,
            name=self.template_file_name,
            context={
                "request": self.request,
            },
        )
