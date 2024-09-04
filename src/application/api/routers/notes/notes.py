from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import UUID4
from starlette import status

from src import service_layer
from src.application.api.schemas import ErrorSchema
from src.domain.exceptions import ApplicationException
from src.domain.note import NoteTimePoints
from src.infrastructure.database import Database, get_db
from src.infrastructure.repository import ORMDiaryRepository


HeaderOwnerOid = Annotated[UUID4, Header(convert_underscores=False)]
router = APIRouter(
    tags=["Notes"],
)


@router.post(
    path="/",
    description="Добавление новой записи в дневник.",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
def write_note(
    time_points: NoteTimePoints,
    owner_oid: HeaderOwnerOid,
    database: Database = Depends(get_db),
) -> None:
    repo = ORMDiaryRepository(database)
    try:
        service_layer.write(
            time_points.bedtime_date,
            time_points.went_to_bed,
            time_points.fell_asleep,
            time_points.woke_up,
            time_points.got_up,
            time_points.no_sleep,
            owner_oid,
            repo,
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )


# namespace_notes.add_resource(
#     endpoints.GetNoteByOidEndPoint,
#     "/<uuid:note_id>",
#     endpoint=endpoints.GetNoteByOidEndPoint.NAME,
# )
# namespace_notes.add_resource(
#     endpoints.GetNoteByBedtimeDateEndPoint,
#     "/<string:note_bedtime_date>",
#     endpoint=endpoints.GetNoteByBedtimeDateEndPoint.NAME,
# )
# namespace_notes.add_resource(
#     endpoints.UpdateNoteEndPoint,
#     "/<uuid:note_id>",
#     endpoint=endpoints.UpdateNoteEndPoint.NAME,
# )
# namespace_notes.add_resource(
#     endpoints.DeleteNoteEndPoint,
#     "/<uuid:note_id>",
#     endpoint=endpoints.DeleteNoteEndPoint.NAME,
# )
