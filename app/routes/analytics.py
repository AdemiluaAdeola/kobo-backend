from datetime import datetime, timedelta, timezone, date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.models.asset import Asset
from app.models.debt import Debt
from app.schemas.analytics import NetWorthResponse, CashFlowSummary, ForecastPoint

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/net-worth", response_model=NetWorthResponse)
async def net_worth(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Calculate total net worth = assets − debts."""
    # Assets
    assets_result = await db.execute(
        select(Asset).where(Asset.user_id == current_user.id)
    )
    assets = assets_result.scalars().all()
    total_assets = sum(a.value for a in assets)
    assets_breakdown = [{"type": a.type, "name": a.name, "value": a.value} for a in assets]

    # Debts (unpaid)
    debts_result = await db.execute(
        select(Debt).where(Debt.user_id == current_user.id, Debt.is_paid == False)
    )
    debts = debts_result.scalars().all()
    total_liabilities = sum(d.amount for d in debts)
    debts_breakdown = [{"name": d.name, "amount": d.amount, "type": d.type} for d in debts]

    # This month's income / expenditure
    today = datetime.now(timezone.utc).date()
    month_start = today.replace(day=1)
    income_result = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == current_user.id,
            Transaction.type == "income",
            Transaction.date >= month_start,
        )
    )
    monthly_income = income_result.scalar()

    exp_result = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == current_user.id,
            Transaction.type == "expenditure",
            Transaction.date >= month_start,
        )
    )
    monthly_expenditure = exp_result.scalar()

    return NetWorthResponse(
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        net_worth=total_assets - total_liabilities,
        assets_breakdown=assets_breakdown,
        debts_breakdown=debts_breakdown,
        monthly_income=monthly_income,
        monthly_expenditure=monthly_expenditure,
    )


@router.get("/cash-flow", response_model=CashFlowSummary)
async def cash_flow(
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Summarise income vs expenditure over the last N days."""
    since = datetime.now(timezone.utc).date() - timedelta(days=days)

    income_result = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == current_user.id,
            Transaction.type == "income",
            Transaction.date >= since,
        )
    )
    total_income = income_result.scalar()

    exp_result = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == current_user.id,
            Transaction.type == "expenditure",
            Transaction.date >= since,
        )
    )
    total_expenditure = exp_result.scalar()

    # Top spending categories
    cat_result = await db.execute(
        select(Transaction.category, func.sum(Transaction.amount).label("total"))
        .where(
            Transaction.user_id == current_user.id,
            Transaction.type == "expenditure",
            Transaction.date >= since,
        )
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(5)
    )
    top_categories = [{"category": row[0], "amount": row[1]} for row in cat_result.all()]

    return CashFlowSummary(
        total_income=total_income,
        total_expenditure=total_expenditure,
        net=total_income - total_expenditure,
        top_categories=top_categories,
    )


@router.get("/forecast", response_model=list[ForecastPoint])
async def forecast(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    14-day balance forecast (stubbed linear projection).
    Uses average daily spend over the last 30 days to project future balance.
    """
    today = datetime.now(timezone.utc).date()
    thirty_days_ago = today - timedelta(days=30)

    # Total income last 30d
    inc = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == current_user.id,
            Transaction.type == "income",
            Transaction.date >= thirty_days_ago,
        )
    )
    total_income_30d = inc.scalar()

    # Total expenditure last 30d
    exp = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == current_user.id,
            Transaction.type == "expenditure",
            Transaction.date >= thirty_days_ago,
        )
    )
    total_exp_30d = exp.scalar()

    current_balance = total_income_30d - total_exp_30d
    daily_spend = total_exp_30d / 30 if total_exp_30d > 0 else 0

    points = []
    for day_offset in range(15):  # today + 14 days
        d = today + timedelta(days=day_offset)
        projected = max(current_balance - (daily_spend * day_offset), 0)
        label = "Today" if day_offset == 0 else f"Day {day_offset}"
        points.append(ForecastPoint(date=d, predicted_balance=round(projected, 2), label=label))

    return points
