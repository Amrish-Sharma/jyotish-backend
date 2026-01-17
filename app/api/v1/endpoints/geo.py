from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.service.geo_service import GeoService, City

router = APIRouter()
geo_service = GeoService()

@router.get("/search", response_model=List[City])
async def search_cities(q: str = Query(..., min_length=2, description="City name to search")):
    """
    Search for cities by name.
    Returns list of matching cities with coordinates and timezone.
    """
    results = await geo_service.search_city(q)
    return results
