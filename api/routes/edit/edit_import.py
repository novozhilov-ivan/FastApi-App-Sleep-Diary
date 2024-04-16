from flask_restx import Resource

from api.routes.edit import ns_edit, import_response_model_200, csv_file_payload
from api.routes.sleep import user_id_params


class EditRouteImport(Resource):
    @ns_edit.doc(description='Импортирование новых записей в дневник сна из файла')
    @ns_edit.expect(user_id_params, csv_file_payload)
    @ns_edit.response(**import_response_model_200)
    def post(self):
        pass
