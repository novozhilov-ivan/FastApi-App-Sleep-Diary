from flask_restx import Namespace


namespace_main = Namespace(
    name="Main",
    description="Основная страница с описанием",
    path="/",
)
