from pydantic import BaseModel
from datetime import datetime
from typing import List

class DashaPeriod(BaseModel):
    planet: str
    start_date: datetime
    end_date: datetime
    duration_years: float
    level: int # 1=Mahadasha, 2=Antardasha, etc.
    sub_periods: List['DashaPeriod'] = []

class DashaTimeline(BaseModel):
    mahadashas: List[DashaPeriod]
