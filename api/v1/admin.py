"""
Admin API endpoints.

All routes are protected by the X-Admin-Key header which must match the
SECRET_KEY value in your .env file.  No JWT / user account required.

POST /api/v1/admin/seed          — generate data for the next N days
POST /api/v1/admin/seed/clean    — wipe future data then regenerate
GET  /api/v1/admin/seed/status   — count of existing records per collection
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

from core.config import settings
from core.seeder import run_full_seed, clean_future_data
from models.flight import Flight, City, PopularFlight
from models.transport import TransportTrip, TransportRoute


router = APIRouter()


# ── Auth helper ───────────────────────────────────────────────────────────────

def _require_admin_key(x_admin_key: Optional[str]) -> None:
    """Raise 403 if the provided key doesn't match SECRET_KEY."""
    if not x_admin_key or x_admin_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing X-Admin-Key header",
        )


# ── Request / Response schemas ────────────────────────────────────────────────

class SeedRequest(BaseModel):
    days: int = Field(default=7, ge=1, le=30, description="How many future days to populate")
    trips_per_pair: int = Field(default=3, ge=1, le=10, description="Trips per city-pair per day")
    clean: bool = Field(default=False, description="Delete existing future data before seeding")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/seed", status_code=status.HTTP_200_OK)
async def seed_data(
    body: SeedRequest = SeedRequest(),
    x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key"),
):
    """
    Generate sample flights, buses and trains for all city permutations.

    Protected by **X-Admin-Key** header — set it to the value of your SECRET_KEY.

    - `days` — how many future days to cover (default 7, max 30)
    - `trips_per_pair` — how many trips to create per city-pair per day (default 3)
    - `clean` — if `true`, wipe existing future data first then regenerate
    """
    _require_admin_key(x_admin_key)

    started_at = datetime.utcnow()
    result = await run_full_seed(
        days=body.days,
        trips_per_pair=body.trips_per_pair,
        clean=body.clean,
    )
    elapsed = (datetime.utcnow() - started_at).total_seconds()

    return {
        "success": True,
        "elapsed_seconds": round(elapsed, 2),
        "summary": result,
    }


@router.delete("/seed/future", status_code=status.HTTP_200_OK)
async def delete_future_data(
    days: int = 7,
    x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key"),
):
    """
    Delete all flights and transport trips departing within the next `days` days.

    Protected by **X-Admin-Key** header.
    """
    _require_admin_key(x_admin_key)

    result = await clean_future_data(days)
    return {"success": True, "deleted": result}


@router.get("/seed/status", status_code=status.HTTP_200_OK)
async def seed_status(
    x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key"),
):
    """
    Return a count of records in each collection so you can verify seeding worked.

    Protected by **X-Admin-Key** header.
    """
    _require_admin_key(x_admin_key)

    today  = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    future = today + timedelta(days=7)

    return {
        "cities": await City.find_all().count(),
        "popular_flights": await PopularFlight.find_all().count(),
        "popular_transport_routes": await TransportRoute.find_all().count(),
        "flights_total": await Flight.find_all().count(),
        "flights_next_7_days": await Flight.find(
            Flight.departure_time >= today,
            Flight.departure_time < future,
        ).count(),
        "transport_trips_total": await TransportTrip.find_all().count(),
        "transport_trips_next_7_days": await TransportTrip.find(
            TransportTrip.departure_time >= today,
            TransportTrip.departure_time < future,
        ).count(),
        "checked_at": today.isoformat(),
    }


# Made with Bob
