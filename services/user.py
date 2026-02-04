"""
User service for database operations (CRUD).
This service handles all user-related database queries.
"""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.user import UserCreate, UserUpdate
from services.auth import auth_service


class UserService:
    """
    Service class for user CRUD operations.
    All methods are async because we're using async SQLAlchemy.
    """
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Create a new user in the database.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created user object
        """
        # Hash the password before storing
        hashed_password = auth_service.hash_password(user_data.password)
        
        # Create user object
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            is_active=True
        )
        
        # Add to database
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)  # Get the updated object with ID
        
        return db_user
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.
        
        Args:
            db: Database session
            user_id: ID of the user to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Get a user by their email address.
        
        Args:
            db: Database session
            email: Email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        Get a user by their username.
        
        Args:
            db: Database session
            username: Username to search for
            
        Returns:
            User object if found, None otherwise
        """
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_users(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of user objects
        """
        result = await db.execute(
            select(User).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def update_user(
        db: AsyncSession, 
        user_id: int, 
        user_data: UserUpdate
    ) -> Optional[User]:
        """
        Update user information.
        
        Args:
            db: Database session
            user_id: ID of the user to update
            user_data: Updated user data
            
        Returns:
            Updated user object if found, None otherwise
        """
        # Get the user
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        
        # Update only provided fields
        update_data = user_data.model_dump(exclude_unset=True)
        
        # If password is being updated, hash it
        if "password" in update_data:
            update_data["hashed_password"] = auth_service.hash_password(
                update_data.pop("password")
            )
        
        # Apply updates
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """
        Delete a user from the database.
        
        Args:
            db: Database session
            user_id: ID of the user to delete
            
        Returns:
            True if user was deleted, False if user not found
        """
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return False
        
        await db.delete(user)
        await db.commit()
        
        return True
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession, 
        email: str, 
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user by email and password.
        
        Args:
            db: Database session
            email: User's email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        # Get user by email
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return None
        
        # Verify password
        if not auth_service.verify_password(password, user.hashed_password):
            return None
        
        # Check if account is active
        if not user.is_active:
            return None
        
        return user


# Create a singleton instance
user_service = UserService()
