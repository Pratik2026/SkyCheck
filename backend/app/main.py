from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import routes
from backend.app.core.config import settings
from backend.app.core.logging_setup import configure_logging
from backend.app.services.weather_service import WeatherService
from backend.app.crew.weather_crew import WeatherCrew
import logging

logger = configure_logging()

app = FastAPI(
    title=settings.app_name,
    description="AI-powered Japanese weather chatbot using CrewAI and Google Gemini",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up app and initializing Weather Crew...")
    


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    # If you need to close any connections or flush logs, do here.
