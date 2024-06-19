from flask_restx import Resource

from src.routes.account import response_model_401
from src.routes.auth import ns_auth
from src.routes.auth.sign_out import response_model_200, response_ok_200
from src.routes.edit import response_model_422
from src.utils.jwt import validate_auth_token
from src.utils.status_codes import HTTP


class DeAuthUserRoute(Resource):
    """Выход пользователя из аккаунта"""

    @validate_auth_token
    @ns_auth.response(**response_model_200)
    @ns_auth.response(**response_model_401)
    @ns_auth.response(**response_model_422)
    @ns_auth.doc(description=__doc__)
    @ns_auth.deprecated
    def post(self) -> tuple:
        # TODO удалить действительные токены, то есть
        #  добавить пару access и refresh токенов в black list, то есть сделать
        #  недействительными, не дожидаясь истечения срока их жизни
        #  и запрещать все обращения к защищенным эндпоинтам, с использованием
        #  удаленных токенов;
        #  Если при обращении к данному эндпоинту, срок жизни обоих токенов истек,
        #  то не предпринимать ничего, вернуть ответ "User is sign out"
        return response_ok_200, HTTP.OK_200
