import uuid
from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import String, Float, Date, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SavingsGoal(Base):
    """A 'Space' — e.g. Detty December, Rent 2026, Emergency Fund."""
    __tablename__ = "savings_goals"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    target_amount: Mapped[float] = mapped_column(Float)
    current_amount: Mapped[float] = mapped_column(Float, default=0.0)
    auto_save_rule: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )  # e.g. {"type": "payday", "amount": 25000} or {"type": "roundup", "nearest": 50}
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    emoji: Mapped[str] = mapped_column(String(10), default="🎯")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="savings_goals")

    @property
    def progress_pct(self) -> float:
        if self.target_amount <= 0:
            return 100.0
        return min(round(self.current_amount / self.target_amount * 100, 1), 100.0)

    def __repr__(self):
        return f"<SavingsGoal '{self.name}' {self.progress_pct}%>"
