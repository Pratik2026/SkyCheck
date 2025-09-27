from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.api import routes
from backend.app.core.config import settings
from backend.app.core.logging_setup import configure_logging
from backend.app.services.weather_service import WeatherService
from backend.app.crew.weather_crew import WeatherCrew
import logging
import os
from pathlib import Path

logger = configure_logging()

app = FastAPI(
    title=settings.app_name,
    description="AI-powered Japanese weather chatbot using CrewAI and Google Gemini",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Update CORS for Render deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.onrender.com",
        "https://skycheck.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def get_weather_service() -> WeatherService:
    crew = getattr(app.state, "weather_crew", None)
    return WeatherService(crew=crew) if crew else WeatherService()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up app and initializing Weather Crew...")
    try:
        # initialize crew and attach to app.state
        crew = WeatherCrew(google_api_key=settings.GOOGLE_API_KEY)
        app.state.weather_crew = crew
        logger.info("Weather Crew initialized successfully.")
    except Exception as e:
        app.state.weather_crew = None
        logger.exception("Failed to initialize Weather Crew: %s", e)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")

# Include API routes with /api prefix
app.include_router(routes.router, prefix="/api", dependencies=[Depends(get_weather_service)])

# Serve React static files
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        """
        Serve React app for all non-API routes.
        This handles client-side routing.
        """
        # If the path is an API route, let FastAPI handle it
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("redoc"):
            return {"error": "API route not found"}
        
        # For all other routes, serve the React app
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        else:
            return {"error": "React app not found. Make sure to build the frontend."}

    @app.get("/")
    async def serve_react_root():
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        else:
            return {"message": "Weather Chatbot API is running! Build the frontend to see the app."}
else:
    # Fallback if static directory doesn't exist
    @app.get("/")
    async def api_root():
        return {
            "message": "Weather Chatbot API is running!",
            "status": "Backend only - Frontend not built yet",
            "docs": "/docs",
            "api": "/api"
        }