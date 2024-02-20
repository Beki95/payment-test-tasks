from fastapi import FastAPI

from src.api.controller.register import bind_routes
from src.api.exceptions.register import register_exceptions
from src.api.register_dependencies import register_dependencies


def initialize_app(_app: FastAPI) -> FastAPI:
    _app.include_router(bind_routes())
    register_dependencies(_app)
    register_exceptions(_app)
    return _app


app = initialize_app(
    FastAPI(),
)
