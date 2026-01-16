from datetime import datetime, timedelta
from typing import List, Tuple
from app.models.dasha import DashaPeriod, DashaTimeline
from app.models.kundli import PlanetPosition

class VimshottariDasha:
    # Planet sequence and duration in years
    PLANET_SEQUENCE = [
        ("Ketu", 7),
        ("Venus", 20),
        ("Sun", 6),
        ("Moon", 10),
        ("Mars", 7),
        ("Rahu", 18),
        ("Jupiter", 16),
        ("Saturn", 19),
        ("Mercury", 17)
    ]
    
    TOTAL_CYCLE = 120 # years

    @staticmethod
    def calculate(moon_longitude: float, birth_date: datetime) -> DashaTimeline:
        """
        Calculate Vimshottari Dasha timeline.
        
        Args:
            moon_longitude: Moon's longitude (0-360)
            birth_date: Date of birth
            
        Returns:
            DashaTimeline containing Mahadashas
        """
        # 1. Determine Nakshatra of Moon
        # 360 / 27 = 13.3333 degrees per nakshatra
        nakshatra_span = 360 / 27
        nakshatra_val = moon_longitude / nakshatra_span
        nakshatra_idx = int(nakshatra_val) # 0-26
        
        # Fraction traversed in current nakshatra
        fraction_traversed = nakshatra_val - nakshatra_idx
        fraction_remaining = 1.0 - fraction_traversed
        
        # 2. Determine Lord of Nakshatra (Starting Mahadasha Lord)
        # Sequence of lords repeats: Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury
        # Nakshatra 0 (Ashwini) -> Ketu
        # Nakshatra 1 (Bharani) -> Venus
        # ...
        lord_idx = nakshatra_idx % 9
        start_planet, duration = VimshottariDasha.PLANET_SEQUENCE[lord_idx]
        
        # 3. Calculate Balance of Dasha
        balance_years = duration * fraction_remaining
        
        # 4. Generate Timeline
        mahadashas = []
        current_date = birth_date
        
        # First Mahadasha (partial)
        end_date = VimshottariDasha.add_years(current_date, balance_years)
        md = DashaPeriod(
            planet=start_planet,
            start_date=current_date,
            end_date=end_date,
            duration_years=balance_years,
            level=1
        )
        md.sub_periods = VimshottariDasha._generate_sub_periods(md, start_planet)
        mahadashas.append(md)
        current_date = end_date
        
        # Subsequent Mahadashas
        for i in range(1, 10): # Generate next 9 dashas
            idx = (lord_idx + i) % 9
            planet, duration = VimshottariDasha.PLANET_SEQUENCE[idx]
            end_date = VimshottariDasha.add_years(current_date, duration)
            
            md = DashaPeriod(
                planet=planet,
                start_date=current_date,
                end_date=end_date,
                duration_years=duration,
                level=1
            )
            md.sub_periods = VimshottariDasha._generate_sub_periods(md, planet)
            mahadashas.append(md)
            current_date = end_date
            
        return DashaTimeline(mahadashas=mahadashas)

    @staticmethod
    def _generate_sub_periods(parent: DashaPeriod, lord_planet: str) -> List[DashaPeriod]:
        """
        Generate Antardashas for a Mahadasha.
        Antardasha sequence starts from the Mahadasha lord itself and follows the standard sequence.
        Duration = (Mahadasha Years * Antardasha Years) / 120
        """
        sub_periods = []
        current_date = parent.start_date
        
        # Find index of the lord planet in the sequence
        start_idx = next(i for i, (p, d) in enumerate(VimshottariDasha.PLANET_SEQUENCE) if p == lord_planet)
        
        for i in range(9):
            idx = (start_idx + i) % 9
            planet, duration_years = VimshottariDasha.PLANET_SEQUENCE[idx]
            
            # Calculate sub-period duration
            # Formula: (Mahadasha Years * Antardasha Lord Years) / 120
            # But wait, parent.duration_years might be partial (balance).
            # The standard formula uses the FULL duration of the Mahadasha.
            # We need to know the full duration of the Mahadasha lord.
            
            # Find full duration of parent lord
            parent_full_duration = next(d for p, d in VimshottariDasha.PLANET_SEQUENCE if p == lord_planet)
            
            sub_duration_years = (parent_full_duration * duration_years) / 120.0
            
            # If this is the first Mahadasha (balance), we might need to adjust sub-periods?
            # Actually, for the first Mahadasha (balance), the sub-periods are also partial.
            # Usually, we calculate the full set of Antardashas and then clip them to the start date.
            # Or we find which Antardasha is running at birth.
            
            # Let's refine the logic for the first Mahadasha (Balance).
            # If parent is partial (balance), we need to find where we are in the sub-period cycle.
            
            # This is complex. Let's simplify:
            # 1. Generate FULL Antardashas for the Mahadasha as if it started from 0.
            # 2. Calculate the end date of the Mahadasha.
            # 3. Filter out sub-periods that ended before birth_date.
            # 4. Clip the sub-period that overlaps with birth_date.
            
            pass 
            
        # Re-implementing with better logic below
        return VimshottariDasha._calculate_antardashas(parent, lord_planet)

    @staticmethod
    def _calculate_antardashas(parent: DashaPeriod, lord_planet: str) -> List[DashaPeriod]:
        sub_periods = []
        
        # Full duration of the Mahadasha lord
        parent_full_duration = next(d for p, d in VimshottariDasha.PLANET_SEQUENCE if p == lord_planet)
        
        # Start index for Antardasha sequence
        start_idx = next(i for i, (p, d) in enumerate(VimshottariDasha.PLANET_SEQUENCE) if p == lord_planet)
        
        # Calculate all 9 Antardashas relative to a theoretical start
        # If parent is full, theoretical start = parent.start_date
        # If parent is partial, we need to back-calculate the theoretical start.
        
        # Theoretical start of this Mahadasha
        # If parent is partial, parent.duration_years < parent_full_duration
        # theoretical_start = parent.end_date - parent_full_duration (years)
        
        theoretical_start = VimshottariDasha.add_years(parent.end_date, -parent_full_duration)
        
        current_cursor = theoretical_start
        
        for i in range(9):
            idx = (start_idx + i) % 9
            planet, duration_years = VimshottariDasha.PLANET_SEQUENCE[idx]
            
            sub_duration = (parent_full_duration * duration_years) / 120.0
            end_cursor = VimshottariDasha.add_years(current_cursor, sub_duration)
            
            # Check overlap with actual parent window [parent.start_date, parent.end_date]
            # We only include if end_cursor > parent.start_date
            
            if end_cursor > parent.start_date:
                # This sub-period is valid (either full or partial)
                actual_start = max(current_cursor, parent.start_date)
                actual_end = min(end_cursor, parent.end_date)
                
                # Duration of this specific segment
                # We can't easily subtract dates to get years, so we use the dates.
                
                sub_periods.append(DashaPeriod(
                    planet=planet,
                    start_date=actual_start,
                    end_date=actual_end,
                    duration_years=sub_duration, # Keep nominal duration or actual? Let's keep nominal for reference? No, actual.
                    # Actually, let's just store dates. duration_years is derived.
                    level=2
                ))
            
            current_cursor = end_cursor
            
        return sub_periods

    @staticmethod
    def add_years(d: datetime, years: float) -> datetime:
        """
        Add fractional years to a date.
        """
        # Approximate using days
        days = years * 365.2425
        return d + timedelta(days=days)
