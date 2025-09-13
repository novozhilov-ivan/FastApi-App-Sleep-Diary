from dataclasses import dataclass
from datetime import date
from typing import ClassVar

from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.domain.sleep_diary.use_cases.get_user_week_notes import GetUserWeekNotesUseCase
from src.infra.application.pages.schemas import WeekNotesListSchema


@dataclass
class WeekPage:
    template_file_name: ClassVar[str] = "week.html"

    request: Request
    templates: Jinja2Templates
    get_week_notes_use_case: GetUserWeekNotesUseCase

    def __call__(self, start_date: date) -> HTMLResponse:
        week_notes = self.get_week_notes_use_case(start_date)

        week_notes_schema = WeekNotesListSchema.from_week_notes(week_notes)
        return self.templates.TemplateResponse(
            request=self.request,
            name=self.template_file_name,
            context={
                "request": self.request,
                "week_notes": week_notes_schema,
                "week_statistics": {},
            },
        )
