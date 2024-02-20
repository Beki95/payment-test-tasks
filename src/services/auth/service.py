from fastapi.openapi.models import Response
from starlette.responses import JSONResponse

from src.core import security
from src.core.const import AC
from src.core.security import verify_password
from src.infra.db import User
from src.interfaces.repositories.users import IUsersRepository
from src.services.auth.request_dto import UserLoginRequest
from src.services.exceptions import AuthenticationError


class AuthorizationService:
    same_site = 'None'
    httponly = True
    secure = True
    token_type = 'Bearer'

    def __init__(self, repo: IUsersRepository):
        self.repo = repo

    async def authenticate_user(self, username: str, password: str) -> None | User:
        user = await self.repo.get_user_by_username(username)

        if user and verify_password(password, user.password):
            return user

    async def authorization_via_cookies(  # noqa
        self, access_token, response: Response,
    ) -> Response:
        response.set_cookie(
            key=AC.ACCESS_TOKEN_KEY, value=access_token, httponly=self.httponly,
            samesite=self.same_site, secure=self.secure,
        )
        response.set_cookie(
            key=AC.TOKEN_TYPE, value=self.token_type, httponly=self.httponly,
            samesite=self.same_site, secure=self.secure,
        )
        return response

    async def authenticate(self, dto: UserLoginRequest, response: Response) -> Response:
        if not (
                user := await self.authenticate_user(username=dto.username, password=dto.password)
        ):
            raise AuthenticationError
        access_token = await security.create_jwt_token(user_id=user.id, scopes=None)

        return await self.authorization_via_cookies(access_token=access_token, response=response)


class AuthLogoutService:

    async def logout(self) -> JSONResponse:  # noqa
        response = JSONResponse(
            content={"message": "Logged out successfully"},
        )
        response.delete_cookie(AC.ACCESS_TOKEN_KEY)
        response.delete_cookie(AC.TOKEN_TYPE)
        return response
