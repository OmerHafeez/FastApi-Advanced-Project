"""
Authentication service for password hashing and JWT token management.
This service handles all security-related operations.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings

# Password hashing context using bcrypt
# This is used to securely hash and verify passwords
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12
)


class AuthService:
    """
    Service class for authentication operations.
    Handles password hashing and JWT token operations.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            Hashed password string
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against
            
        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token for a user.
        
        Args:
            user_id: The ID of the user to create token for
            expires_delta: Optional custom expiration time
            
        Returns:
            Encoded JWT token string
        """
        # Set expiration time
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        # Create token payload (data to be encoded in the token)
        payload = {
            "sub": str(user_id),  # Subject (user ID)
            "exp": expire,        # Expiration time
            "iat": datetime.utcnow()  # Issued at time
        }
        
        # Encode the token using secret key and algorithm
        encoded_jwt = jwt.encode(
            payload, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string to verify
            
        Returns:
            User ID if token is valid, None otherwise
        """
        try:
            # Decode the token
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            
            # Extract user ID from payload
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            
            return int(user_id)
            
        except JWTError:
            # Token is invalid or expired
            return None


# Create a singleton instance
auth_service = AuthService()
