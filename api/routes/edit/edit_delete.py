from flask_restx import Resource

from api.routes.edit import ns_edit


class EditRouteDelete(Resource):
    @ns_edit.doc(description='Удаление всех записей их дневник сна')
    def delete(self):
        pass
