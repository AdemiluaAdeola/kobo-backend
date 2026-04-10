from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.debt import Debt
from app.schemas.debt import DebtCreate, DebtUpdate, DebtResponse

router = APIRouter(prefix="/api/debts", tags=["Debts"])


@router.get("", response_model=list[DebtResponse])
async def list_debts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Debt).where(Debt.user_id == current_user.id).order_by(Debt.due_date.asc().nullslast())
    )
    return result.scalars().all()


@router.post("", response_model=DebtResponse, status_code=201)
async def create_debt(
    data: DebtCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    debt = Debt(
        user_id=current_user.id,
        name=data.name,
        type=data.type,
        amount=data.amount,
        interest_rate=data.interest_rate,
        due_date=data.due_date,
        creditor=data.creditor,
        notes=data.notes,
    )
    db.add(debt)
    await db.flush()
    await db.refresh(debt)
    return debt


@router.put("/{debt_id}", response_model=DebtResponse)
async def update_debt(
    debt_id: str,
    data: DebtUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Debt).where(Debt.id == debt_id, Debt.user_id == current_user.id)
    )
    debt = result.scalar_one_or_none()
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(debt, field, value)
    await db.flush()
    await db.refresh(debt)
    return debt


@router.delete("/{debt_id}", status_code=204)
async def delete_debt(
    debt_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Debt).where(Debt.id == debt_id, Debt.user_id == current_user.id)
    )
    debt = result.scalar_one_or_none()
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    await db.delete(debt)


@router.get("/payoff-plan")
async def payoff_plan(
    strategy: str = "avalanche",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a debt payoff recommendation (avalanche or snowball)."""
    result = await db.execute(
        select(Debt).where(Debt.user_id == current_user.id, Debt.is_paid == False)
    )
    debts = result.scalars().all()

    if not debts:
        return {"strategy": strategy, "plan": [], "message": "No outstanding debts 🎉"}

    if strategy == "avalanche":
        # Pay highest interest first
        ordered = sorted(debts, key=lambda d: d.interest_rate, reverse=True)
    else:
        # Snowball: pay smallest balance first
        ordered = sorted(debts, key=lambda d: d.amount)

    plan = [
        {
            "order": i + 1,
            "name": d.name,
            "amount": d.amount,
            "interest_rate": d.interest_rate,
            "type": d.type,
        }
        for i, d in enumerate(ordered)
    ]
    return {
        "strategy": strategy,
        "total_owed": sum(d.amount for d in ordered),
        "plan": plan,
    }
