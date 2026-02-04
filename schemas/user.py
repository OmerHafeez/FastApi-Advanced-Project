"""
Pydantic schemas for request/response validation.
These schemas define what data is expected in API requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


# ========== Base Schemas ==========

class UserBase(BaseModel):
    """
    Base schema with common user fields.
    This is inherited by other schemas to avoid repetition.
    """
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")


# ========== Request Schemas ==========

class UserCreate(UserBase):
    """
    Schema for creating a new user (registration).
    Includes password which is required for new users.
    """
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=100,
        description="Password (min 8 characters)"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "username": "johndoe",
                "password": "securepassword123"
            }
        }
    )


class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    All fields are optional - only provided fields will be updated.
    """
    email: Optional[EmailStr] = Field(None, description="New email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="New username")
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="New password")
    is_active: Optional[bool] = Field(None, description="Account active status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe_updated",
                "email": "john.new@example.com"
            }
        }
    )


class UserLogin(BaseModel):
    """
    Schema for user login.
    Can login with either email or username.
    """
    email: EmailStr = Field(..., description="User's email for login")
    password: str = Field(..., description="User's password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "securepassword123"
            }
        }
    )


# ========== Response Schemas ==========

class UserResponse(UserBase):
    """
    Schema for user data in responses.
    Excludes sensitive information like passwords.
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Allows SQLAlchemy models to be converted to Pydantic models
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """
    Schema for authentication token response.
    Returned after successful login.
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }
    )


class MessageResponse(BaseModel):
    """
    Schema for simple message responses.
    Used for success/error messages.
    """
    message: str = Field(..., description="Response message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation completed successfully"
            }
        }
    )


# ========== Token Payload Schema ==========

class TokenPayload(BaseModel):
    """
    Schema for JWT token payload.
    This is the data encoded inside the JWT token.
    """
    sub: int = Field(..., description="Subject (user ID)")
    exp: datetime = Field(..., description="Expiration timestamp")
