"""Transaction endpoints — add and list transactions with auto-categorization."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.security import get_current_user
from ...models.transaction import Transaction
from ...models.user import User
from ...schemas.transaction import TransactionCreate, TransactionResponse
from ...services.categorizer import categorize_transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=201,
    summary="Add a transaction (with auto-categorization)",
    description="Submit a transaction description (e.g. bank SMS) and Kobo will auto-categorize it.",
)
async def add_transaction(
    data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Auto-categorize
    category, confidence = categorize_transaction(data.description)

    txn = Transaction(
        user_id=current_user.id,
        amount=data.amount,
        description=data.description,
        category=category,
        confidence_score=confidence,
        transaction_type=data.transaction_type,
        transaction_date=data.transaction_date or datetime.now(timezone.utc),
    )
    db.add(txn)
    await db.flush()
    await db.refresh(txn)
    return txn


@router.get(
    "",
    response_model=list[TransactionResponse],
    summary="List transactions",
)
async def list_transactions(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.transaction_date.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()
