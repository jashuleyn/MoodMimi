from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = Field(default="default")


class EmotionScore(BaseModel):
    label: str
    score: float


class ChatResponse(BaseModel):
    reply: str
    emotion: str
    confidence: float
    tone: str
    suggestion: str
    scores: List[EmotionScore]
    is_crisis: bool
    model_used: str
    created_at: str


class HistoryItem(BaseModel):
    id: int
    session_id: str
    user_text: str
    bot_reply: str
    emotion: str
    confidence: float
    tone: str
    suggestion: str
    scores: List[EmotionScore]
    is_crisis: bool
    model_used: str
    created_at: str
