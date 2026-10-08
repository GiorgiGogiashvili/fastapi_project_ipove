from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models import Booking, Payment, User
from app.schemas.payment import PaymentCreate, PaymentResponse


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


PLATFORM_COMMISSION = 0.10


@router.post(
    "/booking/{booking_id}",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def pay_for_booking(
    booking_id: int,
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    booking = db.get(Booking, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot pay for this booking",
        )

    if booking.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This booking cannot be paid",
        )

    amount = booking.price
    platform_fee = round(amount * PLATFORM_COMMISSION, 2)
    provider_amount = round(amount - platform_fee, 2)

    payment = Payment(
        booking_id=booking.id,
        user_id=current_user.id,
        amount=amount,
        platform_fee=platform_fee,
        provider_amount=provider_amount,
        payment_method=payment_data.payment_method,
        transaction_id=f"TEST-{uuid4()}",
        status="succeeded",
    )

    booking.status = "paid"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment