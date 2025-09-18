import asyncio
from common.core.openweather import get_weather


asyncio.run(get_weather("London", units="metric", lang="en"))

