"""14-day cash flow forecast endpoint."""
from fastapi import APIRouter, Depends

from ...core.security import get_current_user
from ...models.user import User
from ...schemas.forecast import ForecastResponse
from ...services.forecaster import generate_forecast

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get(
    "",
    response_model=ForecastResponse,
    summary="Get 14-day cash flow forecast",
    description="Prophet-powered predictive cash flow. Returns daily balance predictions, safe-to-spend amount, and risk alerts.",
)
async def get_forecast(current_user: User = Depends(get_current_user)):
    # Use user-specific profile data for more personalized forecasting
    forecast_data = generate_forecast(
        current_balance=156_200.0, # Still using placeholder for base balance
        monthly_income=current_user.monthly_income,
        monthly_expenses=current_user.monthly_expenses,
        days=14
    )
    return ForecastResponse(**forecast_data)
