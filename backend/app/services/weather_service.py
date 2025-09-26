from typing import Optional
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from backend.app.crew.weather_crew import WeatherCrew
from backend.app.core.config import settings
import logging

logger = logging.getLogger("jpn_weather_bot.weather_service")


class WeatherService:
    """
    Service layer for handling weather queries via the multi-agent WeatherCrew.
    """

    def __init__(self, crew: Optional[WeatherCrew] = None):
        if crew:
            self.crew = crew
        else:
            if not settings.GOOGLE_API_KEY:
                raise RuntimeError("GOOGLE_API_KEY is missing. Check your .env or environment variables.")
            if not settings.OPENWEATHERMAP_API_KEY:
                raise RuntimeError("OPENWEATHERMAP_API_KEY is missing. Check your .env or environment variables.")

            self.crew = WeatherCrew(google_api_key=settings.GOOGLE_API_KEY)

    async def process(self, user_query: str, location: str = "") -> str:
        if not self.crew:
            raise HTTPException(status_code=503, detail="Weather crew not initialized.")

        logger.info("Processing weather query: %s (location=%s)", user_query[:50], location or "auto-detect")

        try:
            return await run_in_threadpool(
                self.crew.process_weather_query, user_query, location
            )
        except Exception as exc:
            logger.exception("Error during weather processing")
            raise HTTPException(status_code=500, detail="Weather processing failed.") from exc
