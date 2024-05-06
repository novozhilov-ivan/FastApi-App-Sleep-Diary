from flask import request
from flask_restx import Resource

from api.routes.account import ns_account, response_model_200, response_model_401
from api.utils.user import get_current_auth_user, get_current_token_payload
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo


@ns_account.response(**response_model_401)
class UserAccountRoute(Resource):
    """Информация об аккаунте пользователя"""

    @ns_account.doc(description=__doc__)
    @ns_account.response(**response_model_200)
    def get(self):
        credentials = request.headers.get("Authorization")
        payload = get_current_token_payload(credentials)
        current_user = get_current_auth_user(payload)
        user = UserInfo.model_validate(current_user)
        return user.model_dump(mode="json"), HTTP.OK_200
