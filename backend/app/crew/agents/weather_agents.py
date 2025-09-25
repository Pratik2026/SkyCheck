"""
WeatherCrew agents configuration.
Contains all agent definitions for the multilingual weather chatbot.
"""

from crewai import Agent
from crewai.llm import LLM
from ..tools.weather_tools import get_weather_info, detect_language


def create_weather_agents(llm: LLM) -> dict:
    """
    Create and return all weather-related agents.
    
    Args:
        llm: The language model to use for agents.
        
    Returns:
        dict: Dictionary containing all configured agents.
    """
    
    conversation_agent = Agent(
        role="Multilingual Language and Location Specialist",
        goal="Understand user queries in Japanese or English, extract location information using natural language understanding",
        backstory="""You are an expert in both Japanese and English languages with advanced natural language 
        understanding capabilities. You can intelligently extract location names from user queries regardless 
        of how they phrase their request. You understand geographical references, city names, landmarks, 
        abbreviations (NYC, SF, LA), nicknames (Big Apple, City of Angels), and can infer locations from context. 
        You are particularly skilled at identifying locations mentioned in casual conversation and can handle 
        variations in spelling, informal references, and cultural location names in both languages.""",
        verbose=True,
        tools=[detect_language],
        llm=llm
    )

    weather_agent = Agent(
        role="Global Weather Information Specialist",
        goal="Fetch accurate and comprehensive weather data for any location worldwide",
        backstory="""You are a professional meteorologist with access to global weather data. 
        You can retrieve weather information for any city or location worldwide and provide 
        accurate current conditions and forecasts. You understand that location names extracted 
        by the conversation agent should be used as-is with the weather API, which can handle 
        various location formats and spellings.""",
        verbose=True,
        tools=[get_weather_info],
        llm=llm
    )

    advisor_agent = Agent(
        role="Multilingual Lifestyle Consultant",
        goal="Provide culturally appropriate recommendations based on weather conditions in the user's preferred language",
        backstory="""You are a lifestyle consultant who understands both Japanese and Western cultures. 
        You can provide weather-based recommendations that are appropriate for the user's cultural context 
        and communicate in their preferred language (Japanese or English). You understand seasonal clothing, 
        activities, and cultural practices related to weather in different regions.""",
        verbose=True,
        llm=llm
    )

    response_agent = Agent(
        role="Multilingual Response Formatter",
        goal="Create natural, conversational responses in Japanese or English based on user's language preference",
        backstory="""You are an expert at creating warm, natural responses in both Japanese and English. 
        You adapt your communication style, tone, and cultural references based on the detected language. 
        For Japanese, you use appropriate keigo and cultural context. For English, you use friendly, 
        conversational tone. You seamlessly integrate weather information with practical advice.""",
        verbose=True,
        llm=llm
    )

    return {
        'conversation': conversation_agent,
        'weather': weather_agent,
        'advisor': advisor_agent,
        'response': response_agent
    }