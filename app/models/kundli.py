from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PlanetPosition(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float
    speed: float
    sign: int
    house: int
    nakshatra: int
    pada: int
    is_retrograde: bool

class House(BaseModel):
    number: int
    sign: int
    longitude: float # Cusp longitude

class KundliRequest(BaseModel):
    dob: str # YYYY-MM-DD
    tob: str # HH:MM:SS
    lat: float
    lon: float
    timezone: float # Offset in hours (e.g., 5.5 for IST)
    ayanamsa: int = 1 # 1 = Lahiri (swe.SIDM_LAHIRI)

from app.models.dasha import DashaTimeline

class BasicDetails(BaseModel):
    ascendant_lord: str
    rasi_lord: str
    nakshatra_charan: str
    nakshatra_lord: str
    yoga: str
    karan: str
    tithi: str
    day: str
    gana: str
    yoni: str
    nadi: str
    varan: str
    vashya: str
    varga: str
    yunja: str
    hansak: str
    paya: str
    sunsign_west: str

class GhatakDetails(BaseModel):
    month: str
    tithi: str
    day: str
    nakshatra: str
    yoga: str
    karan: str
    prahar: str
    varga: str
    lagna: str
    sun: str
    moon: str
    mars: str
    mer: str
    jup: str
    ven: str
    sat: str
    rah: str

class KundliResponse(BaseModel):
    lagna: float
    lagna_sign: int
    planets: List[PlanetPosition]
    houses: List[House]
    ayanamsa_value: float
    julian_day: float
    dasha: DashaTimeline
    basic_details: Optional[BasicDetails] = None
    ghatak_details: Optional[GhatakDetails] = None
