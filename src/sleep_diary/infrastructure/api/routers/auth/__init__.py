from fastapi import APIRouter, Depends

from src.sleep_diary.infrastructure.api.dependecies import get_token_bearer
from src.sleep_diary.infrastructure.api.routers.auth import login, me, register


auth_router_with_jwt_dependency = APIRouter(
    dependencies=[Depends(get_token_bearer)],
)
auth_router_with_jwt_dependency.include_router(me.router)

auth_router = APIRouter()
auth_router.include_router(login.router)
auth_router.include_router(register.router)

router = APIRouter(prefix="/auth")
router.include_router(auth_router)
router.include_router(auth_router_with_jwt_dependency)

__all__ = ("router",)
