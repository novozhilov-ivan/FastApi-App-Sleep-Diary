from flask_restx import Resource

from api.CRUD.sleep_note_table import delete_all_user_notes
from api.routes.edit import ns_edit, response_model_422
from api.routes.edit.delete_diary import response_model_204
from api.utils.auth import UserActions
from common.baseclasses.status_codes import HTTP


class EditRouteDelete(Resource, UserActions):
    """Удаление всех записей их дневник сна"""

    @ns_edit.response(**response_model_204)
    @ns_edit.response(**response_model_422)
    @ns_edit.doc(description=__doc__)
    def delete(self):
        delete_all_user_notes(user_id=self.current_user_id)
        return None, HTTP.NO_CONTENT_204
