from flask_restx import Resource

from src.pydantic_schemas.main import MainPageModel
from src.routes.main import ns_main, response_model_200
from src.utils.status_codes import HTTP


class MainRoute(Resource):
    """Главная страница с описанием приложения"""

    @ns_main.doc(
        description=__doc__,
        security=None,
    )
    @ns_main.response(**response_model_200)
    def get(self):
        return MainPageModel().model_dump(), HTTP.OK_200
