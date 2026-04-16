"""Pydantic schemas for waitlist."""
from datetime import datetime

from pydantic import BaseModel, EmailStr


class WaitlistCreate(BaseModel):
    email: EmailStr


class WaitlistResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    message: str = "You're on the list! We'll be in touch."

    model_config = {"from_attributes": True}
