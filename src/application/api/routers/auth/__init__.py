from src.application.api.routers.auth.login import router as router_login
from src.application.api.routers.auth.user_info import router as router_me


__all__ = (
    "router_login",
    "router_me",
)
