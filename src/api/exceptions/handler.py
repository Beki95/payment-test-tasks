from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.services.exceptions import (
    AccessDeniedError,
    AuthenticationError,
    TokenExpiredOrNotValid,
)


def token_expired_or_not_valid(request: Request, exc: TokenExpiredOrNotValid):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content=dict(detail=exc.message)
    )


def auth_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content=dict(detail=exc.message)
    )


def access_denied_error_handler(request: Request, exc: AccessDeniedError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content=dict(detail=exc.message)
    )


def not_found_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content=dict(detail=exc.message)  # noqa
    )


def logic_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=dict(detail=exc.message)  # noqa
    )
