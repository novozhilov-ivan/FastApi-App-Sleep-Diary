from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from punq import Container
from pydantic import UUID4
from starlette import status

from src.sleep_diary.application.services.diary import Diary
from src.sleep_diary.config.containers import get_container
from src.sleep_diary.domain.exceptions import ApplicationException
from src.sleep_diary.infrastructure.api.routers.notes.schemas import (
    CreatePointsRequestSchema,
)


HeaderOwnerOid = Annotated[UUID4, Header(convert_underscores=False)]
router = APIRouter(
    tags=["Notes"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": None},
    },
)


@router.post(
    path="/",
    name="Добавить запись",
    description="Добавление новой записи в дневник сна.",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses={
        status.HTTP_201_CREATED: {"model": None},
    },
)
def add_note(
    schema: CreatePointsRequestSchema,
    owner_oid: HeaderOwnerOid,
    container: Container = Depends(get_container),
) -> None:
    diary: Diary = container.resolve(Diary)

    try:
        diary.write(
            owner_oid,
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
