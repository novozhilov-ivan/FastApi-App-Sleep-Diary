from flask_restx import abort

from api.CRUD.users import find_user_by_id
from api.models import UserOrm
from api.routes.account import ns_account, response_model_401
from api.routes.account.account_find import (
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from api.utils.auth import UserActions
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo


class FindAccount(UserActions):
    """Информация об аккаунте пользователя"""

    @ns_account.response(**response_model_200)
    @ns_account.response(**response_model_401)
    @ns_account.response(**response_model_404)
    @ns_account.doc(description=__doc__)
    def get(self) -> tuple:
        db_user: UserOrm | None = find_user_by_id(user_id=self.current_user_id)
        if db_user is None:
            abort(
                code=HTTP.NOT_FOUND_404,
                message=response_not_found_404,
            )
        user: UserInfo = UserInfo.model_validate(db_user)
        return user.model_dump(mode="json"), HTTP.OK_200
