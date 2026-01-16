import os
import urllib.request
import sys

# URL for Swiss Ephemeris files (sweph)
# We need sepl_18.se1 (1800-2399) for main planets
# semo_18.se1 for moon
# seas_18.se1 for asteroids (optional)

BASE_URL = "https://github.com/aloistr/swisseph/raw/master/ephe/"
FILES = [
    "sepl_18.se1",
    "semo_18.se1",
]

TARGET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ephe")

def download_file(filename):
    url = BASE_URL + filename
    target_path = os.path.join(TARGET_DIR, filename)
    
    if os.path.exists(target_path):
        print(f"{filename} already exists.")
        return

    print(f"Downloading {filename}...")
    try:
        with urllib.request.urlopen(url) as response, open(target_path, 'wb') as out_file:
            if response.status != 200:
                 print(f"Failed to download {filename}: HTTP {response.status}")
                 return
            out_file.write(response.read())
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

def main():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    
    for f in FILES:
        download_file(f)

    print(f"Ephemeris files located in {TARGET_DIR}")

if __name__ == "__main__":
    main()
