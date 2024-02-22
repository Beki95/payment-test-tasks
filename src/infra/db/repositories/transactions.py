from sqlalchemy import Transaction

from src.infra.db.repositories.common import CommonRepository
from src.interfaces.repositories.alchemy.transactions import ITransactionsRepository


class TransactionsRepository(CommonRepository, ITransactionsRepository):
    async def add_transaction(self, instance: Transaction):
        self.session.add(instance)
