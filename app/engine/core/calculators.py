import swisseph as swe
from typing import List, Tuple
from app.engine.core.ephemeris import EphemerisProvider
from app.engine.core.time_astronomy import TimeAstronomy
from app.models.kundli import PlanetPosition, House

class KundliCalculator:
    def __init__(self, ephemeris_provider: EphemerisProvider):
        self.ephemeris = ephemeris_provider

    def calculate_planet_positions(self, julian_day: float, ayanamsa_id: int) -> List[PlanetPosition]:
        self.ephemeris.set_sidereal_mode(ayanamsa_id)
        
        planets = []
        # Sun to Ketu (0-9 in standard vedic mapping, but swe has its own IDs)
        # Vedic: Sun(0), Moon(1), Mars(2), Mercury(3), Jupiter(4), Venus(5), Saturn(6), Rahu(7), Ketu(8)
        # Swe: Sun(0), Moon(1), Mercury(2), Venus(3), Mars(4), Jupiter(5), Saturn(6), Uranus(7), Neptune(8), Pluto(9)
        # Nodes: Mean Node (10), True Node (11)
        
        # Mapping:
        # Sun: swe.SUN (0)
        # Moon: swe.MOON (1)
        # Mars: swe.MARS (4)
        # Mercury: swe.MERCURY (2)
        # Jupiter: swe.JUPITER (5)
        # Venus: swe.VENUS (3)
        # Saturn: swe.SATURN (6)
        # Rahu: swe.MEAN_NODE (10) (or TRUE_NODE) - usually Mean Node in traditional
        # Ketu: Opposite of Rahu
        
        planet_ids = [
            (swe.SUN, "Sun"),
            (swe.MOON, "Moon"),
            (swe.MARS, "Mars"),
            (swe.MERCURY, "Mercury"),
            (swe.JUPITER, "Jupiter"),
            (swe.VENUS, "Venus"),
            (swe.SATURN, "Saturn"),
            (swe.MEAN_NODE, "Rahu")
        ]
        
        for pid, name in planet_ids:
            long, lat, dist, speed = self.ephemeris.get_planet_position(pid, julian_day)
            
            # Normalize longitude 0-360
            long = long % 360
            
            # Determine sign (0-11)
            sign = int(long / 30) + 1
            
            # Nakshatra (0-26)
            # 360 / 27 = 13.3333 degrees per nakshatra
            nakshatra_val = long / (360/27)
            nakshatra = int(nakshatra_val) + 1
            
            # Pada (1-4)
            # Each nakshatra has 4 padas. 13.333 / 4 = 3.333 degrees per pada
            pada_val = (long % (360/27)) / (360/108) # 360/108 = 3.3333
            pada = int(pada_val) + 1
            
            # Retrograde?
            is_retrograde = speed < 0
            
            planets.append(PlanetPosition(
                id=pid,
                name=name,
                longitude=long,
                latitude=lat,
                speed=speed,
                sign=sign,
                house=0, # Calculated later
                nakshatra=nakshatra,
                pada=pada,
                is_retrograde=is_retrograde
            ))
            
        # Add Ketu (opposite of Rahu)
        rahu = next(p for p in planets if p.name == "Rahu")
        ketu_long = (rahu.longitude + 180) % 360
        ketu_sign = int(ketu_long / 30) + 1
        ketu_nak = int(ketu_long / (360/27)) + 1
        ketu_pada = int((ketu_long % (360/27)) / (360/108)) + 1
        
        planets.append(PlanetPosition(
            id=100, # Custom ID for Ketu
            name="Ketu",
            longitude=ketu_long,
            latitude=-rahu.latitude,
            speed=rahu.speed,
            sign=ketu_sign,
            house=0,
            nakshatra=ketu_nak,
            pada=ketu_pada,
            is_retrograde=rahu.is_retrograde
        ))
            
        return planets

    def calculate_houses(self, julian_day: float, lat: float, lon: float, house_system: str = 'W') -> Tuple[List[House], float]:
        # swe.houses returns (cusps, ascmc)
        # cusps is 13 elements (0 is 0.0)
        # ascmc[0] is Ascendant
        
        # Pass sidereal_mode=True to get Sidereal Ascendant/Houses
        cusps, ascmc = self.ephemeris.get_house_cusps(julian_day, lat, lon, house_system, sidereal_mode=True)
        
        ascendant = ascmc[0]
        
        houses = []
        is_zero_indexed = len(cusps) == 12
        
        for i in range(1, 13):
            if is_zero_indexed:
                h_long = cusps[i-1]
            else:
                h_long = cusps[i]
                
            h_sign = int(h_long / 30) + 1
            houses.append(House(number=i, sign=h_sign, longitude=h_long))
            
        return houses, ascendant

    def map_planets_to_houses(self, planets: List[PlanetPosition], houses: List[House], ascendant: float):
        # Whole Sign House System logic:
        # House 1 is the sign of the Ascendant.
        # House 2 is the next sign, etc.
        # Planet's house is determined by its sign relative to Ascendant sign.
        
        asc_sign = int(ascendant / 30) + 1
        
        for p in planets:
            # Calculate house based on sign difference
            # If Planet Sign = 5, Asc Sign = 3
            # House = 5 - 3 + 1 = 3rd House
            
            h = p.sign - asc_sign + 1
            if h <= 0:
                h += 12
            p.house = h
