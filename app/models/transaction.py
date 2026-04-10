import uuid
from datetime import datetime, timezone, date

from sqlalchemy import String, Float, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(20))  # "income" | "expenditure"
    amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(80))  # e.g. "food", "transport", "black_tax"
    description: Mapped[str] = mapped_column(Text, default="")
    date: Mapped[date] = mapped_column(Date, default=lambda: datetime.now(timezone.utc).date())
    source: Mapped[str] = mapped_column(String(30), default="manual")  # "manual" | "bank_sms"
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.type} ₦{self.amount:,.0f} [{self.category}]>"
