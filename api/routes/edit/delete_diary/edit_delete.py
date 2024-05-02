from flask import request
from flask_restx import Resource

from api.CRUD.notation_queries import delete_all_user_notes
from api.routes.edit import ns_edit, response_model_422
from api.routes.edit.delete_diary import response_model_204
from api.routes.sleep import user_id_params
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import User


class EditRouteDelete(Resource):
    """Удаление всех записей их дневник сна"""

    @ns_edit.doc(description=__doc__)
    @ns_edit.expect(user_id_params)
    @ns_edit.response(**response_model_204)
    @ns_edit.response(**response_model_422)
    def delete(self):
        user = User(**request.args)
        delete_all_user_notes(user.id)
        return None, HTTP.NO_CONTENT_204
