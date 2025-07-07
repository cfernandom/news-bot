"""
JWT token handling for authentication
Implements secure JWT token creation, verification, and management
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel


class TokenData(BaseModel):
    """Token data structure"""

    user_id: int
    username: str
    email: str
    roles: list[str]
    permissions: list[str]
    exp: datetime
    iat: datetime


class JWTHandler:
    """JWT token handler with secure defaults"""

    def __init__(self):
        self.secret_key = os.getenv(
            "JWT_SECRET_KEY", "your-secret-key-change-in-production"
        )
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

        if self.secret_key == "your-secret-key-change-in-production":
            import sys

            # Only raise error in production environments
            if (
                "pytest" not in sys.modules
                and os.getenv("ENVIRONMENT", "development") == "production"
            ):
                raise ValueError(
                    "JWT_SECRET_KEY environment variable must be set for production"
                )

    def create_access_token(
        self, user_data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token with user data and expiration

        Args:
            user_data: User information including id, username, email, roles, permissions
            expires_delta: Optional custom expiration time

        Returns:
            Encoded JWT token string
        """
        to_encode = user_data.copy()

        # Set expiration time
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )

        # Add standard JWT claims
        to_encode.update(
            {
                "exp": expire,
                "iat": datetime.now(timezone.utc),
                "iss": "preventia-analytics",  # Issuer
                "aud": "preventia-users",  # Audience
                "sub": str(user_data.get("user_id")),  # Subject
            }
        )

        # Encode token
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> bool:
        """
        Verify if token is valid and not expired

        Args:
            token: JWT token string

        Returns:
            True if token is valid, False otherwise
        """
        try:
            jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience="preventia-users",
                issuer="preventia-analytics",
            )
            return True
        except jwt.PyJWTError:
            return False

    def decode_token(self, token: str) -> TokenData:
        """
        Decode and validate JWT token, return user data

        Args:
            token: JWT token string

        Returns:
            TokenData object with user information

        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience="preventia-users",
                issuer="preventia-analytics",
            )

            # Extract user data
            user_id = payload.get("user_id")
            username = payload.get("username")
            email = payload.get("email")
            roles = payload.get("roles", [])
            permissions = payload.get("permissions", [])
            exp = datetime.fromtimestamp(payload.get("exp"))
            iat = datetime.fromtimestamp(payload.get("iat"))

            if not user_id or not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user data",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return TokenData(
                user_id=user_id,
                username=username,
                email=email,
                roles=roles,
                permissions=permissions,
                exp=exp,
                iat=iat,
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def refresh_token(self, token: str) -> str:
        """
        Refresh an existing token with new expiration

        Args:
            token: Current valid JWT token

        Returns:
            New JWT token with extended expiration
        """
        # Decode current token
        token_data = self.decode_token(token)

        # Create new token with same data but new expiration
        user_data = {
            "user_id": token_data.user_id,
            "username": token_data.username,
            "email": token_data.email,
            "roles": token_data.roles,
            "permissions": token_data.permissions,
        }

        return self.create_access_token(user_data)


# Global JWT handler instance
jwt_handler = JWTHandler()


# Convenience functions
def create_access_token(
    user_data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token - convenience function"""
    return jwt_handler.create_access_token(user_data, expires_delta)


def verify_token(token: str) -> bool:
    """Verify JWT token - convenience function"""
    return jwt_handler.verify_token(token)


def decode_token(token: str) -> TokenData:
    """Decode JWT token - convenience function"""
    return jwt_handler.decode_token(token)


def refresh_token(token: str) -> str:
    """Refresh JWT token - convenience function"""
    return jwt_handler.refresh_token(token)
