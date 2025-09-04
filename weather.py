import os
import requests
from dotenv import load_dotenv

# load variables from .env for local runs
load_dotenv()

def get_weather():
    # Vail, Colorado latitude + longitude
    lat, lon = 39.6403, -106.3742

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        # Friendly message if key is missing
        raise RuntimeError(
            "Missing OPENWEATHER_API_KEY. "
            "Create a .env file with OPENWEATHER_API_KEY=your_key"
        )

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "units": "imperial",
        "appid": api_key
    }

    try:
        # add a timeout so the app doesn't hang forever
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        # short, safe message (don’t expose secrets)
        raise RuntimeError("Weather request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Weather request failed: {e}")

    # Pick out simple info (guard against missing fields)
    main = data.get("main", {})
    weather_list = data.get("weather", [{}])
    description = weather_list[0].get("description", "Unknown").title()

    temp = main.get("temp")
    temp = round(temp) if isinstance(temp, (int, float)) else "N/A"

    return {
        "temp": temp,
        "description": description,
    }
