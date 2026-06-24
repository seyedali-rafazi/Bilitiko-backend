"""Insurance API endpoints."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from beanie import PydanticObjectId
from models.insurance import Insurance, InsuranceBooking
from models.user import User
from core.security import get_current_user, get_current_active_user
import random
import string


router = APIRouter()


@router.get("/plans")
async def get_insurance_plans():
    """Get all active insurance plans."""
    plans = (
        await Insurance.find(Insurance.is_active == True)
        .sort([("popular", -1), ("price", 1)])
        .to_list()
    )
    return plans


@router.get("/plans/{plan_id}")
async def get_insurance_plan(plan_id: str):
    """Get insurance plan by ID."""
    try:
        plan = await Insurance.get(PydanticObjectId(plan_id))
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Insurance plan not found"
            )
        return plan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid plan ID"
        )


@router.post("/bookings", status_code=status.HTTP_201_CREATED)
async def create_insurance_booking(
    booking_data: dict, current_user: Optional[User] = Depends(get_current_user)
):
    """Create a new insurance booking."""
    # Generate tracking code
    tracking_code = "INS" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=7)
    )

    # Create booking
    booking = InsuranceBooking(
        plan_id=booking_data.get("plan_id"),
        user_id=str(current_user.id) if current_user else None,
        first_name=booking_data.get("first_name"),
        last_name=booking_data.get("last_name"),
        national_id=booking_data.get("national_id"),
        birth_date=booking_data.get("birth_date"),
        destination=booking_data.get("destination"),
        start_date=booking_data.get("start_date"),
        end_date=booking_data.get("end_date"),
        phone=booking_data.get("phone"),
        email=booking_data.get("email"),
        tracking_code=tracking_code,
    )

    await booking.insert()
    return booking


@router.get("/bookings/my-bookings")
async def get_my_insurance_bookings(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user's insurance bookings."""
    bookings = (
        await InsuranceBooking.find(InsuranceBooking.user_id == str(current_user.id))
        .sort("-created_at")
        .to_list()
    )
    return bookings


@router.get("/bookings/track/{tracking_code}")
async def track_insurance_booking(tracking_code: str):
    """Track insurance booking by tracking code."""
    booking = await InsuranceBooking.find_one(
        InsuranceBooking.tracking_code == tracking_code
    )
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Insurance booking not found"
        )
    return booking


@router.get("/bookings/{booking_id}")
async def get_insurance_booking(
    booking_id: str, current_user: User = Depends(get_current_active_user)
):
    """Get insurance booking by ID."""
    try:
        booking = await InsuranceBooking.get(PydanticObjectId(booking_id))
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insurance booking not found",
            )

        # Check if user owns this booking
        if booking.user_id != str(current_user.id) and not current_user.is_staff:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this booking",
            )

        return booking
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid booking ID"
        )


# Made with Bob
