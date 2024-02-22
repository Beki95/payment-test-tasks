from pydantic import BaseModel


class PaymentResponse(BaseModel):
    success: bool
    description: str
