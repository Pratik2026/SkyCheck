from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message in Japanese or English", example="今日の東京の天気はどうですか？ / What's the weather like in Tokyo today?")
    location: str = Field(default="", description="Optional location override", example="Tokyo")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI response in the same language as the user's input")
    success: bool = Field(default=True, description="Whether the request was successful")
    error: str | None = Field(default=None, description="Error message if any")