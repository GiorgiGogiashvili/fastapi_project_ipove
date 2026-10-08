from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Specialist


def calculate_match_score(specialist: Specialist) -> float:
    rating_score = (specialist.rating / 5) * 70
    price_score = max(0, 20 - specialist.price / 10)
    boost_score = min(specialist.boost_score, 10)

    total_score = rating_score + price_score + boost_score

    return round(min(total_score, 100), 2)


def find_specialists(
    db: Session,
    service_code: str,
    city: str,
) -> list[dict]:
    query = select(Specialist).where(
        Specialist.service_code == service_code,
        Specialist.city == city,
        Specialist.available.is_(True),
    )

    specialists = db.scalars(query).all()

    results = []

    for specialist in specialists:
        results.append(
            {
                "id": specialist.id,
                "name": specialist.name,
                "service_code": specialist.service_code,
                "rating": specialist.rating,
                "price": specialist.price,
                "city": specialist.city,
                "available": specialist.available,
                "boost_score": specialist.boost_score,
                "match_score": calculate_match_score(specialist),
            }
        )

    return sorted(
        results,
        key=lambda specialist: specialist["match_score"],
        reverse=True,
    )