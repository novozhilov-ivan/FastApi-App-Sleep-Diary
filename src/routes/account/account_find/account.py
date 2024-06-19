from flask_restx import abort

from src.CRUD.user_table import find_user_by_id
from src.models import UserOrm
from src.pydantic_schemas.user import UserInfo
from src.routes.account import ns_account, response_model_401
from src.routes.account.account_find import (
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from src.utils.auth import UserActions
from src.utils.status_codes import HTTP


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
