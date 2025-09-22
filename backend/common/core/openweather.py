import httpx
from datetime import datetime
from common.config import settings

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

async def get_weather(city: str = None, units: str = "metric", lang: str = "en", lat: float = None, lon: float = None) -> dict:
    """
    Fetch current weather data for a city from OpenWeatherMap.
    """

    params = {
        "appid": settings.openweather_api_key,
        "units": units,  # "metric" (°C), "imperial" (°F)
        "lang": lang     # response language
    }

    if city:
        params["q"] = city
    else:
        params["lat"] = lat
        params["lon"] = lon
    

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()  # raises error if not 200
            data = response.json()
            # print(generate_weather_paragraph(data))
            return data
    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except httpx.RequestError as req_err:
        print(f"Request error occurred: {req_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None


def generate_weather_paragraph(weather_data):
    # Extracting data
    city = weather_data['name'] or "Your location"
    country = weather_data['sys']['country']
    temperature = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    temp_min = weather_data['main']['temp_min']
    temp_max = weather_data['main']['temp_max']
    weather_description = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    cloudiness = weather_data['clouds']['all']
    sunrise_timestamp = weather_data['sys']['sunrise']
    sunset_timestamp = weather_data['sys']['sunset']

    # Convert Unix timestamps to human-readable time
    sunrise = datetime.utcfromtimestamp(sunrise_timestamp).strftime('%H:%M:%S')
    sunset = datetime.utcfromtimestamp(sunset_timestamp).strftime('%H:%M:%S')

    # Create paragraph
    weather_paragraph = (
        f"In {city}, {country}, the current temperature is {temperature}°C, "
        f"with a 'feels like' temperature of {feels_like}°C. The temperature ranges "
        f"between {temp_min}°C and {temp_max}°C today. The weather is described as "
        f"'{weather_description}' with a cloud cover of {cloudiness}% and a humidity level "
        f"of {humidity}%. Winds are blowing at {wind_speed} m/s. The sun rose at {sunrise} "
        f"and will set at {sunset}."
    )

    return weather_paragraph
