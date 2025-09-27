from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.core.config import settings
from app.core.logging_setup import configure_logging
from app.services.weather_service import WeatherService
from app.crew.weather_crew import WeatherCrew
import logging

logger = configure_logging()

app = FastAPI(
    title=settings.app_name,
    description="AI-powered Japanese weather chatbot using CrewAI and Google Gemini",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for separate frontend deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def get_weather_service() -> WeatherService:
    crew = getattr(app.state, "weather_crew", None)
    return WeatherService(crew=crew) if crew else WeatherService()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Weather API...")
    try:
        crew = WeatherCrew(google_api_key=settings.GOOGLE_API_KEY)
        app.state.weather_crew = crew
        logger.info("Weather Crew initialized successfully.")
    except Exception as e:
        app.state.weather_crew = None
        logger.exception("Failed to initialize Weather Crew: %s", e)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Weather API...")

# Root route for API
@app.get("/")
async def root():
    return {
        "message": "SkyCheck Weather API",
        "status": "running",
        "version": settings.version,
        "docs": "/docs",
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        }
    }

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "weather-api"}

# Include API routes (without /api prefix since this is backend only)
app.include_router(routes.router, dependencies=[Depends(get_weather_service)])