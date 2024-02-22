from fastapi import (
    APIRouter,
    Depends,
)

from src.interfaces.db import get_session
from src.interfaces.repositories.alchemy.balance import IBalanceRepository
from src.interfaces.repositories.alchemy.transactions import ITransactionsRepository
from src.services.common import get_current_user
from src.services.payment.request_dto import PaymentRequest
from src.services.payment.response_dto import PaymentResponse
from src.services.payment.service import PaymentService

payment = APIRouter(prefix='/payment', tags=['payment'])


@payment.post('/withdraw', response_model=PaymentResponse)
async def payment_withdraw(
    dto: PaymentRequest,
    session: get_session = Depends(),
    user: get_current_user = Depends(),
    transaction_repo: ITransactionsRepository = Depends(),
    balance_repo: IBalanceRepository = Depends(),

):
    service = PaymentService(
        session=session,
        transaction_repo=transaction_repo,
        balance_repo=balance_repo,
    )
    return await service.execute(dto=dto, user=user)
