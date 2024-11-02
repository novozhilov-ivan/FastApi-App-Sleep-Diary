from src.application.api.routers.auth.login import router as router_login
from src.application.api.routers.auth.me import router as router_me
from src.application.api.routers.auth.register import router as router_register


__all__ = (
    "router_login",
    "router_me",
    "router_register",
)
