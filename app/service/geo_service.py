from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from pydantic import BaseModel
from typing import List, Optional

class City(BaseModel):
    name: str
    lat: float
    lon: float
    timezone: str
    country: str

class GeoService:
    def __init__(self):
        # Initialize Nominatim with a specific user agent
        self.geolocator = Nominatim(user_agent="jyotish-backend")
        self.tf = TimezoneFinder()

    async def search_city(self, query: str) -> List[City]:
        """
        Search for cities by name using Nominatim.
        Restricted to 5 results for relevance.
        """
        try:
            # Nominatim is synchronous, wrap in try-except block
            # In a high-load async environment, this should ideally be run in a threadpool
            locations = self.geolocator.geocode(query, exactly_one=False, limit=5, language="en")
            
            cities = []
            if locations:
                for loc in locations:
                    # Get timezone for coordinates
                    tz_str = self.tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
                    if not tz_str:
                        tz_str = "UTC" # Fallback
                    
                    # Convert to numeric offset
                    from zoneinfo import ZoneInfo
                    import datetime
                    
                    try:
                        timezone = ZoneInfo(tz_str)
                        # We need offset for today
                        now = datetime.datetime.now(timezone)
                        offset_seconds = now.utcoffset().total_seconds()
                        offset_hours = offset_seconds / 3600.0
                    except Exception as e:
                        print(f"Error converting timezone: {e}")
                        offset_hours = 0.0

                    # Extract country
                    address_components = loc.raw.get('address', {})
                    country = address_components.get('country', '')
                    
                    cities.append(City(
                        name=loc.address,
                        lat=loc.latitude,
                        lon=loc.longitude,
                        timezone=str(offset_hours), # Return string of float for consistency with model? No model says str.
                        country=country
                    ))
            return cities
        except Exception as e:
            print(f"Error searching city: {e}")
            return []
