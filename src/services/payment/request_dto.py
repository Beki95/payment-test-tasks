from pydantic import BaseModel
from pydantic import Field

from src.core.enums.reason_type import ReasonType


class PaymentRequest(BaseModel):
    amount: float = Field(ge=0.1)
    reason_type: ReasonType
