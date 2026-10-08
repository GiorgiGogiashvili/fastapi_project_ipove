from pydantic import BaseModel


class SpecialistResponse(BaseModel):
    id: int
    name: str
    service_code: str
    rating: float
    price: float
    city: str
    available: bool
    boost_score: float
    match_score: float