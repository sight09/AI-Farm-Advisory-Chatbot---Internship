# tests/test_openweather.py
import unittest
from common.core.openweather import get_weather, generate_weather_paragraph


class TestOpenWeather(unittest.IsolatedAsyncioTestCase):

    async def test_get_weather(self):
        city = "Addis Ababa"
        weather = await get_weather(city)
        self.assertIn("weather", weather)
        self.assertIn("base", weather)
        self.assertIn("cod", weather)
        
        # with longitude and latitude
        lat = 51.5074
        lon = -0.1278
        weather = await get_weather(lat=lat, lon=lon)
        self.assertIn("weather", weather)
        self.assertIn("base", weather)
        self.assertIn("cod", weather)

    async def test_generate_weather_paragraph(self):
        city = "Addis Ababa"
        weather = await get_weather(city)
        forecast = generate_weather_paragraph(weather)
        
        self.assertIsInstance(forecast, str)
        # Check if certain keywords are in the generated paragraph
        self.assertIn("Addis Ababa", forecast)
        self.assertIn("temperature", forecast)
        self.assertIn("humidity", forecast)
