from flask_restx import Resource
from flask import request, Response

from api.CRUD.notation_queries import delete_all_user_notes
from api.routes.edit import ns_edit, response_model_422
from api.routes.edit.delete_diary import delete_success_response, delete_response_model_200
from api.routes.sleep import user_id_params
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import User


class EditRouteDelete(Resource):
    @ns_edit.doc(description='Удаление всех записей их дневник сна')
    @ns_edit.expect(user_id_params)
    @ns_edit.response(**delete_response_model_200)
    @ns_edit.response(**response_model_422)
    def delete(self):
        args = request.args.to_dict()
        user_id = User(**args).id
        delete_all_user_notes(user_id)
        response = delete_success_response
        return Response(response, HTTP.OK_200)
