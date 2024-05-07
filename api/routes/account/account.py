from flask_restx import Resource

from api.models import User
from api.routes.account import ns_account, response_model_200, response_model_401
from api.utils.auth import get_current_auth_user_for_access
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo


@ns_account.response(**response_model_200)
@ns_account.response(**response_model_401)
class UserAccountRoute(Resource):
    """Информация об аккаунте пользователя"""

    @ns_account.doc(description=__doc__)
    def get(self) -> tuple:
        current_user: User = get_current_auth_user_for_access()
        user: UserInfo = UserInfo.model_validate(current_user)
        return user.model_dump(mode="json"), HTTP.OK_200
