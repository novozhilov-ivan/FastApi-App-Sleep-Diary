from flask_restx import Namespace

from src.application.api.namespaces.notes import endpoints


namespace_notes = Namespace(
    name="Notes",
    description="Действия с записями дневника",
    path="/note",
    # decorators=[validate_auth_token],
)

namespace_notes.add_resource(
    endpoints.AddNoteEndPoint,
    "/add_note",
    endpoint=endpoints.AddNoteEndPoint.NAME,
)
namespace_notes.add_resource(
    endpoints.GetNoteByOidEndPoint,
    "/<uuid:oid>",
    endpoint=endpoints.GetNoteByOidEndPoint.NAME,
)
namespace_notes.add_resource(
    endpoints.GetNoteByBedtimeDateEndPoint,
    "/<string:bedtime_date>",
    endpoint=endpoints.GetNoteByBedtimeDateEndPoint.NAME,
)
namespace_notes.add_resource(
    endpoints.UpdateNoteEndPoint,
    "/update_note",
    endpoint=endpoints.UpdateNoteEndPoint.NAME,
)
namespace_notes.add_resource(
    endpoints.DeleteNoteEndPoint,
    "/delete_note",
    endpoint=endpoints.DeleteNoteEndPoint.NAME,
)
