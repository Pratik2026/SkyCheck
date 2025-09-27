"""
WeatherCrew tasks configuration.
Contains all task definitions for the multilingual weather chatbot workflow
including both weather-specific and general response tasks.
"""

from crewai import Task
from typing import Dict


def create_weather_tasks(user_query: str, location: str, agents: Dict) -> Dict[str, Task]:
    """
    Create and return weather-related tasks for full weather processing pipeline.
    
    Args:
        user_query (str): The user's input query.
        location (str): Optional location override.
        agents (Dict): Dictionary of agents to assign tasks to.
        
    Returns:
        Dict[str, Task]: Dictionary containing all configured weather tasks.
    """
    
    parse_task = Task(
        description=f"""
        Analyze this weather-related user input: "{user_query}"
        
        Your tasks:
        1. Using your advanced natural language understanding, extract the location mentioned in the query:
           - Look for city names, region names, country names, landmarks, or any geographical references
           - Handle variations and abbreviations (NYC→New York City, SF→San Francisco, LA→Los Angeles)
           - Understand nicknames (Big Apple→New York, City of Angels→Los Angeles, Sin City→Las Vegas)
           - For Japanese queries, identify place names in kanji/hiragana/katakana (東京→Tokyo, 大阪→Osaka)
           - Handle mixed language queries (What's the weather in 京都? → Kyoto)
           - Consider landmark references (Where the Eiffel Tower is → Paris)
           - If multiple locations mentioned, pick the most relevant one for weather inquiry
           - Extract informal references intelligently
           
        2. Determine the type of weather request (current weather, forecast, specific conditions, etc.)
        3. Identify the time frame (now, today, tomorrow, this week, etc.)
        4. Note any specific concerns or preferences mentioned
        
        Override location if specified: {location or 'None specified'}
        Default fallback if no location found: Tokyo
        
        """,
        agent=agents['conversation'],
        expected_output="""A detailed analysis containing:
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
        - Weather conditions and their implications for daily activities
        - Practical advice for clothing, transportation, outdoor activities
        - Seasonal considerations and local customs
        - Cultural appropriateness of suggestions
        """,
        agent=agents['advisor'],
        expected_output="Culturally appropriate recommendations based on weather conditions",
        context=[parse_task, weather_task]
    )

    response_task = Task(
        description=f"""
        Create a natural response based on the original user input "{user_query}".
        
        Requirements:
        - Respond in the SAME LANGUAGE as the user's input
        - Seamlessly combine weather information and recommendations in a natural flow
        - Match the tone and formality appropriate for the detected language
        - Include the weather data in a clear, readable format
        - Make the response feel conversational and helpful, not robotic
        - Acknowledge the specific location that was extracted and used
        """,
        agent=agents['response'],
        expected_output="Natural response in the user's language with weather info and practical advice",
        context=[parse_task, weather_task, advice_task]
    )

    return {
        'parse': parse_task,
        'weather': weather_task,
        'advice': advice_task,
        'response': response_task
    }


def create_simple_response_tasks(user_query: str, intent: str, language: str, agents: Dict) -> Dict[str, Task]:
    """
    Create simplified tasks for non-weather queries.
    
    Args:
        user_query (str): The user's input query.
        intent (str): Classified intent (GREETING, CAPABILITY_INFO, GENERAL_CHAT).
        language (str): Detected language ('japanese' or 'english').
        agents (Dict): Dictionary of agents to assign tasks to.
        
    Returns:
        Dict[str, Task]: Dictionary containing simple response task.
    """
    
    # Customize response based on intent
    if intent == "GREETING":
        task_description = f"""
        Respond to this greeting: "{user_query}"
        Language: {language}
        
        Provide a warm, welcoming response that:
        - Greets the user appropriately in their language
        - Briefly mentions that you're a weather chatbot
        - Invites them to ask about weather anywhere in the world
        - Uses appropriate cultural politeness levels
        
        Keep it friendly and concise.
        """
        
    elif intent == "CAPABILITY_INFO":
        task_description = f"""
        Respond to this capability/help query: "{user_query}"
        Language: {language}
        
        Explain your weather chatbot capabilities:
        - Real-time weather information for any location worldwide
        - Support for both Japanese and English
        - Voice input capability (mention this feature)
        - Current conditions and forecasts
        - Weather-based advice and recommendations
        - Intelligent location detection from natural language
        
        Be informative but conversational.
        """
        
    else:  # GENERAL_CHAT
        task_description = f"""
        Respond to this general conversation: "{user_query}"
        Language: {language}
        
        Provide a natural, friendly response that:
        - Addresses their message appropriately
        - Maintains a warm, conversational tone
        - Gently guides the conversation toward weather topics if appropriate
        - Uses appropriate cultural communication style
        
        Keep it natural and engaging.
        """

    response_task = Task(
        description=task_description,
        agent=agents['response'],
        expected_output=f"Natural, helpful response in {language} appropriate for {intent} intent"
    )

    return {
        'response': response_task
    }