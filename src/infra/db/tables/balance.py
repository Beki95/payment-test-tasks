import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql

from src.infra.db.tables.common import Base


class UserBalance(Base):
    __tablename__ = "balance"

    user_id = sa.Column(
        psql.UUID(as_uuid=True),
        sa.ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )
    balance = sa.Column(
        sa.Numeric(precision=10, scale=2),
        default=100,
        nullable=False,
    )
    user = sa.orm.relationship(
        'User',
        lazy='joined',
        uselist=False,
        back_populates='balance',
    )
