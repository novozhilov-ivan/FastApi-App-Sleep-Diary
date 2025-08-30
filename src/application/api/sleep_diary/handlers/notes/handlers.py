from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaSyncRoute, FromDishka
from fastapi import APIRouter, Header, HTTPException, Request, status
from pydantic import UUID4

from src.application.api.identity.auth.token_auth import TokenAuth
from src.application.api.sleep_diary.handlers.notes.schemas import (
    CreatePointsRequestSchema,
)
from src.application.api.sleep_diary.services.diary import Diary
from src.domain.sleep_diary.exceptions.base import ApplicationError
from src.infra.identity.access_token_processor import AccessTokenProcessor
from src.project.settings import AuthorizationTokenSettings

HeaderOwnerOid = Annotated[UUID4, Header(convert_underscores=False)]
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
    request: Request,
    schema: CreatePointsRequestSchema,
    token_processor: FromDishka[AccessTokenProcessor],
    settings: FromDishka[AuthorizationTokenSettings],
    diary: FromDishka[Diary],
) -> None:
    token_auth = TokenAuth(
        request=request,
        token_processor=token_processor,
        settings=settings,
    )

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
