from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from punq import Container
from pydantic import UUID4
from starlette import status

from src.application.api.routers.notes.schemas import (
    CreatePointsSchema,
    NoteResponseSchema,
)
from src.domain.exceptions import ApplicationException
from src.project.containers import get_container
from src.service_layer.diary import Diary


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
    schema: CreatePointsSchema,
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


@router.get(
    path="/{note_oid}",
    name="Получить запись по oid",
    description="Получение записи о сне из дневника по идентификатору объекта.",
    status_code=status.HTTP_200_OK,
    response_model=NoteResponseSchema,
    responses={
        status.HTTP_200_OK: {"model": NoteResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
)
def get_note_by_oid(
    note_oid: UUID4,
    owner_oid: HeaderOwnerOid,
) -> NoteResponseSchema: ...


# repository = ORMDiaryRepository(database)
# try:
#     return service_layer.get_note_by_note_oid(
#         note_oid,
#         owner_oid,
#         repository,
#     )
# except NoteNotFound as exception:
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail={"error": exception.message},
#     )


@router.get(
    path="/{note_bedtime_date}",
    name="Получить запись по bedtime_date",
    description="Получение записи о сне из дневника по дате записи.",
    status_code=status.HTTP_200_OK,
    response_model=None,
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
)
def get_note_by_bedtime_date(
    bedtime_date: date,
    owner_oid: HeaderOwnerOid,
) -> None: ...


# repository = ORMDiaryRepository(database)
# try:
#     return service_layer.get_note_by_bedtime_date(
#         bedtime_date,
#         owner_oid,
#         repository,
#     )
# except NoteNotFound as exception:
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail={"error": exception.message},
#     )


@router.patch(
    path="/{note_oid}",
    name="Обновить запись",
    description="Обновление значений полей записи дневника сна.",
    status_code=status.HTTP_200_OK,
    response_model=None,
    responses={
        status.HTTP_200_OK: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
)
def update_note(
    note_oid: UUID4,
    owner_oid: HeaderOwnerOid,
) -> None: ...


@router.delete(
    path="/{note_oid}",
    name="Удалить запись",
    description="Удалить записи дневника сна.",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": None},
    },
)
def delete_note(
    note_oid: UUID4,
    owner_oid: HeaderOwnerOid,
) -> None: ...
