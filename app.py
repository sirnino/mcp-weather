import os
import json
from pyowm.owm import OWM
import gradio as gr

import requests
from bs4 import BeautifulSoup, Comment

def scrape_body(url: str, return_html: bool = False) -> str:
    """
    Fetches the given URL and extracts its <body> content, cleaned of scripts,
    styles, navigation, header/footer, comments, and other non-essential tags.

    Args:
        url (str): The URL to scrape.
        return_html (bool): If True, returns the cleaned HTML of the <body>;
                            otherwise, returns plain text.

    Returns:
        str: Cleaned HTML or text content of the <body>.
    """
    # Fetch the page
    response = requests.get(url)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove unwanted tags
    for tag_name in ['script', 'style', 'header', 'footer', 'nav', 'aside', 'form', 'noscript', 'details']:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Remove HTML comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Extract body
    body = soup.body
    if body is None:
        return ''

    if return_html:
        # Return cleaned HTML of the body
        # Strip attributes from tags to keep only content structure
        for tag in body.find_all(True):
            tag.attrs = {}
        return str(body)
    else:
        # Get plain text, preserving line breaks
        text = body.get_text(separator='\n', strip=True)
        # Optionally, collapse multiple blank lines
        lines = [line for line in text.splitlines() if line.strip()]
        return '\n'.join(lines)

# Ref: https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#weather_data
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

with gr.Blocks() as demo:
    gr.Markdown(
        """
        ## This tool is MCP-only, so it does not have a UI.
        """
    )
    gr.api(
        current_weather, 
        scrape_body
    )

_, url, _ = demo.launch(mcp_server=True)