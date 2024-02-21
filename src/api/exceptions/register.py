from fastapi import FastAPI

from src.api.exceptions.handler import (
    access_denied_error_handler,
    auth_error_handler,
    token_expired_or_not_valid,
)
from src.services.exceptions import (
    AccessDeniedError,
    AuthenticationError,
    TokenExpiredOrNotValid,
)


def register_exceptions(app: FastAPI) -> None:
    app.exception_handlers.setdefault(
        TokenExpiredOrNotValid, token_expired_or_not_valid,
    )
    app.exception_handlers.setdefault(
        AuthenticationError, auth_error_handler,
    )
    app.exception_handlers.setdefault(
        AccessDeniedError, access_denied_error_handler,
    )