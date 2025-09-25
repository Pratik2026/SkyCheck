"""
Weather-related tools for the CrewAI weather chatbot.
Contains tools for fetching weather data and language detection.
"""

from crewai.tools import tool
import requests
import os
import re
from datetime import datetime
from typing import Dict, Any


@tool("Weather Information Tool")
def get_weather_info(location: str) -> str:
    """
    Fetch current weather and forecast information for a given location.

    Args:
        location (str): The city or region name (in Japanese or English).

    Returns:
        str: A formatted string containing current weather and up to 3-day forecast.
        Returns an error message string if API fails or data is unavailable.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return "⚠ Weather API key not configured. Please set OPENWEATHERMAP_API_KEY in .env file."

    try:
        # Try to fetch weather data directly with the provided location
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        current_response = requests.get(current_url, timeout=10)

        if current_response.status_code != 200:
            return f"⚠ Weather information for '{location}' could not be found. Please check the city name."

        current_data = current_response.json()

        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
        forecast_response = requests.get(forecast_url, timeout=10)
        forecast_data = forecast_response.json() if forecast_response.status_code == 200 else {}

        from ..utils.weather_formatters import format_weather_info
        return format_weather_info(current_data, forecast_data)

    except requests.exceptions.Timeout:
        return "⚠ Weather service response is too slow. Please try again later."
    except requests.exceptions.RequestException as e:
        return f"⚠ Network error: {str(e)}"
    except Exception as e:
        return f"⚠ Error occurred while processing weather data: {str(e)}"


@tool("Language Detector")
def detect_language(text: str) -> str:
    """
    Detect the language of user input.

    Args:
        text (str): Input sentence in Japanese or English.

    Returns:
        str: 'japanese' or 'english'
    """
    # Detect if text contains Japanese characters
    has_japanese = bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text))
    return 'japanese' if has_japanese else 'english'