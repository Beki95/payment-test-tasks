from pydantic import BaseModel


class BlockedIdModel(BaseModel):
    attempt: int
    exp: int | None
