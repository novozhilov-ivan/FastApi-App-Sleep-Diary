from flask_restx import Resource

from api.routes.edit import ns_edit


class EditRoute(Resource):
    @ns_edit.doc(description='Главная страница с описанием приложения')
    def get(self):
        pass
