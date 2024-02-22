from pydantic import BaseModel

from src.core.enums.reason_type import ReasonType


class PaymentRequest(BaseModel):
    amount: float
    reason_type: ReasonType
