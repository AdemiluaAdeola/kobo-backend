"""Smart nudges endpoint."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.security import get_current_user
from ...models.nudge import Nudge
from ...models.user import User
from ...schemas.nudge import NudgeResponse

router = APIRouter(prefix="/nudges", tags=["Nudges"])


@router.get(
    "",
    response_model=list[NudgeResponse],
    summary="Get smart nudges",
    description="Context-aware financial notifications. 'You just got paid—auto-save 10%?' Right message, right time.",
)
async def get_nudges(
    unread_only: bool = Query(False, description="Only return unread nudges"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Nudge).where(Nudge.user_id == current_user.id)

    if unread_only:
        query = query.where(Nudge.is_read == False)  # noqa: E712

    query = query.order_by(Nudge.created_at.desc()).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.patch(
    "/{nudge_id}/read",
    response_model=NudgeResponse,
    summary="Mark a nudge as read",
)
async def mark_nudge_read(
    nudge_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Nudge).where(Nudge.id == nudge_id, Nudge.user_id == current_user.id)
    )
    nudge = result.scalar_one_or_none()
    if not nudge:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nudge not found")

    nudge.is_read = True
    await db.flush()
    await db.refresh(nudge)
    return nudge
