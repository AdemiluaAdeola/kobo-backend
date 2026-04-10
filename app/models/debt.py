import uuid
from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Debt(Base):
    """Tracks formal (Palmcredit, Carbon) and informal (Uncle Tunde) debts."""
    __tablename__ = "debts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    type: Mapped[str] = mapped_column(String(20))  # "formal" | "informal"
    amount: Mapped[float] = mapped_column(Float)
    interest_rate: Mapped[float] = mapped_column(Float, default=0.0)  # annual %
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    creditor: Mapped[str] = mapped_column(String(120), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    is_paid: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="debts")

    def __repr__(self):
        return f"<Debt '{self.name}' ₦{self.amount:,.0f} ({self.type})>"
