
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(override=True)

# OpenWeatherMap API configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Default temperature unit
DEFAULT_UNIT = "metric"
