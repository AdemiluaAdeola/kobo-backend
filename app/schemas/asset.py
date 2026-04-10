from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AssetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    type: str = Field(..., pattern="^(stocks|savings|crypto|property|other)$")
    value: float = Field(..., ge=0)


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    value: Optional[float] = Field(None, ge=0)


class AssetResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    name: str
    type: str
    value: float
    last_updated: datetime
    created_at: datetime
