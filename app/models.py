"""
SQLAlchemy models define your database tables.
Think of them as Django models, but you have more explicit control.
"""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, select
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from datetime import datetime
from enum import Enum as PyEnum
import uuid

Base = declarative_base()


class UserRole(str, PyEnum):
    """Roles determine what users can do."""
    READER = "reader"      # Can only read posts
    AUTHOR = "author"      # Can create and manage own posts
    ADMIN = "admin"        # Can do everything


class User(Base):
    __tablename__ = "users"
    
    # Primary key - using UUID instead of auto-increment for security
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Login credentials
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    # Role-based access control
    role: Mapped[UserRole] = mapped_column(default=UserRole.READER)
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationship: A user has many posts
    # "posts" attribute will contain a list of Post objects
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author", lazy="selectin")
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    
    # Content
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    published: Mapped[bool] = mapped_column(default=False)
    
    # Foreign key to author
    author_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationship: Each post has one author
    author: Mapped["User"] = relationship("User", back_populates="posts")
    
    def __repr__(self):
        status = "published" if self.published else "draft"
        return f"<Post '{self.title[:30]}' ({status})>"


# Helper function to check permissions
def can_edit_post(user: User, post: Post) -> bool:
    """Check if user can edit a specific post."""
    if user.role == UserRole.ADMIN:
        return True
    if user.role == UserRole.AUTHOR and post.author_id == user.id:
        return True
    return False


def can_delete_post(user: User, post: Post) -> bool:
    """Check if user can delete a specific post."""
    # Same logic as edit for this simple example
    return can_edit_post(user, post)


def can_publish_post(user: User) -> bool:
    """Check if user can change publish status."""
    # Only admins can publish (authors submit for review in real apps)
    return user.role == UserRole.ADMIN