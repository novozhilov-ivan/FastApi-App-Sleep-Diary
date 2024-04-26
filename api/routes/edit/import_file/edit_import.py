import sqlalchemy
from flask import request, Response, Flask
from flask_restx import Resource
from flask_restx.reqparse import Argument

from api import configuration
from api.CRUD.notation_queries import create_many_notes
from api.models import Notation
from api.routes.edit import ns_edit, response_model_422
from api.routes.sleep import user_id_params
from api.utils.manage_notes import FileDataConverter
from common.baseclasses.status_codes import HTTP
from api.routes.edit.import_file import (
    import_file_payload,
    allowed_file_extensions,
    import_response_model_201,
    import_response_model_400,
    import_response_model_409,
    import_response_model_413,
    import_response_model_415,
    import_response_created_201,
    import_response_bad_request_400,
    import_response_conflict_409,
    import_response_content_too_large_413,
    import_response_unsupported_media_type_415,
)
from common.pydantic_schemas.user import User


class EditRouteImport(Resource):
    @ns_edit.doc(description='Импортирование новых записей в дневник сна из файла')
    @ns_edit.expect(user_id_params, import_file_payload)
    @ns_edit.response(**import_response_model_201)
    @ns_edit.response(**import_response_model_400)
    @ns_edit.response(**import_response_model_409)
    @ns_edit.response(**import_response_model_413)
    @ns_edit.response(**import_response_model_415)
    @ns_edit.response(**response_model_422)
    def post(self):
        payload_arg: Argument
        arg: Argument
        payload_arg, *_ = import_file_payload.args
        args = request.args.to_dict()
        file = request.files.get(payload_arg.name)
        if file is None or not args:
            return Response(import_response_bad_request_400, HTTP.BAD_REQUEST_400)
        if file.content_length > configuration.MAX_CONTENT_LENGTH:
            return Response(import_response_content_too_large_413, HTTP.CONTENT_TOO_LARGE_413)
        *_, file_extension = file.filename.split('.')
        if file_extension not in allowed_file_extensions:
            return Response(import_response_unsupported_media_type_415, HTTP.UNSUPPORTED_MEDIA_TYPE_415)

        user = User(**args)
        new_notes = FileDataConverter(file=file)
        new_notes.to_model(Notation, **user.model_dump(by_alias=True))
        new_notes = new_notes.data

        try:
            create_many_notes(new_notes)
        except sqlalchemy.exc.IntegrityError:
            return Response(import_response_conflict_409, HTTP.CONFLICT_409)

        return Response(import_response_created_201, HTTP.CREATED_201)
