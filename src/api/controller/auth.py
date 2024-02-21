from fastapi import (
    APIRouter,
    Depends,
)
from starlette.requests import Request
from starlette.responses import Response

from src.interfaces.repositories.alchemy.users import IUsersRepository
from src.interfaces.repositories.redis._ip import IBlockedIPRepository
from src.services.auth.request_dto import UserLoginRequest
from src.services.auth.service import (
    AuthLogoutService,
    AuthorizationService,
)
from src.services.common import (
    LockoutManager,
    get_current_user,
)

auth = APIRouter(prefix='/auth', tags=['auth'])


@auth.post('/login')
async def login(
    request: Request,
    dto: UserLoginRequest,
    blocked_cache_repo: IBlockedIPRepository = Depends(),
    repo: IUsersRepository = Depends(),
):
    lockout_manager = LockoutManager(request=request, blocked_cache_repo=blocked_cache_repo)
    service = AuthorizationService(repo=repo, lockout_manager=lockout_manager)
    return await service.authenticate(dto=dto, response=Response())


@auth.post('/logout')
async def logout(_: get_current_user = Depends()):
    service = AuthLogoutService()
    return await service.logout()
