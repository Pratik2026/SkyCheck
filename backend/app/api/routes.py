from fastapi import APIRouter, Depends
from backend.app.schema import ChatRequest, ChatResponse
from backend.app.services.weather_service import WeatherService
from backend.app.core.config import settings
import logging
import re

router = APIRouter()
logger = logging.getLogger("jpn_weather_bot.api")


def get_weather_service() -> WeatherService:
    return WeatherService()


def detect_language(text: str) -> str:
    """Detect if the input text is in Japanese or English"""
    has_japanese = bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', text))
    return 'japanese' if has_japanese else 'english'


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    weather_service: WeatherService = Depends(get_weather_service),
):
    detected_language = detect_language(request.message)
    logger.info("Received %s chat request: %s", detected_language, request.message[:80])
    
    try:
        result = await weather_service.process(request.message, request.location)
        return ChatResponse(response=result, success=True)
    except Exception as e:
        logger.error("chat_endpoint error: %s", str(e))
        
        # Return error message in detected language
        if detected_language == 'japanese':
            error_message = "申し訳ございませんが、処理中にエラーが発生しました。もう一度お試しください。"
        else:
            error_message = "Sorry, an error occurred during processing. Please try again."
            
        return ChatResponse(
            response=error_message,
            success=False,
            error=str(e),
        )
    crew_ok = getattr(weather_service, "crew", None) is not None
    env_status = {
        "google_api_key": bool(settings.GOOGLE_API_KEY),
        "weather_api_key": bool(settings.OPENWEATHERMAP_API_KEY),
        "serper_api_key": bool(settings.SERPER_API_KEY),
    }
    is_healthy = crew_ok and env_status["google_api_key"] and env_status["weather_api_key"]

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "crew_initialized": crew_ok,
        "environment_variables": env_status,
        "ai_model": "google/gemini-2.0-flash",
        "weather_api": "OpenWeatherMap",
        "supported_languages": ["Japanese", "English"],
        "features": ["voice_input", "multilingual_support", "dynamic_location_extraction"]
    }