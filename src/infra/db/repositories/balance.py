from uuid import UUID

from sqlalchemy import update, func, Numeric

from src.infra.db import UserBalance
from src.infra.db.repositories.common import CommonRepository
from src.interfaces.repositories.alchemy.balance import IBalanceRepository


class BalanceRepository(CommonRepository, IBalanceRepository):

    def add_balance(self, instance: UserBalance) -> None:
        self.session.add(instance)

    async def withdraw_funds(self, user_id: UUID, amount: float) -> None:
        query = (
            update(UserBalance)
            .where(UserBalance.user_id == user_id)
            .values(balance=amount)
            .returning(func.cast(UserBalance.balance, Numeric(scale=2)))
        )
        result = await self.session.execute(query)
        return result.scalar()
