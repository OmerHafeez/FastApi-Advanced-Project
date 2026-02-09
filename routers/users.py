"""
Users router for CRUD operations on user resources.
These endpoints require authentication.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.user import UserResponse, UserUpdate, MessageResponse
from services.user import user_service
from models.user import User

from dependencies import get_current_user

# Create router with prefix and tags
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Get the profile of the currently authenticated user."
)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get your own user profile.
    
    Requires authentication token in the Authorization header.
    """
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
    description="Update your own profile information."
)
async def update_my_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update your own user profile.
    
    You can update:
    - **email**: New email address
    - **username**: New username
    - **password**: New password
    
    All fields are optional - only provided fields will be updated.
    """
    # Users can't change their own active status
    if user_data.is_active is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot change your own active status"
        )
    
    # Check if new email is already taken by another user
    if user_data.email:
        existing_user = await user_service.get_user_by_email(db, user_data.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use"
            )
    
    # Check if new username is already taken by another user
    if user_data.username:
        existing_user = await user_service.get_user_by_username(db, user_data.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken"
            )
    
    # Update user
    updated_user = await user_service.update_user(db, current_user.id, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )
    
    return updated_user


@router.delete(
    "/me",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete current user account",
    description="Delete your own user account (irreversible)."
)
async def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete your own account.
    
    **Warning**: This action is irreversible!
    """
    success = await user_service.delete_user(db, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )
    
    return MessageResponse(message="Account deleted successfully")
