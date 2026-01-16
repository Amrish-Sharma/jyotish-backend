from datetime import datetime, timezone
import swisseph as swe
from typing import Tuple

class TimeAstronomy:
    """
    Handles time conversions and astronomical calculations.
    """

    @staticmethod
    def to_julian_day(dt: datetime) -> float:
        """
        Convert datetime to Julian Day (UT).
        Assumes dt is timezone-aware or UTC.
        """
        if dt.tzinfo is None:
            # Assume UTC if naive, but ideally should be aware
            dt = dt.replace(tzinfo=timezone.utc)
        
        # Convert to UTC
        dt_utc = dt.astimezone(timezone.utc)
        
        # swe.julday takes year, month, day, hour (decimal)
        hour_decimal = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0 + dt_utc.microsecond / 3600000000.0
        
        return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_decimal)

    @staticmethod
    def get_sidereal_time(julian_day: float, longitude: float, obliquity: float = 23.44) -> float:
        """
        Calculate Local Sidereal Time (LST).
        
        Args:
            julian_day: Julian Day (UT)
            longitude: Observer's longitude (degrees, East is positive)
            obliquity: Obliquity of ecliptic (approx 23.44, swe calculates it internally usually)
            
        Returns:
            LST in degrees (0-360) or hours? swe.sidtime returns hours.
        """
        # swe.sidtime(jd_ut) returns Greenwich Sidereal Time (GST) in hours
        gst_hours = swe.sidtime(julian_day)
        
        # Convert GST to LST
        # LST = GST + Longitude / 15
        lst_hours = gst_hours + longitude / 15.0
        
        # Normalize to 0-24
        lst_hours = lst_hours % 24
        
        return lst_hours

    @staticmethod
    def get_ayanamsa(julian_day: float, ayanamsa_id: int = swe.SIDM_LAHIRI) -> float:
        """
        Get Ayanamsa value for a given date.
        """
        swe.set_sid_mode(ayanamsa_id)
        return swe.get_ayanamsa_ut(julian_day)
