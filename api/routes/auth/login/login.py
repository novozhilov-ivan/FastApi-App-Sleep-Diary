from flask import request
from flask_restx import Resource

from api.routes.auth import ns_auth
from api.routes.auth.login import login_params, response_model_200
from api.routes.edit import response_model_422
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserCredentials


@ns_auth.response(**response_model_200)
@ns_auth.response(**response_model_422)
class LogInRoute(Resource):
    """Авторизация в приложении по логину и паролю"""

    @ns_auth.doc(description=__doc__)
    @ns_auth.expect(login_params)
    @ns_auth.param("payload", description=UserCredentials.__doc__, _in="body")
    def post(self):
        user_credentials = UserCredentials(**request.json)
        return user_credentials.model_dump(), HTTP.OK_200
