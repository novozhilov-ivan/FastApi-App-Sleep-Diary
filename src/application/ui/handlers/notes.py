from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.ui.schemas import CreateNoteSchema
from src.domain.identity.exceptions import IdentityError
from src.domain.sleep_diary.exceptions.base import ApplicationError
from src.infra.identity.services.token_auth import TokenAuth
from src.infra.sleep_diary.use_cases.diary import Diary
from src.project.containers import config

router = APIRouter(
    prefix="/notes",
    route_class=DishkaSyncRoute,
)


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_class=HTMLResponse,
    dependencies=[
        Depends(config.authorization_token.jwt_api_key_cookies),
    ],
)
def add_note_page(
    request: Request,
    schema: Annotated[CreateNoteSchema, Form()],
    dairy: FromDishka[Diary],
    token_auth: FromDishka[TokenAuth],
) -> HTMLResponse:
    try:
        dairy.write(
            UUID(token_auth.get_subject()),
            schema.bedtime_date,
            schema.went_to_bed,
            schema.fell_asleep,
            schema.woke_up,
            schema.got_up,
            schema.no_sleep,
        )
    except (ApplicationError, IdentityError) as error:
        return RedirectResponse(
            url=f"{request.url_for('fetch_sign_up_page')}/?error={error.message}",
            status_code=status.HTTP_302_FOUND,
        )

    return RedirectResponse(
        url=f"{request.url_for('weeks_info_page')}/?success=Запись успешно сохранена!",
        status_code=status.HTTP_302_FOUND,
    )
