"""
WeatherCrew - Optimized 3-agent system for multilingual weather chatbot.
Coordinates agents and tasks with integrated advisory functionality in the response agent.
"""

from crewai import Crew, Process
from crewai.llm import LLM
import os
from typing import Optional

from .agents.weather_agents import create_weather_agents
from .tasks.weather_tasks import create_weather_tasks, create_simple_response_tasks
from .tools.weather_tools import detect_language
from .intent_classifier import classify_intent, IntentClassifier


class WeatherCrew:
    """
    Optimized 3-agent system for processing weather queries in Japanese or English using CrewAI.
    Features intelligent intent classification and integrated advisory functionality.

    This class orchestrates:
      - Intent classification (rule-based + LLM hybrid)
      - Language detection for all query types
      - Weather data fetching via OpenWeatherMap (when needed)
      - Integrated weather-based advice and culturally appropriate responses
      - Efficient task routing based on query type
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
            model=os.getenv("LLM_MODEL"),
            provider="google",
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        self.agents = create_weather_agents(self.gemini_llm)
        self.intent_classifier = IntentClassifier(self.gemini_llm)

    def process_weather_query(self, user_query: str, location: str = "") -> str:
        """
        Process a user query with intelligent intent classification and routing.
        Uses hybrid rule-based + LLM intent classification for optimal efficiency.

        Args:
            user_query (str): The input question in Japanese or English.
            location (str): Optional override location (for weather queries only).

        Returns:
            str: A natural response in the same language as the input.
        """
        try:
            # Step 1: Detect language using tool
            language = detect_language(user_query)
            
            # Step 2: Classify intent using hybrid approach
            intent = classify_intent(user_query, self.gemini_llm, language)
            
            # Step 3: Create appropriate tasks based on intent
            if intent == IntentClassifier.WEATHER_QUERY:
                # Full weather processing pipeline with integrated advisory
                tasks = create_weather_tasks(user_query, location, self.agents)
                agents_to_use = list(self.agents.values())
            else:
                # Simplified response pipeline for non-weather queries
                tasks = create_simple_response_tasks(user_query, intent, language, self.agents)
                # Only use response agent for non-weather queries
                agents_to_use = [self.agents['response']]

            # Step 4: Execute the crew with appropriate agents and tasks
            crew = Crew(
                agents=agents_to_use,
                tasks=list(tasks.values()),
                process=Process.sequential,
                verbose=True,
                memory=False
            )

            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            # Return error message in both languages
            error_msg = str(e)
            if language == "japanese":
                return f"⚠️ 処理中にエラーが発生しました: {error_msg}"
            else:
                return f"⚠️ An error occurred during processing: {error_msg}"