from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    payment_method: str = "test_card"


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    booking_id: int
    user_id: int
    amount: float
    platform_fee: float
    provider_amount: float
    payment_method: str
    transaction_id: str
    status: str
    created_at: datetime