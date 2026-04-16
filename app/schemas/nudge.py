"""Pydantic schemas for smart nudges."""
from datetime import datetime

from pydantic import BaseModel


class NudgeResponse(BaseModel):
    id: int
    message: str
    nudge_type: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
