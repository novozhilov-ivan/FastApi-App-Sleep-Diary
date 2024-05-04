from flask_restx import Resource

from api.routes.account import ns_account, response_model_200
from api.utils.user import get_current_auth_user
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo


@ns_account.response(**response_model_200)
class UserAccountRoute(Resource):
    """Информация об аккаунте пользователя"""

    @ns_account.doc(description=__doc__)
    def get(self):

        user = UserInfo(**get_current_auth_user())
        return user.model_dump(mode="json"), HTTP.OK_200
