from dataclasses import dataclass
from typing import ClassVar

from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.domain.sleep_diary.use_cases.get_user_weeks_info import GetUserWeeksInfoUseCase


@dataclass
class WeeksInfoPage:
    template_file_name: ClassVar[str] = "weeks_info.html"

    request: Request
    templates: Jinja2Templates
    get_user_weeks_info_use_case: GetUserWeeksInfoUseCase

    def __call__(self) -> HTMLResponse:
        return self.templates.TemplateResponse(
            request=self.request,
            name=self.template_file_name,
            context={
                "request": self.request,
                "weeks": self.get_user_weeks_info_use_case(),
            },
        )
