from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.specialist import SpecialistResponse


Language = Literal["ru", "en", "ka"]


class UserRequest(BaseModel):
    text: str = Field(
        min_length=3,
        max_length=1000,
    )
    language: Language = "en"
    city: str = "Tbilisi"


class RequestAnalysis(BaseModel):
    category: str
    service: str
    service_code: str
    urgency: Literal["low", "medium", "high"]


class SearchResponse(BaseModel):
    analysis: RequestAnalysis
    specialists: list[SpecialistResponse]