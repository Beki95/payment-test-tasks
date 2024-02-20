from fastapi import (
    APIRouter,
    Depends,
)
from starlette.responses import Response

from src.interfaces.repositories.users import IUsersRepository
from src.services.auth.request_dto import UserLoginRequest
from src.services.auth.service import (
    AuthLogoutService,
    AuthorizationService,
)
from src.services.common import get_current_user

auth = APIRouter(prefix='/auth', tags=['auth'])


@auth.post('/login')
async def login(
    dto: UserLoginRequest, repo: IUsersRepository = Depends(),
):
    service = AuthorizationService(repo=repo)
    return await service.authenticate(dto=dto, response=Response())


@auth.post('/logout')
async def logout(_: get_current_user = Depends()):
    service = AuthLogoutService()
    return await service.logout()
