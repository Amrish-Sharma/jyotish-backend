import asyncio
from app.engine.core.ephemeris import SwissEphemerisProvider
from app.engine.core.calculators import KundliCalculator
import swisseph as swe
from app.engine.core.time_astronomy import TimeAstronomy
from datetime import datetime, timedelta

async def main():
    dt = datetime.strptime("1989-02-24 16:50:00", "%Y-%m-%d %H:%M:%S")
    dt_utc = dt - timedelta(hours=5.5)
    jd = TimeAstronomy.to_julian_day(dt_utc)
    lat = 28.5355
    lon = 77.3910
    
    print(f"JD: {jd}")
    
    # 3. Try swe.houses_ex with SIDEREAL flag if available
    try:
        flags = swe.FLG_SIDEREAL
        cusps_ex, ascmc_ex = swe.houses_ex(jd, lat, lon, b'W', flags)
        asc_sidereal_ex = ascmc_ex[0]
        print(f"Sidereal Ascendant (swe.houses_ex): {asc_sidereal_ex}")
        print(f"Sidereal Asc Sign (ex): {int(asc_sidereal_ex/30)+1}")
    except AttributeError:
        print("swe.houses_ex not found")
    except Exception as e:
        print(f"swe.houses_ex failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
