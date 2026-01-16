import abc
import os
import swisseph as swe
from typing import Tuple, Optional

class EphemerisProvider(abc.ABC):
    """
    Abstract base class for Ephemeris providers.
    """

    @abc.abstractmethod
    def get_planet_position(self, planet_id: int, julian_day: float) -> Tuple[float, float, float, float]:
        """
        Get planet position (longitude, latitude, distance, speed).
        
        Args:
            planet_id: Swiss Ephemeris planet ID (e.g., swe.SUN)
            julian_day: Julian Day number (ET)

        Returns:
            Tuple of (longitude, latitude, distance, speed)
        """
        pass

    @abc.abstractmethod
    def get_house_cusps(self, julian_day: float, lat: float, lon: float, house_system: str = 'W') -> Tuple[list, list]:
        """
        Get house cusps and ascendant.

        Args:
            julian_day: Julian Day number (UT)
            lat: Latitude
            lon: Longitude
            house_system: House system code (default 'W' for Whole Sign - mapped later, usually 'P' or 'W' in swe)
                          Note: swe.houses usually takes 'P' (Placidus), 'W' (Equal), etc.
                          For Whole Sign, we typically calculate Ascendant and derive houses manually,
                          but 'W' in swe is Equal House.
        
        Returns:
            Tuple of (cusps, ascmc)
        """
        pass

    @abc.abstractmethod
    def set_sidereal_mode(self, ayanamsa_id: int):
        """
        Set the Ayanamsa mode.
        """
        pass

class SwissEphemerisProvider(EphemerisProvider):
    """
    Implementation of EphemerisProvider using pyswisseph.
    """

    def __init__(self, ephe_path: Optional[str] = None):
        if ephe_path:
            swe.set_ephe_path(ephe_path)
        else:
            # Default to looking in a local 'ephe' directory relative to this file or project root
            # For now, let's assume it's set via environment or default
            pass

    def get_planet_position(self, planet_id: int, julian_day: float) -> Tuple[float, float, float, float]:
        # flags: swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL
        # We assume sidereal mode is set globally or we pass the flag.
        # Ideally, we set sidereal mode once.
        
        flags = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL
        
        # swe.calc_ut returns ((long, lat, dist, speed_long, speed_lat, speed_dist), rflag)
        # But wait, julian_day for planet positions in sidereal usually requires ET if high precision, 
        # but swe.calc_ut takes UT. swe.calc takes ET.
        # Let's use swe.calc (ET) for consistency if we have ET, but usually we start with UT.
        # For simplicity in this phase, we'll assume the input JD is correct for the function used.
        # Let's use swe.calc_ut and assume input is UT.
        
        res, rflag = swe.calc_ut(julian_day, planet_id, flags)
        return res[0], res[1], res[2], res[3] # long, lat, dist, speed_long

    def get_house_cusps(self, julian_day: float, lat: float, lon: float, house_system: str = 'W') -> Tuple[list, list]:
        # swe.houses returns (cusps, ascmc)
        # cusps is a tuple of 13 floats (index 0 is 0.0)
        # ascmc is a tuple of 10 floats
        return swe.houses(julian_day, lat, lon, bytes(house_system, 'ascii'))

    def set_sidereal_mode(self, ayanamsa_id: int):
        swe.set_sid_mode(ayanamsa_id)

    def get_ayanamsa(self, julian_day: float) -> float:
        return swe.get_ayanamsa_ut(julian_day)
