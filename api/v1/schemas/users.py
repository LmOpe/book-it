from pydantic import BaseModel, EmailStr, Field, UUID4
from api.v1.models.users import UserRole


class UserCreate(BaseModel):
    """User model for creating a new user."""

    full_name: str = Field(..., min_length=5, max_length=500)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole = Field(...)


class UserLogin(BaseModel):
    """User model for user login."""

    email: EmailStr = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)


class UserResponse(BaseModel):
    """User model for GET user response."""

    id: UUID4
    full_name: str
    email: EmailStr
    is_active: bool
    role: UserRole

    class Config:
        """Pydantic configuration."""
        from_attributes = True

class LoginResponse(BaseModel):
    """Login response model."""

    access_token: str
    refresh_token: str
