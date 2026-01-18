import pytest
from datetime import datetime, timedelta
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

def test_sidereal_ascendant(calculator):
    # Date: 1989-02-24 16:30:00 Local Time (IST +5.5)
    # UTC: 11:00:00
    # Location: Noida/Delhi (28.5355, 77.3910)
    
    dt = datetime(1989, 2, 24, 16, 30, 0)
    dt_utc = dt - timedelta(hours=5.5)
    jd = TimeAstronomy.to_julian_day(dt_utc)
    
    lat = 28.5355
    lon = 77.3910
    
    # Check Ayanamsa (sanity check)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    houses, ascendant = calculator.calculate_houses(jd, lat, lon)
    
    # Expected: Cancer Ascendant (Sign 4)
    # Cancer is 90-120 degrees
    # Ascendant should be approx 114 degrees
    
    asc_sign = int(ascendant / 30) + 1
    
    assert asc_sign == 4, f"Expected Ascendant Sign 4 (Cancer), got {asc_sign}. Ascendant Longitude: {ascendant}"
    assert 90 <= ascendant < 120, f"Ascendant {ascendant} not in Cancer range"
