from datetime import datetime, timedelta
from app.models.kundli import KundliRequest, KundliResponse
from app.engine.core.ephemeris import SwissEphemerisProvider
from app.engine.core.time_astronomy import TimeAstronomy
from app.engine.core.calculators import KundliCalculator
from app.engine.dasha.vimshottari import VimshottariDasha
from app.engine.core.panchang import PanchangCalculator
from app.engine.core.vedic_attributes import VedicAttributes
from app.models.kundli import KundliRequest, KundliResponse, BasicDetails, GhatakDetails
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
        sun = next(p for p in planets if p.name == "Sun")
        
        dasha_timeline = VimshottariDasha.calculate(moon.longitude, dt)
        
        # 7a. Calculate Panchang
        panchang = PanchangCalculator.calculate_panchang(julian_day, sun.longitude, moon.longitude, dt)
        
        # 7b. Calculate Vedic Attributes
        # Need Moon Nakshatra Index and Moon Sign Index
        # Nakshatra is 0-26, Sign is 1-12
        moon_nak_idx = moon.nakshatra # 0-26
        moon_sign_idx = moon.sign # 1-12
        
        avakahada = VedicAttributes.get_avakahada(moon_nak_idx, moon_sign_idx)
        ghatak_raw = VedicAttributes.get_ghatak(moon_sign_idx)
        
        # 7c. Construct Details Models
        
        # Rasi Lord mapping
        PLANET_LORDS = {
            1: "Mars", 8: "Mars",
            2: "Venus", 7: "Venus",
            3: "Mercury", 6: "Mercury",
            4: "Moon",
            5: "Sun",
            9: "Jupiter", 12: "Jupiter",
            10: "Saturn", 11: "Saturn"
        }
        
        lagna_sign = int(ascendant / 30) + 1
        
        basic_details = BasicDetails(
            ascendant_lord=PLANET_LORDS.get(lagna_sign, "Unknown"),
            rasi_lord=PLANET_LORDS.get(moon_sign_idx, "Unknown"),
            nakshatra_charan=str(moon.pada),
            nakshatra_lord="Unknown", # Need logic, can get from Dasha sequence
            yoga=panchang["yoga"],
            karan=panchang["karan"],
            tithi=panchang["tithi"],
            day=panchang["day"],
            gana=avakahada["gana"],
            yoni=avakahada["yoni"],
            nadi=avakahada["nadi"],
            varan=avakahada["varan"],
            vashya=avakahada["vashya"],
            varga=avakahada["varga"],
            yunja=avakahada["yunja"],
            hansak=avakahada["hansak"],
            paya=avakahada["paya"],
            sunsign_west="Unknown" # TODO implement west sign calc if needed
        )
        
        ghatak_details = GhatakDetails(
            month=ghatak_raw.get("month", "-"),
            tithi=ghatak_raw.get("tithi", "-"),
            day=ghatak_raw.get("day", "-"),
            nakshatra=ghatak_raw.get("nakshatra", "-"),
            yoga="To be implemented", # Ghatak yoga logic needs specific table
            karan="To be implemented",
            prahar="To be implemented",
            varga="To be implemented",
            lagna="To be implemented",
            sun="To be implemented",
            moon="To be implemented", 
            mars="To be implemented",
            mer="To be implemented",
            jup="To be implemented",
            ven="To be implemented",
            sat="To be implemented",
            rah="To be implemented"
        )
        
        # 7d. Construct Response
        response = KundliResponse(
            lagna=ascendant,
            lagna_sign=lagna_sign,
            planets=planets,
            houses=houses,
            ayanamsa_value=ayanamsa_val,
            julian_day=julian_day,
            dasha=dasha_timeline,
            basic_details=basic_details,
            ghatak_details=ghatak_details
        )
        
        # 8. Cache Result
        await self.cache.set(cache_key, response.model_dump_json())
        
        return response

    def _generate_input_hash(self, request: KundliRequest) -> str:
        input_str = f"{request.dob}|{request.tob}|{request.lat}|{request.lon}|{request.timezone}|{request.ayanamsa}"
        return hashlib.sha256(input_str.encode()).hexdigest()
