from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    specialist_id: int
    appointment_at: datetime


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    specialist_id: int
    service_code: str
    appointment_at: datetime
    price: float
    status: str
    created_at: datetime