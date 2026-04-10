from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.nudge import Nudge
from app.schemas.nudge import NudgeResponse

router = APIRouter(prefix="/api/nudges", tags=["Nudges"])


@router.get("", response_model=list[NudgeResponse])
async def list_nudges(
    unread_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List nudges. By default returns only unread ones."""
    stmt = select(Nudge).where(Nudge.user_id == current_user.id)
    if unread_only:
        stmt = stmt.where(Nudge.is_read == False)
    stmt = stmt.order_by(Nudge.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.put("/{nudge_id}/dismiss", response_model=NudgeResponse)
async def dismiss_nudge(
    nudge_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a nudge as read/dismissed."""
    result = await db.execute(
        select(Nudge).where(Nudge.id == nudge_id, Nudge.user_id == current_user.id)
    )
    nudge = result.scalar_one_or_none()
    if not nudge:
        raise HTTPException(status_code=404, detail="Nudge not found")
    nudge.is_read = True
    await db.flush()
    await db.refresh(nudge)
    return nudge
