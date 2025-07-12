import os
from dotenv import load_dotenv

load_dotenv()

WEATHERBIT_KEY = os.getenv("WEATHERBIT_KEY")
LAT = float(os.getenv("LAT", 48.7758))
LON = float(os.getenv("LON", 9.1829))
CITY = os.getenv("CITY", "Stuttgart")

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
