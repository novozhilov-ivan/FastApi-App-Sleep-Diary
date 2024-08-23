from flask_restx import Namespace

from src.application.api.namespaces.main.endpoint import MainEndpoint


namespace_main = Namespace(
    name="Main",
    description="Основная страница с описанием",
    path="/",
)
namespace_main.add_resource(
    MainEndpoint,
    "/main",
    endpoint=MainEndpoint.NAME,
)
