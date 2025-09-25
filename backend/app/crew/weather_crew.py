"""
WeatherCrew - Main orchestrator for the multilingual weather chatbot.
Coordinates agents and tasks for intelligent weather query processing.
"""

from crewai import Crew, Process
from crewai.llm import LLM
import os
from typing import Optional

from .agents.weather_agents import create_weather_agents
from .tasks.weather_tasks import create_weather_tasks


class WeatherCrew:
    """
    Multi-agent system for processing weather queries in Japanese or English using CrewAI.
    Uses LLM-powered location extraction for intelligent understanding of user queries.

    This class orchestrates:
      - Language detection and intelligent location extraction using LLM
      - Fetching weather data via OpenWeatherMap for any global location
      - Providing culturally appropriate advice
      - Formatting natural responses in the detected language
    """

    def __init__(self, google_api_key: Optional[str] = None):
        """
        Initialize the WeatherCrew with Google Gemini LLM.

        Args:
            google_api_key (Optional[str]): Gemini API key (or loaded from env).
        """
        if google_api_key:
            os.environ["GOOGLE_API_KEY"] = google_api_key

        self.gemini_llm = LLM(
            model="gemini/gemini-2.0-flash",
            provider="google",
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        # Create agents using the factory function
        self.agents = create_weather_agents(self.gemini_llm)

    def process_weather_query(self, user_query: str, location: str = "") -> str:
        """
        Process a weather query in Japanese or English through the multi-agent Crew.
        Uses LLM-powered location extraction for intelligent understanding.

        Args:
            user_query (str): The input question in Japanese or English.
            location (str): Optional override location (defaults to LLM-extracted value).

        Returns:
            str: A natural response in the same language as the input with weather info and advice.
        """
        try:
            # Create tasks for this specific query
            tasks = create_weather_tasks(user_query, location, self.agents)

            # Create and execute the crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=list(tasks.values()),
                process=Process.sequential,
                verbose=True,
                memory=False
            )

            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            # Return error message in both languages
            return f"⚠ An error occurred during processing: {str(e)} / 処理中にエラーが発生しました: {str(e)}"