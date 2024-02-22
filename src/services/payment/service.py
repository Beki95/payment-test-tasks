from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db import (
    Transactions,
    User,
)
from src.interfaces.repositories.alchemy.balance import IBalanceRepository
from src.interfaces.repositories.alchemy.transactions import ITransactionsRepository
from src.services.payment.exceptions import (
    InsufficientFundsError,
    NoBalanceError,
)
from src.services.payment.request_dto import PaymentRequest
from src.services.payment.response_dto import PaymentResponse


class PaymentService:

    def __init__(
        self,
        session: AsyncSession,
        transaction_repo: ITransactionsRepository,
        balance_repo: IBalanceRepository,
    ):
        self.session = session
        self.transaction_repo = transaction_repo
        self.balance_repo = balance_repo

    async def execute(self, user: User, dto: PaymentRequest):
        if not (balance_obj := user.balance): raise NoBalanceError
        if balance_obj.balance <= 0: raise NoBalanceError
        elif dto.amount > balance_obj.balance: raise InsufficientFundsError
        try:
            async with self.session:  # Begin
                # Withdrawal of funds from the balance
                remains = float(balance_obj.balance) - dto.amount
                remains = await self.balance_repo.withdraw_funds(
                    user_id=user.id, amount=remains,
                )
                transaction = Transactions(
                    amount=dto.amount,
                    user_id=user.id,
                    reason_type=dto.reason_type,
                )
                await self.transaction_repo.add_transaction(instance=transaction)
                await self.session.commit()
        except Exception as err:
            print(err)
            await self.session.rollback()
            return PaymentResponse(
                success=False, description='A transaction error has occurred'
            )
        return PaymentResponse(success=True, description='Your balance: {}'.format(remains))
