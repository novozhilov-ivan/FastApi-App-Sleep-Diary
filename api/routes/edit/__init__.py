from flask_restx import Namespace

from api.exceptions.handlers import handler_not_found_404

ns_edit = Namespace(
    name='edit',
    description='Описание edit sleep diary',
    path='/edit',
    validate=True
)
ns_edit.errorhandler(handler_not_found_404)
