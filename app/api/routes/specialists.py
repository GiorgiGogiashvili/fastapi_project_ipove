from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.recommender import find_specialists


router = APIRouter(
    prefix="/specialists",
    tags=["Specialists"],
)


@router.get("/recommend")
def recommend_specialists(
    service_code: str,
    city: str = "Tbilisi",
    db: Session = Depends(get_db),
):
    return find_specialists(
        db=db,
        service_code=service_code,
        city=city,
    )