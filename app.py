import os
import json
from pyowm.owm import OWM
import gradio as gr

owm = OWM(os.getenv('OPENWEATHERMAP_APIKEY'))

def current_weather(city: str) -> str:
    """
    Get the current weather condition in a city
    Args:
        city (str): The city to provide the weather of
    Returns:
        str: A JSON string containing the current weather conditions
    """

    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)  # the observation object is a box containing a weather object
    
    result = {
        'weather': observation.weather.status,
        'temperature': observation.weather.temperature.temp,
        'humidity': observation.weather.humidity
    }

    return json.dumps(result)

# Create the Gradio interface
demo = gr.Interface(
    fn=current_weather,
    inputs=gr.Textbox(placeholder="Enter a city to check the weather..."),
    outputs=gr.JSON(),
    title="Current Weather in a city",
    description="Get the current weather condition in a city using OpenWeatherMap"
)

# Launch the interface and MCP server
if __name__ == "__main__":
    demo.launch(mcp_server=True)