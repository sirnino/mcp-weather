import os
import json
from pyowm.owm import OWM



def current_weather(city: str) -> str:
    """
    Get the current weather condition in a city
    Args:
        city (str): The city to provide the weather of
    Returns:
        str: A JSON string containing the current weather conditions
    """
    # Ref: https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#weather_data
    owm = OWM(os.getenv('OPENWEATHERMAP_APIKEY'))
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)  # the observation object is a box containing a weather object
    temperature = observation.weather.temperature('celsius')
    result = {
        'temperature': {
                'temp': temperature['temp'],
                'feels_like': temperature['feels_like']
        },
        'humidity': observation.weather.humidity,
        'weather': observation.weather.status
    }

    return json.dumps(result)