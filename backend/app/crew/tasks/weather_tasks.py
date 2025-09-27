"""
WeatherCrew tasks configuration - Optimized 3-agent system.
Contains all task definitions for the multilingual weather chatbot workflow
with integrated advisory functionality in the response agent.
"""

from crewai import Task
from typing import Dict


def create_weather_tasks(user_query: str, location: str, agents: Dict) -> Dict[str, Task]:
    """
    Create and return weather-related tasks for optimized 3-agent processing pipeline.
    
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
        3. Provide detailed current weather and forecast information using ONLY API data
        4. Do NOT add interpretations, predictions, or context beyond what the API provides
        5. If the API call fails due to location not found, report the exact error
        
        Return the raw weather data without additional commentary or advice.
        """,
        agent=agents['weather'],
        expected_output="Factual weather information including current conditions and forecast for the extracted location, using only API-provided data",
        context=[parse_task]
    )

    response_task = Task(
        description=f"""
        Create a comprehensive natural response that combines weather information with practical advice.
        
        ## Primary Requirements:
        - Respond in the SAME LANGUAGE as the user's input: "{user_query}"
        - Use ONLY the weather data provided by the weather agent
        - Integrate practical advice based exclusively on the specific weather values
        - Make the response conversational and culturally appropriate
        - Acknowledge the specific location that was extracted and used

        ## Weather-Based Advisory Integration:
        Based EXCLUSIVELY on the provided weather data, include relevant advice:

        ### Temperature-Based Recommendations:
        - Below 5°C: Suggest heavy winter clothing, warm layers, heating considerations
        - 5-10°C: Recommend warm jacket, long pants, closed shoes, layers
        - 10-15°C: Advise light jacket or sweater, comfortable layers
        - 15-20°C: Suggest light clothing, maybe light jacket for evening
        - 20-25°C: Recommend comfortable casual wear, breathable fabrics
        - 25-30°C: Advise light, breathable clothing, sun protection
        - Above 30°C: Emphasize minimal, light-colored clothing, hydration, shade

        ### Condition-Based Advice:
        - Rain/Drizzle: Umbrella, waterproof clothing, non-slip shoes
        - Snow: Warm layers, waterproof boots, gloves, careful walking
        - Clear/Sunny: Sun protection, sunglasses, light colors
        - Cloudy: Comfortable clothing, possible light jacket
        - Windy: Wind-resistant clothing, secure loose items
        - High Humidity (>70%): Breathable fabrics, ventilation considerations

        ### Activity Suggestions:
        - Good weather: Outdoor activities, sightseeing, parks
        - Poor weather: Indoor alternatives, museums, shopping
        - Specific warnings: Travel delays, outdoor event considerations

        ## Cultural Considerations:
        - For Japanese responses: Use appropriate keigo, cultural context
        - For English responses: Friendly, conversational tone
        - Consider local customs and typical clothing preferences
        - Be practical and helpful without being prescriptive

        ## Response Structure:
        1. Natural acknowledgment of the query and location
        2. Current weather information (using exact API data)
        3. Integrated practical advice based on the specific conditions
        4. Forecast information if relevant (using exact API data)
        5. Friendly closing that invites further questions

        STRICT RULES:
        - Use ONLY weather values provided by the weather agent
        - Base advice ONLY on the specific temperature, humidity, and condition values
        - Do NOT add weather information not in the API response
        - Do NOT use general weather knowledge instead of provided data
        - Make advice logical and practical, not generic
        """,
        agent=agents['response'],
        expected_output="Natural, comprehensive response in the user's language combining weather data with practical advice, all based exclusively on API-provided information",
        context=[parse_task, weather_task]
    )

    return {
        'parse': parse_task,
        'weather': weather_task,
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
        - Briefly mentions that you're a weather chatbot with advisory capabilities
        - Invites them to ask about weather anywhere in the world
        - Uses appropriate cultural politeness levels
        - Mentions that you can provide weather-based clothing and activity advice
        
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
        - Intelligent weather-based advice and recommendations including:
          * Clothing suggestions based on temperature and conditions
          * Activity recommendations for the weather
          * Travel and outdoor planning advice
        - Intelligent location detection from natural language
        - Cultural awareness in communication and advice
        
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
        - Mentions your weather and advisory capabilities if relevant
        
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