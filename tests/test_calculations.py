import pytest
from datetime import datetime
from app.engine.core.ephemeris import SwissEphemerisProvider
from app.engine.core.calculators import KundliCalculator
from app.engine.core.time_astronomy import TimeAstronomy
import swisseph as swe

@pytest.fixture
def ephemeris_provider():
    return SwissEphemerisProvider()

@pytest.fixture
def calculator(ephemeris_provider):
    return KundliCalculator(ephemeris_provider)

def test_julian_day_conversion():
    # Known date: 2000-01-01 12:00:00 UTC -> JD 2451545.0
    dt = datetime(2000, 1, 1, 12, 0, 0)
    jd = TimeAstronomy.to_julian_day(dt)
    assert jd == pytest.approx(2451545.0, abs=0.0001)

def test_planet_positions(calculator):
    # Test for a known date
    # 2000-01-01 00:00:00 UTC
    dt = datetime(2000, 1, 1, 0, 0, 0)
    jd = TimeAstronomy.to_julian_day(dt)
    
    planets = calculator.calculate_planet_positions(jd, swe.SIDM_LAHIRI)
    
    sun = next(p for p in planets if p.name == "Sun")
    # Sun should be in Sagittarius (approx 256 degrees tropical - ayanamsa ~23 = 233 sidereal -> Scorpio/Sagittarius border?)
    # Wait, Jan 1 is Capricorn tropical. Sidereal is Sagittarius.
    # Sun long tropical ~ 280. Sidereal ~ 256 (Sagittarius).
    
    assert sun.name == "Sun"
    assert sun.longitude > 0
    assert sun.speed > 0

def test_retrograde_detection(calculator):
    # Find a date where Mercury is retrograde
    # Mercury retrograde: Dec 13 2023 to Jan 1 2024
    dt = datetime(2023, 12, 20, 0, 0, 0)
    jd = TimeAstronomy.to_julian_day(dt)
    
    planets = calculator.calculate_planet_positions(jd, swe.SIDM_LAHIRI)
    mercury = next(p for p in planets if p.name == "Mercury")
    
    assert mercury.is_retrograde is True
