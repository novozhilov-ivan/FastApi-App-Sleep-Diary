from flask import request
from flask_restx import Resource
from flask_restx.reqparse import Argument

from src.CRUD.sleep_note_table import create_many_notes
from src.config import flask_config
from src.models import SleepNoteOrm
from src.routes.edit import ns_edit, response_model_422
from src.routes.edit.import_file import (
    allowed_file_extensions,
    import_file_payload,
    response_bad_request_400,
    response_conflict_409,
    response_content_too_large_413,
    response_created_201,
    response_model_201,
    response_model_400,
    response_model_409,
    response_model_413,
    response_model_415,
    response_unsupported_media_type_415,
)
from src.utils.auth import UserActions
from src.utils.manage_notes import FileDataConverter
from src.utils.status_codes import HTTP


class EditRouteImport(Resource, UserActions):
    """Импортирование новых записей в дневник сна из файла"""

    @ns_edit.doc(description=__doc__)
    @ns_edit.expect(import_file_payload)
    @ns_edit.response(**response_model_201)
    @ns_edit.response(**response_model_400)
    @ns_edit.response(**response_model_409)
    @ns_edit.response(**response_model_413)
    @ns_edit.response(**response_model_415)
    @ns_edit.response(**response_model_422)
    def post(self):
        payload_arg: Argument
        payload_arg, *_ = import_file_payload.args
        file = request.files.get(payload_arg.name)
        if file is None:
            return response_bad_request_400, HTTP.BAD_REQUEST_400
        if file.content_length > flask_config.MAX_CONTENT_LENGTH:
            return response_content_too_large_413, HTTP.CONTENT_TOO_LARGE_413
        *_, file_extension = file.filename.split(".")
        if file_extension not in allowed_file_extensions:
            return (
                response_unsupported_media_type_415,
                HTTP.UNSUPPORTED_MEDIA_TYPE_415,
            )
        new_notes = FileDataConverter(file=file)
        new_notes.to_model(
            as_model=SleepNoteOrm,
            owner_id=self.current_user_id,
        )

        if create_many_notes(new_notes.data):
            return response_created_201, HTTP.CREATED_201
        return response_conflict_409, HTTP.CONFLICT_409
