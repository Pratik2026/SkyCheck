from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Japanese Weather Chatbot API"
    version: str = "1.0.0"

    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY")
    OPENWEATHERMAP_API_KEY: str = Field(..., env="OPENWEATHERMAP_API_KEY")
    LLM_MODEL: str = Field(..., env="LLM_MODEL")

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
