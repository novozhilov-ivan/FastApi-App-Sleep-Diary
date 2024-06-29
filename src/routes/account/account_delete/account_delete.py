from src.CRUD.user_table import delete_user_by_id
from src.routes.account import (
    ns_account,
    response_model_401,
)
from src.routes.account.account_delete import response_model_204
from src.utils.auth import UserActions
from src.utils.status_codes import HTTP


class DeleteAccount(UserActions):
    """Удаление аккаунта пользователя"""

    @ns_account.response(**response_model_204)
    @ns_account.response(**response_model_401)
    @ns_account.doc(description=__doc__)
    def delete(self):
        delete_user_by_id(self.current_user_id)
        return None, HTTP.NO_CONTENT_204
