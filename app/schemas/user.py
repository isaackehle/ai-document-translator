"""User Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Schema for user creation."""

    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserUpdate(BaseModel):
    """Schema for user update."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Schema for user in database."""

    id: int
    created_at: datetime
    updated_at: datetime
    is_superuser: bool

    class Config:
        from_attributes = True


class User(UserInDB):
    """Schema for user response."""

    pass
