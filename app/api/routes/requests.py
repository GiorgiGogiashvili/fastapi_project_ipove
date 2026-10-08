from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.request import (
    RequestAnalysis,
    SearchResponse,
    UserRequest,
)
from app.services.analyzer import detect_service
from app.services.recommender import find_specialists


router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)


@router.post("/analyze", response_model=RequestAnalysis)
def analyze_request(user_request: UserRequest):
    return detect_service(
        text=user_request.text,
        language=user_request.language,
    )


@router.post("/search", response_model=SearchResponse)
def search_specialists(
    user_request: UserRequest,
    db: Session = Depends(get_db),
):
    analysis = detect_service(
        text=user_request.text,
        language=user_request.language,
    )

    specialists = find_specialists(
        db=db,
        service_code=analysis.service_code,
        city=user_request.city,
    )

    return SearchResponse(
        analysis=analysis,
        specialists=specialists,
    )