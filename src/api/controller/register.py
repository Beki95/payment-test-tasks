from fastapi import APIRouter

from src.api.controller.auth import auth as auth_router


def bind_routes():
    router = APIRouter(prefix='/api')
    router.include_router(auth_router)
    return router
