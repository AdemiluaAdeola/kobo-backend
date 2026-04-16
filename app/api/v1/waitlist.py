"""Waitlist signup endpoint — matches the HTML landing page form."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...models.waitlist import WaitlistEntry
from ...schemas.waitlist import WaitlistCreate, WaitlistResponse

router = APIRouter(prefix="/waitlist", tags=["Waitlist"])


@router.post(
    "",
    response_model=WaitlistResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Join the waitlist",
    description="Submit your email to join the Kobo early access waitlist.",
)
async def join_waitlist(data: WaitlistCreate, db: AsyncSession = Depends(get_db)):
    # Check if email already registered
    result = await db.execute(
        select(WaitlistEntry).where(WaitlistEntry.email == data.email)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already on the waitlist!",
        )

    entry = WaitlistEntry(email=data.email)
    db.add(entry)
    await db.flush()
    await db.refresh(entry)

    return WaitlistResponse(
        id=entry.id,
        email=entry.email,
        created_at=entry.created_at,
        message="✓ You're on the list! We'll be in touch.",
    )
