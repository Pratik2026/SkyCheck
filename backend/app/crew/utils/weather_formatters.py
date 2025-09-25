"""
Weather data formatting utilities.
Contains functions to format weather API responses into human-readable strings.
"""

from datetime import datetime
from typing import Dict, Any


def format_weather_info(current_data: Dict[Any, Any], forecast_data: Dict[Any, Any]) -> str:
    """
    Format weather API JSON response into a human-readable string.

    Args:
        current_data (dict): JSON object with current weather information.
        forecast_data (dict): JSON object with forecast data.

    Returns:
        str: Formatted string with current weather and up to 3-day forecast.
    """
    try:
        location_name = current_data['name']
        country = current_data['sys']['country']

        temp = round(current_data['main']['temp'])
        feels_like = round(current_data['main']['feels_like'])
        humidity = current_data['main']['humidity']
        pressure = current_data['main']['pressure']
        description = current_data['weather'][0]['description']
        wind_speed = current_data['wind']['speed']
        visibility = current_data.get('visibility', 0) / 1000

        weather_id = current_data['weather'][0]['id']
        emoji = get_weather_emoji(weather_id)

        weather_info = f"""
🌍 Weather for {location_name}, {country}

{emoji} Current Weather: {description.title()}
🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)
💧 Humidity: {humidity}%
🌀 Pressure: {pressure} hPa
💨 Wind Speed: {wind_speed} m/s
👁️ Visibility: {visibility:.1f} km
⏰ Updated: {datetime.now().strftime('%H:%M')}

"""
        if forecast_data and 'list' in forecast_data:
            weather_info += "📅 3-Day Forecast:\n"
            seen_dates = set()
            count = 0

            for item in forecast_data['list']:
                if count >= 3:
                    break
                date_str = item['dt_txt'].split()[0]
                if date_str not in seen_dates:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    day_name = date_obj.strftime('%m/%d (%a)')

                    temp_max = round(item['main']['temp_max'])
                    temp_min = round(item['main']['temp_min'])
                    desc = item['weather'][0]['description']
                    emoji = get_weather_emoji(item['weather'][0]['id'])

                    weather_info += f"{emoji} {day_name}: {temp_max}°C / {temp_min}°C - {desc.title()}\n"

                    seen_dates.add(date_str)
                    count += 1

        return weather_info.strip()

    except Exception as e:
        return f"⚠ Error formatting weather information: {str(e)}"


def format_weather_info_japanese(current_data: Dict[Any, Any], forecast_data: Dict[Any, Any]) -> str:
    """
    Format weather API JSON response into a human-readable Japanese string.

    Args:
        current_data (dict): JSON object with current weather information.
        forecast_data (dict): JSON object with forecast data.

    Returns:
        str: Formatted string with current weather and up to 3-day forecast in Japanese.
    """
    try:
        location_name = current_data['name']
        country = current_data['sys']['country']

        temp = round(current_data['main']['temp'])
        feels_like = round(current_data['main']['feels_like'])
        humidity = current_data['main']['humidity']
        pressure = current_data['main']['pressure']
        description = current_data['weather'][0]['description']
        wind_speed = current_data['wind']['speed']
        visibility = current_data.get('visibility', 0) / 1000

        weather_id = current_data['weather'][0]['id']
        emoji = get_weather_emoji(weather_id)

        weather_info = f"""
🌍 {location_name}, {country} の天気情報

{emoji} 現在の天気: {description}
🌡️ 気温: {temp}°C (体感 {feels_like}°C)
💧 湿度: {humidity}%
🌀 気圧: {pressure} hPa
💨 風速: {wind_speed} m/s
👁️ 視界: {visibility:.1f} km
⏰ 更新: {datetime.now().strftime('%H:%M')}

"""
        if forecast_data and 'list' in forecast_data:
            weather_info += "📅 3日間の予報:\n"
            seen_dates = set()
            count = 0

            for item in forecast_data['list']:
                if count >= 3:
                    break
                date_str = item['dt_txt'].split()[0]
                if date_str not in seen_dates:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    day_name = date_obj.strftime('%m/%d (%a)')

                    temp_max = round(item['main']['temp_max'])
                    temp_min = round(item['main']['temp_min'])
                    desc = item['weather'][0]['description']
                    emoji = get_weather_emoji(item['weather'][0]['id'])

                    weather_info += f"{emoji} {day_name}: {temp_max}°C / {temp_min}°C - {desc}\n"

                    seen_dates.add(date_str)
                    count += 1

        return weather_info.strip()

    except Exception as e:
        return f"⚠ 天気情報のフォーマット中にエラー: {str(e)}"


def get_weather_emoji(weather_id: int) -> str:
    """
    Map OpenWeatherMap weather condition codes to emojis.

    Args:
        weather_id (int): Weather condition ID from OpenWeatherMap.

    Returns:
        str: Emoji representing the weather condition.
    """
    if 200 <= weather_id <= 232:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "🌦️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif 600 <= weather_id <= 622:
        return "❄️"
    elif 701 <= weather_id <= 781:
        return "🌫️"
    elif weather_id == 800:
        return "☀️"
    elif 801 <= weather_id <= 804:
        return "☁️"
    else:
        return "🌤️"