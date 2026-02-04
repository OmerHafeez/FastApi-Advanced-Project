"""
Dependency functions for FastAPI dependency injection.
These are used to enforce authentication and authorization.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from services.auth import auth_service
from services.user import user_service
from models.user import User

# HTTP Bearer token scheme for authentication
# This tells FastAPI to look for "Authorization: Bearer <token>" header
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency that gets the current authenticated user.
    
    This function:
    1. Extracts the JWT token from the Authorization header
    2. Verifies the token and gets the user ID
    3. Fetches the user from the database
    4. Returns the user object
    
    Raises HTTPException if:
    - Token is missing or invalid
    - Token has expired
    - User doesn't exist
    - User account is inactive
    
    Usage:
        @app.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.username}
    """
    # Get the token from credentials
    token = credentials.credentials
    
    # Verify token and get user ID
    user_id = auth_service.verify_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user from database
    user = await user_service.get_user_by_id(db, user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Check if user account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user
