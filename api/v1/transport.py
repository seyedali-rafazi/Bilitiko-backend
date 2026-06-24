"""Transport API endpoints."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from beanie import PydanticObjectId
from models.transport import TransportTrip, TransportRoute


router = APIRouter()


@router.get("/search")
async def search_transport(
    transport_type: str = Query(..., description="Transport type (bus/train)"),
    origin: str = Query(..., description="Origin city"),
    destination: str = Query(..., description="Destination city"),
    departure_date: Optional[str] = Query(
        None, description="Departure date (YYYY-MM-DD)"
    ),
    limit: int = Query(20, ge=1, le=100),
):
    """Search for transport trips."""
    query = TransportTrip.find(
        TransportTrip.transport_type == transport_type,
        TransportTrip.origin == origin,
        TransportTrip.destination == destination,
        TransportTrip.is_active == True,
    )

    trips = await query.limit(limit).to_list()
    return trips


@router.get("/{trip_id}")
async def get_transport_trip(trip_id: str):
    """Get transport trip by ID."""
    try:
        trip = await TransportTrip.get(PydanticObjectId(trip_id))
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transport trip not found"
            )
        return trip
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid trip ID"
        )


@router.get("/routes/popular")
async def get_popular_routes(transport_type: Optional[str] = None):
    """Get popular transport routes."""
    query = TransportRoute.find(TransportRoute.is_active == True)

    if transport_type:
        query = query.find(TransportRoute.transport_type == transport_type)

    routes = await query.sort("+order").to_list()
    return routes


# Made with Bob
