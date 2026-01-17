from typing import Dict, Optional, Tuple

class VedicAttributes:
    # Lookup tables for Nakshatra based attributes
    
    # 27 Nakshatras
    NAKSHATRAS = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
        "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    
    # Gana: 0=Deva, 1=Manushya, 2=Rakshasa
    GANA_MAP = {
       "Ashwini": "Deva", "Bharani": "Manushya", "Krittika": "Rakshasa",
       "Rohini": "Manushya", "Mrigashira": "Deva", "Ardra": "Manushya",
       "Punarvasu": "Deva", "Pushya": "Deva", "Ashlesha": "Rakshasa",
       "Magha": "Rakshasa", "Purva Phalguni": "Manushya", "Uttara Phalguni": "Manushya",
       "Hasta": "Deva", "Chitra": "Rakshasa", "Swati": "Deva",
       "Vishakha": "Rakshasa", "Anuradha": "Deva", "Jyeshtha": "Rakshasa",
       "Mula": "Rakshasa", "Purva Ashadha": "Manushya", "Uttara Ashadha": "Manushya",
       "Shravana": "Deva", "Dhanishtha": "Rakshasa", "Shatabhisha": "Rakshasa",
       "Purva Bhadrapada": "Manushya", "Uttara Bhadrapada": "Manushya", "Revati": "Deva"
    }

    # Yoni (Animal Symbol)
    YONI_MAP = {
        "Ashwini": "Horse", "Bharani": "Elephant", "Krittika": "Sheep",
        "Rohini": "Snake", "Mrigashira": "Serpent", "Ardra": "Dog",
        "Punarvasu": "Cat", "Pushya": "Goat", "Ashlesha": "Cat",
        "Magha": "Rat", "Purva Phalguni": "Rat", "Uttara Phalguni": "Cow",
        "Hasta": "Buffalo", "Chitra": "Tiger", "Swati": "Buffalo",
        "Vishakha": "Tiger", "Anuradha": "Deer", "Jyeshtha": "Deer",
        "Mula": "Dog", "Purva Ashadha": "Monkey", "Uttara Ashadha": "Mongoose",
        "Shravana": "Monkey", "Dhanishtha": "Lion", "Shatabhisha": "Horse",
        "Purva Bhadrapada": "Lion", "Uttara Bhadrapada": "Cow", "Revati": "Elephant"
    }
    
    # Nadi (Pseudo-medical classification): Aadi (Vata), Madhya (Pitta), Antya (Kapha)
    NADI_MAP = {
        "Ashwini": "Aadi", "Bharani": "Madhya", "Krittika": "Antya",
        "Rohini": "Antya", "Mrigashira": "Madhya", "Ardra": "Aadi",
        "Punarvasu": "Aadi", "Pushya": "Madhya", "Ashlesha": "Antya",
        "Magha": "Antya", "Purva Phalguni": "Madhya", "Uttara Phalguni": "Aadi",
        "Hasta": "Aadi", "Chitra": "Madhya", "Swati": "Antya",
        "Vishakha": "Antya", "Anuradha": "Madhya", "Jyeshtha": "Aadi",
        "Mula": "Aadi", "Purva Ashadha": "Madhya", "Uttara Ashadha": "Antya",
        "Shravana": "Antya", "Dhanishtha": "Madhya", "Shatabhisha": "Aadi",
        "Purva Bhadrapada": "Aadi", "Uttara Bhadrapada": "Madhya", "Revati": "Antya"
    }

    # Varan (Caste/Class based on Rasi/Sign)
    # 1,4,8 ('Brahmin'), 2,5,9 ('Kshatriya'), 3,6,10 ('Vaishya'), 7,11,12 ('Shudra') - Simplified mapping
    VARAN_MAP_BY_SIGN = {
        1: "Kshatriya", 2: "Vaishya", 3: "Shudra", 4: "Brahmin",
        5: "Kshatriya", 6: "Vaishya", 7: "Shudra", 8: "Brahmin",
        9: "Kshatriya", 10: "Vaishya", 11: "Shudra", 12: "Brahmin"
    }

    # Vashya (Control nature)
    VASHYA_MAP_BY_SIGN = {
        1: "Chatushpada", 2: "Chatushpada", 3: "Manava", 4: "Jalachara",
        5: "Vanachara", 6: "Manava", 7: "Manava", 8: "Keeta",
        9: "Chatushpada", 10: "Jalachara", 11: "Manava", 12: "Jalachara"
    }
    
    # Ghatak Chakra (Inauspicious factors based on Moon Sign)
    # Format: Sign Index (1-12) -> { month, tithi, day, nakshatra, ... }
    GHATAK_MAP = {
        1: {"month": "Kartik", "tithi": "1, 6, 11", "day": "Sunday", "nakshatra": "Magha"},  # Aries
        2: {"month": "Margashirsha", "tithi": "5, 10, 15", "day": "Saturday", "nakshatra": "Rohini"}, # Taurus
        3: {"month": "Pausha", "tithi": "2, 7, 12", "day": "Monday", "nakshatra": "Ardra"}, # Gemini
        4: {"month": "Magha", "tithi": "2, 7, 12", "day": "Wednesday", "nakshatra": "Pushya"}, # Cancer
        5: {"month": "Phalguna", "tithi": "3, 8, 13", "day": "Saturday", "nakshatra": "Hasta"}, # Leo
        6: {"month": "Chaitra", "tithi": "5, 10, 15", "day": "Saturday", "nakshatra": "Chitra"}, # Virgo
        7: {"month": "Vaishakha", "tithi": "4, 9, 14", "day": "Thursday", "nakshatra": "Vishakha"}, # Libra
        8: {"month": "Jyeshtha", "tithi": "1, 6, 11", "day": "Friday", "nakshatra": "Anuradha"}, # Scorpio
        9: {"month": "Ashadha", "tithi": "3, 8, 13", "day": "Sunday", "nakshatra": "Mula"}, # Sagittarius
        10: {"month": "Shravana", "tithi": "4, 9, 14", "day": "Tuesday", "nakshatra": "Shravana"}, # Capricorn
        11: {"month": "Bhadrapada", "tithi": "4, 9, 14", "day": "Thursday", "nakshatra": "Shatabhisha"}, # Aquarius
        12: {"month": "Ashvina", "tithi": "3, 8, 13", "day": "Friday", "nakshatra": "Revati"} # Pisces
    }

    @staticmethod
    def get_avakahada(nakshatra_idx: int, sign_idx: int) -> Dict[str, str]:
        """
        Get Avakahada Chakra details based on Nakshatra (0-26) and Sign (1-12).
        """
        nakshatra_name = VedicAttributes.NAKSHATRAS[nakshatra_idx]
        
        return {
            "gana": VedicAttributes.GANA_MAP.get(nakshatra_name, "Unknown"),
            "yoni": VedicAttributes.YONI_MAP.get(nakshatra_name, "Unknown"),
            "nadi": VedicAttributes.NADI_MAP.get(nakshatra_name, "Unknown"),
            "varan": VedicAttributes.VARAN_MAP_BY_SIGN.get(sign_idx, "Unknown"),
            "vashya": VedicAttributes.VASHYA_MAP_BY_SIGN.get(sign_idx, "Unknown"),
            "varga": "Unknown", # Needs more complex calc
            "yunja": "Unknown", # Needs more complex calc
            "hansak": "Unknown", # Needs more complex calc
            "paya": "Unknown"   # Needs more complex calc
        }

    @staticmethod
    def get_ghatak(sign_idx: int) -> Dict[str, str]:
        """
        Get Ghatak Details based on Moon Sign (1-12).
        """
        return VedicAttributes.GHATAK_MAP.get(sign_idx, {})
