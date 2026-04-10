from pydantic import BaseModel, EmailStr
from datetime import datetime


class WaitlistCreate(BaseModel):
    email: EmailStr
    city: str = ""


class WaitlistResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    email: str
    city: str
    created_at: datetime
