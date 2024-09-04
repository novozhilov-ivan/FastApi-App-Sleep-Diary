from fastapi import APIRouter


router = APIRouter(
    tags=["Notes"],
)

namespace_notes = Namespace(
    name="Notes",
    description="Действия с записями дневника",
    path="/notes",
    # decorators=[validate_auth_token],
)

namespace_notes.add_resource(
    endpoints.AddNoteEndPoint,
    "",
    endpoint=endpoints.AddNoteEndPoint.NAME,
)
namespace_notes.add_resource(
    endpoints.GetNoteByOidEndPoint,
    "/<uuid:note_id>",
    endpoint=endpoints.GetNoteByOidEndPoint.NAME,
)
namespace_notes.add_resource(
    endpoints.GetNoteByBedtimeDateEndPoint,
    "/<string:note_bedtime_date>",
    endpoint=endpoints.GetNoteByBedtimeDateEndPoint.NAME,
)
namespace_notes.add_resource(
    endpoints.UpdateNoteEndPoint,
    "/<uuid:note_id>",
    endpoint=endpoints.UpdateNoteEndPoint.NAME,
)
namespace_notes.add_resource(
    endpoints.DeleteNoteEndPoint,
    "/<uuid:note_id>",
    endpoint=endpoints.DeleteNoteEndPoint.NAME,
)
