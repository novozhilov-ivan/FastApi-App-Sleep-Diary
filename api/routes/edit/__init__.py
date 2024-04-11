from flask_restx import Namespace

ns_edit = Namespace(
    name='edit',
    description='Описание edit sleep diary',
    path='/',
    validate=True
)

from api.routes.edit.route_edit import EditRoute
ns_edit.add_resource(EditRoute, '/edit')
