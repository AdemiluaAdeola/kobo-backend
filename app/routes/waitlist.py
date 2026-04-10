from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.waitlist import WaitlistEntry
from app.schemas.waitlist import WaitlistCreate, WaitlistResponse

router = APIRouter(prefix="/api/waitlist", tags=["Waitlist"])


@router.post("", response_model=WaitlistResponse, status_code=201)
async def join_waitlist(data: WaitlistCreate, db: AsyncSession = Depends(get_db)):
    """Join the Kobo early-access waitlist (no auth required)."""
    existing = await db.execute(
        select(WaitlistEntry).where(WaitlistEntry.email == data.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already on the waitlist")

    entry = WaitlistEntry(email=data.email, city=data.city)
    db.add(entry)
    await db.flush()
    await db.refresh(entry)
    return entry
