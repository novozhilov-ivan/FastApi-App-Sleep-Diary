from flask_restx import abort

from api.CRUD.users import find_user_by_id
from api.models import User
from api.routes.account import ns_account, response_model_401
from api.routes.account.account_find import response_model_200
from api.utils.auth import get_current_auth_user_id_for_access
from api.utils.jwt import response_invalid_authorization_token_401
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo


@ns_account.response(**response_model_200)
@ns_account.response(**response_model_401)
class FindAccount:
    """Информация об аккаунте пользователя"""

    @ns_account.doc(description=__doc__)
    def get(self) -> tuple:
        current_user_id: int = get_current_auth_user_id_for_access()
        db_user: User | None = find_user_by_id(current_user_id)
        if db_user is None:
            abort(
                code=HTTP.UNAUTHORIZED_401,
                message=response_invalid_authorization_token_401,
            )
        user: UserInfo = UserInfo.model_validate(db_user)
        return user.model_dump(mode="json"), HTTP.OK_200
