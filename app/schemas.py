from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List
from datetime import datetime

from app.models import UserRole


# ============ USER SCHEMAS ============

class UserBase(BaseModel):
    """Shared user fields."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Request: Create new user."""
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.READER  # Default role


class UserResponse(UserBase):
    """Response: User data (excludes password!)."""
    model_config = ConfigDict(from_attributes=True)  # Convert from ORM model
    
    id: str
    role: UserRole
    created_at: datetime


class UserLogin(BaseModel):
    """Request: Login credentials."""
    username: str
    password: str


# ============ POST SCHEMAS ============

class PostBase(BaseModel):
    """Shared post fields."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=10)


class PostCreate(PostBase):
    """Request: Create post."""
    published: bool = False  # Authors create drafts by default


class PostUpdate(BaseModel):
    """Request: Update post (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    published: Optional[bool] = None


class PostResponse(PostBase):
    """Response: Post with author info."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    published: bool
    created_at: datetime
    updated_at: datetime
    author: UserResponse  # Nested author data
    
    # Permission hints for frontend
    can_edit: bool = False
    can_delete: bool = False


class PostListResponse(BaseModel):
    """Response: Paginated list of posts."""
    items: List[PostResponse]
    total: int


# ============ AUTH SCHEMAS ============

class Token(BaseModel):
    """Response: JWT tokens."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Internal: Decoded JWT content."""
    sub: str  # User ID
    role: str
    exp: datetime 