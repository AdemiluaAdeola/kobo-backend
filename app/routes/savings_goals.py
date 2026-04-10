from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.savings_goal import SavingsGoal
from app.schemas.savings_goal import (
    SavingsGoalCreate, SavingsGoalUpdate, SavingsGoalResponse, ContributeRequest,
)

router = APIRouter(prefix="/api/savings-goals", tags=["Savings Goals (Spaces)"])


@router.get("", response_model=list[SavingsGoalResponse])
async def list_goals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SavingsGoal).where(SavingsGoal.user_id == current_user.id)
    )
    goals = result.scalars().all()
    return [_goal_to_response(g) for g in goals]


@router.post("", response_model=SavingsGoalResponse, status_code=201)
async def create_goal(
    data: SavingsGoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    goal = SavingsGoal(
        user_id=current_user.id,
        name=data.name,
        target_amount=data.target_amount,
        auto_save_rule=data.auto_save_rule,
        deadline=data.deadline,
        emoji=data.emoji,
    )
    db.add(goal)
    await db.flush()
    await db.refresh(goal)
    return _goal_to_response(goal)


@router.put("/{goal_id}", response_model=SavingsGoalResponse)
async def update_goal(
    goal_id: str,
    data: SavingsGoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    goal = await _get_goal(goal_id, current_user.id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(goal, field, value)
    await db.flush()
    await db.refresh(goal)
    return _goal_to_response(goal)


@router.post("/{goal_id}/contribute", response_model=SavingsGoalResponse)
async def contribute(
    goal_id: str,
    data: ContributeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add money to a savings goal."""
    goal = await _get_goal(goal_id, current_user.id, db)
    goal.current_amount += data.amount
    await db.flush()
    await db.refresh(goal)
    return _goal_to_response(goal)


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(
    goal_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    goal = await _get_goal(goal_id, current_user.id, db)
    await db.delete(goal)


# ── helpers ──

async def _get_goal(goal_id: str, user_id: str, db: AsyncSession) -> SavingsGoal:
    result = await db.execute(
        select(SavingsGoal).where(SavingsGoal.id == goal_id, SavingsGoal.user_id == user_id)
    )
    goal = result.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=404, detail="Savings goal not found")
    return goal


def _goal_to_response(goal: SavingsGoal) -> SavingsGoalResponse:
    return SavingsGoalResponse(
        id=goal.id,
        user_id=goal.user_id,
        name=goal.name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        auto_save_rule=goal.auto_save_rule,
        deadline=goal.deadline,
        emoji=goal.emoji,
        progress_pct=goal.progress_pct,
        created_at=goal.created_at,
    )
