from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Specialist


SPECIALISTS = [
    {
        "name": "Tbilisi Dental Center",
        "service_code": "dentist",
        "rating": 4.9,
        "price": 80,
        "city": "Tbilisi",
        "available": True,
        "boost_score": 0,
    },
    {
        "name": "Healthy Smile Clinic",
        "service_code": "dentist",
        "rating": 4.7,
        "price": 60,
        "city": "Tbilisi",
        "available": True,
        "boost_score": 8,
    },
    {
        "name": "City Laboratory",
        "service_code": "laboratory",
        "rating": 4.8,
        "price": 40,
        "city": "Tbilisi",
        "available": True,
        "boost_score": 2,
    },
]


def seed_specialists():
    db = SessionLocal()

    try:
        for specialist_data in SPECIALISTS:
            existing_specialist = db.scalar(
                select(Specialist).where(
                    Specialist.name == specialist_data["name"]
                )
            )

            if existing_specialist is None:
                specialist = Specialist(**specialist_data)
                db.add(specialist)

        db.commit()
        print("Specialists seeded successfully")

    finally:
        db.close()


if __name__ == "__main__":
    seed_specialists()