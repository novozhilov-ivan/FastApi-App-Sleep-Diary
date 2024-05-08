from flask_restx import Resource

from api.routes.account import response_model_401
from api.routes.auth import ns_auth
from api.routes.auth.sign_out import response_model_200, response_ok_200
from api.routes.edit import response_model_422
from api.utils.jwt import validate_auth_token
from common.baseclasses.status_codes import HTTP


@ns_auth.response(**response_model_200)
@ns_auth.response(**response_model_401)
@ns_auth.response(**response_model_422)
class DeAuthUserRoute(Resource):
    """Выход пользователя из аккаунта"""

    @ns_auth.doc(description=__doc__)
    @validate_auth_token
    def post(self) -> tuple:
        # TODO удалить действительные токены; Обращения, с использованием
        #  удаленного токена, должны быть отклонены и без токена тоже.
        return response_ok_200, HTTP.OK_200
