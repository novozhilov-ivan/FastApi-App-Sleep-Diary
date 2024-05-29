from api.CRUD.users import delete_user_by_id
from api.routes.account import ns_account, response_model_401
from api.routes.account.account_delete import response_model_204
from api.utils.auth import get_current_auth_user_id_for_access
from common.baseclasses.status_codes import HTTP


class DeleteAccount:
    """Удаление аккаунта пользователя"""

    @ns_account.response(**response_model_204)
    @ns_account.response(**response_model_401)
    @ns_account.doc(description=__doc__)
    def delete(self):
        current_user_id: int = get_current_auth_user_id_for_access()
        delete_user_by_id(current_user_id)
        return None, HTTP.NO_CONTENT_204
