from uuid import UUID

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, HTTPException, status

from src.application.api.identity.services.token_auth import TokenAuth
from src.application.api.sleep_diary.handlers.notes.schemas import (
    CreatePointsRequestSchema,
)
from src.application.api.sleep_diary.services.diary import Diary
from src.domain.sleep_diary.exceptions.base import ApplicationError

router = APIRouter(
    tags=["Notes"],
    prefix="/notes",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": None},
    },
    route_class=DishkaSyncRoute,
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
    except ApplicationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error.message},
        ) from error
