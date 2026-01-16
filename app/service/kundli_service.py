from datetime import datetime, timedelta
from app.models.kundli import KundliRequest, KundliResponse
from app.engine.core.ephemeris import SwissEphemerisProvider
from app.engine.core.time_astronomy import TimeAstronomy
from app.engine.core.calculators import KundliCalculator
from app.engine.dasha.vimshottari import VimshottariDasha
from app.core.cache import CacheService
from app.core.config import settings
import hashlib
import json

class KundliService:
    def __init__(self):
        # Initialize providers
        # In a real app, these might be injected
        self.ephemeris_provider = SwissEphemerisProvider()
        self.calculator = KundliCalculator(self.ephemeris_provider)
        self.cache = CacheService()

    async def generate_kundli(self, request: KundliRequest) -> KundliResponse:
        # 0. Check Cache
        input_hash = self._generate_input_hash(request)
        cache_key = f"kundli:{settings.ENGINE_VERSION}:{input_hash}"
        
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return KundliResponse.model_validate_json(cached_data)

        # 1. Parse Date/Time
        dt_str = f"{request.dob} {request.tob}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        
        # Adjust for timezone to get UTC/Julian Day
        # Input time is Local Time.
        # UTC Time = Local Time - Timezone Offset
        dt_utc = dt - timedelta(hours=request.timezone)
        
        julian_day = TimeAstronomy.to_julian_day(dt_utc)
        
        # 2. Set Ayanamsa
        # Default is Lahiri (1)
        self.ephemeris_provider.set_sidereal_mode(request.ayanamsa)
        ayanamsa_val = TimeAstronomy.get_ayanamsa(julian_day, request.ayanamsa)
        
        # 3. Calculate Planets
        planets = self.calculator.calculate_planet_positions(julian_day, request.ayanamsa)
        
        # 4. Calculate Houses
        houses, ascendant = self.calculator.calculate_houses(julian_day, request.lat, request.lon)
        
        # 5. Map Planets to Houses (Whole Sign)
        self.calculator.map_planets_to_houses(planets, houses, ascendant)
        
        # 6. Calculate Dasha
        # Find Moon
        moon = next(p for p in planets if p.name == "Moon")
        dasha_timeline = VimshottariDasha.calculate(moon.longitude, dt)
        
        # 7. Construct Response
        # Lagna Sign
        lagna_sign = int(ascendant / 30) + 1
        
        response = KundliResponse(
            lagna=ascendant,
            lagna_sign=lagna_sign,
            planets=planets,
            houses=houses,
            ayanamsa_value=ayanamsa_val,
            julian_day=julian_day,
            dasha=dasha_timeline
        )
        
        # 8. Cache Result
        await self.cache.set(cache_key, response.model_dump_json())
        
        return response

    def _generate_input_hash(self, request: KundliRequest) -> str:
        input_str = f"{request.dob}|{request.tob}|{request.lat}|{request.lon}|{request.timezone}|{request.ayanamsa}"
        return hashlib.sha256(input_str.encode()).hexdigest()
