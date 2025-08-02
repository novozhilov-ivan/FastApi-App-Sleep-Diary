from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Header, HTTPException
from pydantic import UUID4
from starlette import status

from src.application.api.identity.auth.token_auth import TokenAuth
from src.application.api.sleep_diary.handlers.notes.schemas import (
    CreatePointsRequestSchema,
)
from src.application.api.sleep_diary.services.diary import Diary
from src.domain.sleep_diary.exceptions.base import ApplicationException


HeaderOwnerOid = Annotated[UUID4, Header(convert_underscores=False)]
router = APIRouter(
    tags=["Notes"],
    prefix="/notes",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": None},
    },
    route_class=DishkaRoute,
)


@router.post(
    path="",
    description="Добавление новой записи в дневник сна.",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses={
        status.HTTP_201_CREATED: {"model": None},
    },
)
def add_note(
    schema: CreatePointsRequestSchema,
    token_auth: FromDishka[TokenAuth],
    diary: FromDishka[Diary],
) -> None:

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
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
