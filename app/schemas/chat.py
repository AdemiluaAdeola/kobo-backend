"""Pydantic schemas for conversational AI chat."""
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    suggestion: str | None = None
    amount_referenced: float | None = None
