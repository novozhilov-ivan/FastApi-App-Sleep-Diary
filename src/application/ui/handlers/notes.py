from datetime import date
from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Depends, Form, Path, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from src.application.ui.schemas import CreateNoteSchema, PatchNoteSchema
from src.domain.sleep_diary.exceptions.base import ApplicationError
from src.infra.identity.services.token_auth import TokenAuth
from src.infra.sleep_diary.commands import DeleteNoteCommand
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
    diary: FromDishka[Diary],
    token_auth: FromDishka[TokenAuth],
) -> HTMLResponse:
    try:
        diary.write(
            UUID(token_auth.get_subject()),
            schema.bedtime_date,
            schema.went_to_bed,
            schema.fell_asleep,
            schema.woke_up,
            schema.got_up,
            schema.no_sleep,
        )
    except ApplicationError as error:
        return RedirectResponse(
            url=request.url_for("weeks_info_page").replace_query_params(
                error=error.message,
            ),
            status_code=status.HTTP_302_FOUND,
        )

    return RedirectResponse(
        url=request.url_for("weeks_info_page").replace_query_params(
            success="Запись успешно сохранена!",
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.patch(
    path="/{note_date}",
    status_code=status.HTTP_303_SEE_OTHER,
    response_class=HTMLResponse,
    dependencies=[
        Depends(config.authorization_token.jwt_api_key_cookies),
    ],
)
def edit_note_page(
    request: Request,
    note_date: Annotated[date, Path()],
    schema: Annotated[PatchNoteSchema, Form()],
    diary: FromDishka[Diary],
    token_auth: FromDishka[TokenAuth],
) -> HTMLResponse:
    try:
        command = schema.to_command(
            owner_oid=token_auth.get_subject(),
            note_date=note_date,
        )
        diary.edit(command)
    except ApplicationError as error:
        return RedirectResponse(
            url=request.url_for("weeks_info_page").replace_query_params(
                error=error.message,
            ),
            status_code=status.HTTP_302_FOUND,
        )

    return RedirectResponse(
        url=request.url_for("weeks_info_page").replace_query_params(
            success="Запись успешно изменена!",
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.delete(
    path="/{note_date}",
    status_code=status.HTTP_303_SEE_OTHER,
    response_class=HTMLResponse,
    dependencies=[
        Depends(config.authorization_token.jwt_api_key_cookies),
    ],
)
def delete_note_page(
    request: Request,
    note_date: Annotated[date, Path()],
    diary: FromDishka[Diary],
    token_auth: FromDishka[TokenAuth],
) -> HTMLResponse:
    try:
        command = DeleteNoteCommand(
            owner_oid=token_auth.get_subject(),
            note_date=note_date,
        )
        diary.delete(command=command)
    except ApplicationError as error:
        return RedirectResponse(
            url=request.url_for("weeks_info_page").replace_query_params(
                error=error.message,
            ),
            status_code=status.HTTP_302_FOUND,
        )

    return RedirectResponse(
        url=request.url_for("weeks_info_page").replace_query_params(
            success=f"Запись за {note_date} удалена!",
        ),
        status_code=status.HTTP_303_SEE_OTHER,
    )
