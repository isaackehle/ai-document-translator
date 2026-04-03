"""User Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str | None = None
    is_active: bool | None = True


class UserCreate(UserBase):
    """Schema for user creation."""

    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserUpdate(BaseModel):
    """Schema for user update."""

    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = Field(None, min_length=8)
    is_active: bool | None = None


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

    model_config = {"from_attributes": True}
