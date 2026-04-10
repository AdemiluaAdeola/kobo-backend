import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    hashed_password: Mapped[str] = mapped_column(String(255))
    currency: Mapped[str] = mapped_column(String(5), default="NGN")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    transactions = relationship("Transaction", back_populates="user", lazy="selectin")
    budgets = relationship("Budget", back_populates="user", lazy="selectin")
    savings_goals = relationship("SavingsGoal", back_populates="user", lazy="selectin")
    debts = relationship("Debt", back_populates="user", lazy="selectin")
    assets = relationship("Asset", back_populates="user", lazy="selectin")
    nudges = relationship("Nudge", back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"<User {self.email}>"
