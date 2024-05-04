from flask_restx import Resource

from api.routes.main import ns_main, response_model_200
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.main import MainPageModel


class MainRoute(Resource):
    """Главная страница с описанием приложения"""

    @ns_main.doc(description=__doc__)
    @ns_main.response(**response_model_200)
    def get(self):
        return MainPageModel().model_dump(), HTTP.OK_200
