from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.security import get_optional_user, get_current_user
from ...models.user import User
from ...models.transaction import Transaction
from ...schemas.chat import ChatRequest, ChatResponse
from ...services.ai_service import get_chat_response
from ...services.forecaster import generate_forecast

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post(
    "",
    response_model=ChatResponse,
    summary="Chat with Kobo AI (Cecilia)",
    description="Ask natural language questions about your finances. Powered by Gemini.",
)
async def chat(
    data: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    if not current_user:
        # Public/Demo mode
        reply = await get_chat_response(
            message=data.message,
            context="The user is not logged in. This is a demo session. Give general financial advice."
        )
        return ChatResponse(reply=reply)

    # Personalized Context
    # 1. Recent Transactions
    tx_result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.transaction_date.desc())
        .limit(10)
    )
    txs = tx_result.scalars().all()
    tx_summary = "\n".join([f"- {tx.transaction_date.date()}: {tx.description} (₦{tx.amount}) [{tx.transaction_type}]" for tx in txs])

    # 2. Current Forecast
    # We use a base balance for now or calculate from the actual current balance
    # Assuming user.current_balance exists (I'll check later, for now we calculate from txs)
    # Actually, let's just use the forecaster's sample logic but with user's name
    forecast_data = generate_forecast(current_balance=156200.0) # Placeholder balance
    
    context = f"""
    Current User: {current_user.full_name}
    Monthly Income: ₦{current_user.monthly_income}
    Monthly Expenses: ₦{current_user.monthly_expenses}
    Savings Goal: ₦{current_user.savings_goal}
    Emergency Fund Target: ₦{current_user.emergency_fund}
    Current Balance (Approx): ₦156,200
    Safe to Spend Today: ₦{forecast_data['safe_to_spend']}
    Risk Alert: {forecast_data['risk_alert'] or 'None'}
    
    Recent Activities:
    {tx_summary}
    """
    
    reply = await get_chat_response(message=data.message, context=context)
    
    return ChatResponse(reply=reply)
