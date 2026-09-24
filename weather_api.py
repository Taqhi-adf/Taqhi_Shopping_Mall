import httpx
from config import (
    WEATHER_API_URL, WEATHER_LATITUDE, WEATHER_LONGITUDE,
    WEATHER_TIMEZONE, WEATHER_LOCATION_NAME
)

def get_current_weather() -> dict:
    params = {
        "latitude": WEATHER_LATITUDE,
        "longitude": WEATHER_LONGITUDE,
        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "surface_pressure",
            "wind_speed_10m",
            "precipitation",
            "weather_code",
        ]),
        "timezone": WEATHER_TIMEZONE,
    }

    with httpx.Client(timeout=15) as client:
        response = client.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

    current = data.get("current", {})
    return {
        "location": WEATHER_LOCATION_NAME,
        "latitude": WEATHER_LATITUDE,
        "longitude": WEATHER_LONGITUDE,
        "observation_time": current.get("time"),
        "temperature_c": current.get("temperature_2m"),
        "relative_humidity": current.get("relative_humidity_2m"),
        "surface_pressure_hpa": current.get("surface_pressure"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
        "precipitation_mm": current.get("precipitation"),
        "weather_code": current.get("weather_code"),
        "provider": "Open-Meteo",
    }
