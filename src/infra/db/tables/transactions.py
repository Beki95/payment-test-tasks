import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql

from src.core.enums.reason_type import ReasonType
from src.infra.db.tables.common import Base


class Transactions(Base):
    __tablename__ = "transactions"

    user_id = sa.Column(
        psql.UUID(as_uuid=True),
        sa.ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    amount = sa.Column(
        sa.Numeric(precision=10, scale=2),
        nullable=False,
    )
    reason_type = sa.Column(
        sa.Enum(ReasonType),
        default=ReasonType.WITHDRAW,
        nullable=False,
    )
