import httpx
from common.config import settings

BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

async def get_weather(city: str, units: str = "metric", lang: str = "en") -> dict:
    """
    Fetch current weather data for a city from OpenWeatherMap.
    """
    params = {
        "q": city,
        "appid": settings.openweather_api_key,
        "units": units,  # "metric" (°C), "imperial" (°F)
        "lang": lang     # response language
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()  # raises error if not 200
        return response.json()
