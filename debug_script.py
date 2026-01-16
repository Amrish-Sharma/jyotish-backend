import asyncio
from app.service.kundli_service import KundliService
from app.models.kundli import KundliRequest
from app.core.config import settings

# Mock settings if needed, but defaults should work
# We need to mock CacheService or ensure Redis is reachable.
# Since we are running outside of test mock, it will try to connect to Redis.
# If Redis is not running, it will fail.
# I'll mock CacheService in the script.

from unittest.mock import AsyncMock, patch

async def main():
    with patch("app.service.kundli_service.CacheService") as MockCache:
        mock_instance = MockCache.return_value
        mock_instance.get = AsyncMock(return_value=None)
        mock_instance.set = AsyncMock()
        
        service = KundliService()
        
        request = KundliRequest(
            dob="1989-02-24",
            tob="16:30:00",
            lat=28.5355,
            lon=77.3910,
            timezone=5.5,
            ayanamsa=1
        )
        
        print("Generating Kundli...")
        
        # Direct debug of swe.houses
        import swisseph as swe
        from app.engine.core.time_astronomy import TimeAstronomy
        from datetime import datetime, timedelta
        
        dt = datetime.strptime("1989-02-24 16:30:00", "%Y-%m-%d %H:%M:%S")
        dt_utc = dt - timedelta(hours=5.5)
        jd = TimeAstronomy.to_julian_day(dt_utc)
        lat = 28.5355
        lon = 77.3910
        
        print(f"JD: {jd}, Lat: {lat}, Lon: {lon}")
        cusps, ascmc = swe.houses(jd, lat, lon, b'W')
        print(f"Cusps type: {type(cusps)}")
        print(f"Cusps len: {len(cusps)}")
        print(f"Cusps: {cusps}")
        
        try:
            response = await service.generate_kundli(request)
            print("Success!")
            print(response.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
