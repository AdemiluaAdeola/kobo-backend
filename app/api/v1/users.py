"""User profile endpoint."""
from fastapi import APIRouter, Depends

from ...core.security import get_current_user
from ...models.user import User
from ...schemas.user import UserResponse

from sqlalchemy.ext.asyncio import AsyncSession
from ...core.database import get_db
from ...schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
async def update_me(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.full_name is not None:
        current_user.full_name = data.full_name
    if data.monthly_income is not None:
        current_user.monthly_income = data.monthly_income
    if data.monthly_expenses is not None:
        current_user.monthly_expenses = data.monthly_expenses
    if data.savings_goal is not None:
        current_user.savings_goal = data.savings_goal
    if data.emergency_fund is not None:
        current_user.emergency_fund = data.emergency_fund
    
    await db.flush()
    await db.refresh(current_user)
    return current_user
