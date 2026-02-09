"""
User database model.
This defines the structure of the 'users' table in the database.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """
    User model representing a user in the database.
    
    Attributes:
        id: Unique identifier for the user
        email: User's email (unique, used for login)
        username: User's display name (unique)
        hashed_password: Securely hashed password
        is_active: Whether the user account is active
        is_admin: Whether the user has admin privileges
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # User credentials
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # User status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps (automatically managed)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        """String representation of the User object."""
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
