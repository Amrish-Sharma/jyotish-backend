from datetime import datetime
import swisseph as swe
from typing import Tuple, Dict

class PanchangCalculator:
    
    TITHIS = [
        "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashti", "Saptami", "Ashtami",
        "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima", "Amavasya"
    ]
    
    YOGAS = [
        "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
        "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
        "Variyan", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"
    ]
    
    KARANS = [
        "Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti", # Chara (Movable)
        "Shakuni", "Chatushpada", "Naga", "Kimstughna" # Sthira (Fixed)
    ]
    
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    @staticmethod
    def calculate_panchang(julian_day: float, sun_lon: float, moon_lon: float, date: datetime) -> Dict[str, str]:
        """
        Calculate Panchang elements: Day, Tithi, Yoga, Karan.
        """
        
        # 1. Day of Week
        day_idx = date.weekday() # 0=Monday
        day_name = PanchangCalculator.DAYS[day_idx]
        
        # 2. Tithi
        # Difference between Moon and Sun longitude
        diff = moon_lon - sun_lon
        if diff < 0:
            diff += 360
            
        tithi_val = diff / 12.0
        tithi_idx = int(tithi_val) 
        # tithi_idx goes from 0 to 29.
        # 0-14: Shukla Paksha (Waxing), 15-29: Krishna Paksha (Waning)
        
        is_shukla = tithi_idx < 15
        paksha = "Shukla" if is_shukla else "Krishna"
        
        display_idx = tithi_idx % 15
        tithi_name_base = PanchangCalculator.TITHIS[display_idx]
        
        # Special case for 15th (Purnima) and 30th (Amavasya)
        if tithi_idx == 14:
            tithi_name = "Purnima"
        elif tithi_idx == 29:
            tithi_name = "Amavasya"
        else:
            tithi_name = f"{paksha} {tithi_name_base}"
            
        # 3. Yoga
        # Sum of Sun and Moon longitude
        total = sun_lon + moon_lon
        if total > 360:
            total -= 360
        
        yoga_val = total / (360.0 / 27.0)
        yoga_idx = int(yoga_val)
        yoga_name = PanchangCalculator.YOGAS[yoga_idx % 27]
        
        # 4. Karan
        # Half of Tithi
        karan_val = diff / 6.0
        karan_idx = int(karan_val)
        
        # Logic for Karan mapping is complex (repeating vs fixed)
        # 0-56 Karans in a lunar month (60 half-tithis? No 30 tithis * 2 = 60 karans)
        
        # First 7 are movable and repeat 8 times = 56
        # Last 4 are fixed (appear once)
        
        # Total 60 Karans
        # Karan 1: Kimstughna (Fixed) - 1st half of Shukla Pratipada
        # Karan 2-57: Bava...Vishti (Repeating)
        # Karan 58: Shakuni (Fixed)
        # Karan 59: Chatushpada (Fixed)
        # Karan 60: Naga (Fixed)
        
        # It's easier to map based on 'karan_idx' (0 to 59)
        
        if karan_idx == 0:
            karan_name = "Kimstughna"
        elif 1 <= karan_idx <= 56:
            # (karan_idx - 1) % 7
            karan_name = PanchangCalculator.KARANS[(karan_idx - 1) % 7]
        elif karan_idx == 57:
            karan_name = "Shakuni"
        elif karan_idx == 58:
            karan_name = "Chatushpada"
        else:
            karan_name = "Naga"

        return {
            "day": day_name,
            "tithi": tithi_name,
            "yoga": yoga_name,
            "karan": karan_name
        }
