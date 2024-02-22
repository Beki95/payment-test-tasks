from fastapi import APIRouter

from src.api.controller.auth import auth as auth_router
from src.api.controller.payment import payment as payment_router


def bind_routes():
    router = APIRouter(prefix='/api')
    router.include_router(auth_router)
    router.include_router(payment_router)
    return router
