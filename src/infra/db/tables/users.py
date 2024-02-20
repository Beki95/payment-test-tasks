import sqlalchemy as sa

from src.infra.db.tables.common import Base


class User(Base):
    __tablename__ = "users"

    username = sa.Column(
        sa.String,
        unique=True,
        nullable=False,
    )
    first_name = sa.Column(
        sa.String,
        nullable=True,
    )
    last_name = sa.Column(
        sa.String,
        nullable=True,
    )
    password = sa.Column(
        sa.String(255),
        nullable=False,
    )
