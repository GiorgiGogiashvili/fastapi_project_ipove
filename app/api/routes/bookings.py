from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models import Booking, Specialist, User
from app.schemas.booking import BookingCreate, BookingResponse


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    specialist = db.get(
        Specialist,
        booking_data.specialist_id,
    )

    if specialist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialist not found",
        )

    if not specialist.available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Specialist is not available",
        )

    if booking_data.appointment_at <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment time must be in the future",
        )

    existing_booking = db.scalar(
        select(Booking).where(
            Booking.specialist_id == specialist.id,
            Booking.appointment_at == booking_data.appointment_at,
            Booking.status != "cancelled",
        )
    )

    if existing_booking is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This time is already booked",
        )

    booking = Booking(
        user_id=current_user.id,
        specialist_id=specialist.id,
        service_code=specialist.service_code,
        appointment_at=booking_data.appointment_at,
        price=specialist.price,
        status="pending",
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.get(
    "/me",
    response_model=list[BookingResponse],
)
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    bookings = db.scalars(
        select(Booking)
        .where(Booking.user_id == current_user.id)
        .order_by(Booking.created_at.desc())
    ).all()

    return bookings