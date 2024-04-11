from flask_restx import Resource

from api.routes.edit import ns_edit


class EditRouteImport(Resource):
    @ns_edit.doc(description='Импортирование новых записей в дневник сна из файла')
    def post(self):
        pass
