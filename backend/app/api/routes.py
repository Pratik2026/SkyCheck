from fastapi import APIRouter, Depends, HTTPException
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


def extract_user_friendly_error(error_message: str, language: str) -> str:
    """Extract user-friendly error message from technical error details"""
    error_lower = error_message.lower()
    
    # API Key errors
    if "api key not valid" in error_lower or "invalid_argument" in error_lower:
        return "設定エラーです。しばらくしてから再度お試しください。" if language == 'japanese' else "Configuration error. Please try again later."
    
    # Authentication errors
    if "authentication" in error_lower or "unauthorized" in error_lower:
        return "認証エラーです。しばらくしてから再度お試しください。" if language == 'japanese' else "Authentication error. Please try again later."
    
    # Rate limit errors
    if "rate limit" in error_lower or "quota" in error_lower:
        return "リクエストが多すぎます。少し待ってから再度お試しください。" if language == 'japanese' else "Too many requests. Please wait a moment and try again."
    
    # Network/timeout errors
    if "timeout" in error_lower or "network" in error_lower:
        return "ネットワークエラーです。接続を確認して再度お試しください。" if language == 'japanese' else "Network error. Please check your connection and try again."
    
    # Weather API errors
    if "weather" in error_lower and "not found" in error_lower:
        return "指定された場所の天気情報が見つかりませんでした。" if language == 'japanese' else "Weather information for the specified location was not found."
    
    # Generic error
    return "申し訳ございませんが、エラーが発生しました。もう一度お試しください。" if language == 'japanese' else "Sorry, an error occurred. Please try again."


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    weather_service: WeatherService = Depends(get_weather_service),
):
    detected_language = detect_language(request.message)
    logger.info("Received %s chat request: %s", detected_language, request.message[:80])

    try:
        result = await weather_service.process(request.message, request.location)

        if result.startswith("⚠") or "error occurred during processing" in result.lower():
            user_friendly_error = extract_user_friendly_error(result, detected_language)
            logger.error("Weather processing error: %s", result)

            raise HTTPException(
                status_code=500,
                detail={
                    "error": user_friendly_error,
                    "code": "PROCESSING_ERROR",
                    "language": detected_language
                }
            )

        return ChatResponse(response=result, success=True)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("chat_endpoint unexpected error: %s", str(e))
        user_friendly_error = extract_user_friendly_error(str(e), detected_language)

        error_str = str(e).lower()
        if "authentication" in error_str or "api key" in error_str:
            status_code = 401
            error_code = "INVALID_API_KEY"
        elif "rate limit" in error_str or "quota" in error_str:
            status_code = 429
            error_code = "RATE_LIMIT_ERROR"
        elif "timeout" in error_str:
            status_code = 408
            error_code = "TIMEOUT_ERROR"
        else:
            status_code = 500
            error_code = "INTERNAL_ERROR"

        raise HTTPException(
            status_code=status_code,
            detail={
                "error": user_friendly_error,
                "code": error_code,
                "language": detected_language,
            },
        ) from e

    """Health check endpoint"""
    try:
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
    except Exception as e:
        logger.error("Health check failed: %s", str(e))
        raise HTTPException(status_code=503, detail="Service unavailable")