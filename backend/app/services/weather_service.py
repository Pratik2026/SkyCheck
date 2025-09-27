from typing import Optional
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from app.crew.weather_crew import WeatherCrew
from app.core.config import settings
import logging

logger = logging.getLogger("jpn_weather_bot.weather_service")


class WeatherServiceError(Exception):
    """Custom exception for weather service errors"""
    def __init__(self, message: str, error_code: str = "WEATHER_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class WeatherService:
    """
    Service layer for handling weather queries via the multi-agent WeatherCrew.
    """

    def __init__(self, crew: Optional[WeatherCrew] = None):
        if crew:
            self.crew = crew
        else:
            if not settings.GOOGLE_API_KEY:
                raise WeatherServiceError(
                    "AI service is currently unavailable",
                    "CONFIGURATION_ERROR"
                )
            if not settings.OPENWEATHERMAP_API_KEY:
                raise WeatherServiceError(
                    "Weather service is currently unavailable", 
                    "CONFIGURATION_ERROR"
                )

            try:
                self.crew = WeatherCrew(google_api_key=settings.GOOGLE_API_KEY)
            except Exception as e:
                logger.error("Failed to initialize WeatherCrew: %s", str(e))
                raise WeatherServiceError(
                    "AI service initialization failed",
                    "INITIALIZATION_ERROR"
                ) from e

    async def process(self, user_query: str, location: str = "") -> str:
        if not self.crew:
            raise WeatherServiceError(
                "Weather service is not available",
                "SERVICE_UNAVAILABLE"
            )

        logger.info("Processing weather query: %s (location=%s)", user_query[:50], location or "auto-detect")

        try:
            result = await run_in_threadpool(
                self.crew.process_weather_query, user_query, location
            )
            
            # Check if the result indicates an error
            if result and (result.startswith("⚠") or "error occurred during processing" in result.lower()):
                # Parse the error to provide better error handling
                if "api key not valid" in result.lower():
                    raise WeatherServiceError(
                        "Invalid API key - please check your configuration",
                        "INVALID_API_KEY"
                    )
                elif "timeout" in result.lower():
                    raise WeatherServiceError(
                        "Request timeout - service is taking too long to respond",
                        "TIMEOUT_ERROR"
                    )
                elif "rate limit" in result.lower() or "quota" in result.lower():
                    raise WeatherServiceError(
                        "Service is currently busy - please try again in a moment",
                        "RATE_LIMIT_ERROR"
                    )
                else:
                    raise WeatherServiceError(
                        "Failed to process weather request",
                        "PROCESSING_ERROR"
                    )
            
            return result
            
        except WeatherServiceError:
            # Re-raise our custom errors
            raise
        except Exception as exc:
            logger.exception("Error during weather processing")
            
            # Parse different types of errors
            error_str = str(exc).lower()
            if "authentication" in error_str or "api key" in error_str:
                raise WeatherServiceError(
                    "Invalid API key - please check your configuration",
                    "INVALID_API_KEY"
                ) from exc
            elif "timeout" in error_str:
                raise WeatherServiceError(
                    "Request timeout - please try again",
                    "TIMEOUT_ERROR"
                ) from exc
            elif "network" in error_str or "connection" in error_str:
                raise WeatherServiceError(
                    "Network error - please check your connection",
                    "NETWORK_ERROR"
                ) from exc
            else:
                raise WeatherServiceError(
                    "Weather processing failed - please try again",
                    "PROCESSING_ERROR"
                ) from exc