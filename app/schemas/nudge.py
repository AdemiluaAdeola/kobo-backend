from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class NudgeResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    type: str
    message: str
    is_read: bool
    trigger_date: Optional[date] = None
    created_at: datetime
