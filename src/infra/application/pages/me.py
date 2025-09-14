from dataclasses import dataclass
from typing import ClassVar

from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.infra.identity.services.token_auth import TokenAuth


@dataclass
class MePage:
    template_file_name: ClassVar[str] = "me.html"

    request: Request
    templates: Jinja2Templates
    token_auth: TokenAuth

    def __call__(self) -> HTMLResponse:
        return self.templates.TemplateResponse(
            request=self.request,
            name=self.template_file_name,
            context={
                "request": self.request,
                "user_data": self.token_auth.get_access_token(),
            },
        )
