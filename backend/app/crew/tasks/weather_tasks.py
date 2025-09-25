"""
WeatherCrew tasks configuration.
Contains all task definitions for the multilingual weather chatbot workflow.
"""

from crewai import Task
from typing import Dict


def create_weather_tasks(user_query: str, location: str, agents: Dict) -> Dict[str, Task]:
    """
    Create and return all weather-related tasks.
    
    Args:
        user_query (str): The user's input query.
        location (str): Optional location override.
        agents (Dict): Dictionary of agents to assign tasks to.
        
    Returns:
        Dict[str, Task]: Dictionary containing all configured tasks.
    """
    
    parse_task = Task(
        description=f"""
        Analyze this user input: "{user_query}"
        
        Your tasks:
        1. Use the detect_language tool to determine if the input is in Japanese or English
        
        2. Using your advanced natural language understanding, extract the location mentioned in the query:
           - Look for city names, region names, country names, landmarks, or any geographical references
           - Handle variations and abbreviations (NYC→New York City, SF→San Francisco, LA→Los Angeles)
           - Understand nicknames (Big Apple→New York, City of Angels→Los Angeles, Sin City→Las Vegas)
           - For Japanese queries, identify place names in kanji/hiragana/katakana (東京→Tokyo, 大阪→Osaka)
           - Handle mixed language queries (What's the weather in 京都? → Kyoto)
           - Consider landmark references (Where the Eiffel Tower is → Paris)
           - If multiple locations mentioned, pick the most relevant one for weather inquiry
           - Extract informal references intelligently
           
        3. Determine the type of weather request (current weather, forecast, specific conditions, etc.)
        4. Identify the time frame (now, today, tomorrow, this week, etc.)
        5. Note any specific concerns or preferences mentioned
        
        Override location if specified: {location or 'None specified'}
        Default fallback if no location found: Tokyo
        
        Examples of intelligent extraction:
        - "How's it in NYC?" → New York City
        - "Weather check for the Big Apple" → New York City  
        - "Is it sunny in 東京?" → Tokyo
        - "Check SF forecast" → San Francisco
        - "Temperature where the Space Needle is" → Seattle
        - "How's the weather in Chi-town?" → Chicago
        - "Will it rain in パリ tomorrow?" → Paris
        """,
        agent=agents['conversation'],
        expected_output="""A detailed analysis containing:
        - Detected language (japanese/english)
        - Extracted location name (in English for API compatibility, with high confidence)
        - Weather request type and time frame
        - Any specific user preferences or concerns
        - Brief explanation of location extraction logic used"""
    )

    weather_task = Task(
        description="""
        Based on the location intelligently extracted by the conversation agent, fetch comprehensive weather data.
        
        Instructions:
        1. Use the exact location name provided by the conversation agent
        2. Trust the LLM's location extraction - it has processed abbreviations, nicknames, and references
        3. If the API call fails due to location not found, the error will be handled gracefully
        4. Provide detailed current weather and forecast information
        
        The OpenWeatherMap API can handle various location formats, so use the extracted location as-is.
        """,
        agent=agents['weather'],
        expected_output="Detailed weather information including current conditions and forecast for the extracted location",
        context=[parse_task]
    )

    advice_task = Task(
        description=f"""
        Based on the weather data and the original user question "{user_query}", 
        provide appropriate recommendations. Consider:
        - The detected language and cultural context
        - Weather conditions and their implications for daily activities
        - Practical advice for clothing, transportation, outdoor activities
        - Cultural appropriateness of suggestions based on the detected language
        - Seasonal considerations and local customs
        """,
        agent=agents['advisor'],
        expected_output="Culturally appropriate recommendations based on weather conditions and user's language/cultural context",
        context=[parse_task, weather_task]
    )

    response_task = Task(
        description=f"""
        Create a natural response in the SAME LANGUAGE as the user's input "{user_query}".
        
        Requirements:
        - If input was in Japanese, respond in Japanese with appropriate politeness level (keigo when appropriate)
        - If input was in English, respond in friendly, conversational English
        - Seamlessly combine weather information and recommendations in a natural flow
        - Match the tone and formality appropriate for the detected language
        - Include the weather data in a clear, readable format
        - Make the response feel conversational and helpful, not robotic
        - Acknowledge the specific location that was extracted and used
        """,
        agent=agents['response'],
        expected_output="Natural response in the user's language (Japanese or English) with weather info and practical advice",
        context=[parse_task, weather_task, advice_task]
    )

    return {
        'parse': parse_task,
        'weather': weather_task,
        'advice': advice_task,
        'response': response_task
    }