from flask_restx import Namespace

from src.application.api.namespaces.main.endpoint import MainEndPoint


namespace_main = Namespace(
    name="Main",
    description="Основная страница с описанием цели приложения",
    path="/",
)
namespace_main.add_resource(
    MainEndPoint,
    "/main",
    endpoint=MainEndPoint.NAME,
)
