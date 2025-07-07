"""
FastAPI dependencies for authentication and authorization
Implements secure dependency injection for protected endpoints
"""

from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select

from services.data.database.connection import db_manager
from services.data.database.models import User

from .jwt_handler import TokenData, decode_token
from .role_manager import check_permission, check_role, role_manager

# HTTP Bearer token scheme
security = HTTPBearer()


class AuthenticatedUser:
    """Represents an authenticated user with roles and permissions"""

    def __init__(self, user: User, token_data: TokenData):
        self.id = user.id
        self.username = user.username
        self.email = user.email
        self.full_name = user.full_name
        self.is_active = user.is_active
        self.is_superuser = user.is_superuser
        self.roles = token_data.roles
        self.permissions = token_data.permissions
        self.token_data = token_data

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission"""
        return permission in self.permissions or "*" in self.permissions

    def has_role(self, role: str) -> bool:
        """Check if user has a specific role"""
        return role in self.roles

    def has_any_role(self, roles: List[str]) -> bool:
        """Check if user has any of the specified roles"""
        return any(role in self.roles for role in roles)

    def has_all_roles(self, roles: List[str]) -> bool:
        """Check if user has all of the specified roles"""
        return all(role in self.roles for role in roles)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthenticatedUser:
    """
    Get current authenticated user from JWT token

    Args:
        credentials: HTTP Bearer credentials containing JWT token

    Returns:
        AuthenticatedUser object with user information and permissions

    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Decode and validate token
    token_data = decode_token(credentials.credentials)

    # Use global database manager

    # Fetch user from database
    async with db_manager.get_session() as session:
        query = select(User).where(User.id == token_data.user_id)
        result = await session.execute(query)
        user = result.scalar()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user account",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return AuthenticatedUser(user, token_data)


async def get_current_active_user(
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    """
    Get current active user (additional check for account status)

    Args:
        current_user: Current authenticated user

    Returns:
        AuthenticatedUser object

    Raises:
        HTTPException: If user account is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account"
        )

    return current_user


async def get_superuser(
    current_user: AuthenticatedUser = Depends(get_current_active_user),
) -> AuthenticatedUser:
    """
    Require superuser privileges

    Args:
        current_user: Current authenticated user

    Returns:
        AuthenticatedUser object

    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Superuser access required"
        )

    return current_user


def require_permission(permission: str):
    """
    Dependency factory for requiring specific permissions

    Args:
        permission: Required permission string (e.g., 'sources:read')

    Returns:
        FastAPI dependency function
    """

    async def check_user_permission(
        current_user: AuthenticatedUser = Depends(get_current_active_user),
    ) -> AuthenticatedUser:
        if not current_user.has_permission(permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission}",
            )
        return current_user

    return check_user_permission


def require_role(role: str):
    """
    Dependency factory for requiring specific roles

    Args:
        role: Required role name (e.g., 'source_admin')

    Returns:
        FastAPI dependency function
    """

    async def check_user_role(
        current_user: AuthenticatedUser = Depends(get_current_active_user),
    ) -> AuthenticatedUser:
        if not current_user.has_role(role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Role required: {role}"
            )
        return current_user

    return check_user_role


def require_any_role(roles: List[str]):
    """
    Dependency factory for requiring any of specified roles

    Args:
        roles: List of acceptable roles

    Returns:
        FastAPI dependency function
    """

    async def check_user_roles(
        current_user: AuthenticatedUser = Depends(get_current_active_user),
    ) -> AuthenticatedUser:
        if not current_user.has_any_role(roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of these roles required: {', '.join(roles)}",
            )
        return current_user

    return check_user_roles


def require_all_roles(roles: List[str]):
    """
    Dependency factory for requiring all specified roles

    Args:
        roles: List of required roles

    Returns:
        FastAPI dependency function
    """

    async def check_user_roles(
        current_user: AuthenticatedUser = Depends(get_current_active_user),
    ) -> AuthenticatedUser:
        if not current_user.has_all_roles(roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"All these roles required: {', '.join(roles)}",
            )
        return current_user

    return check_user_roles


def require_source_access(source_id: Optional[int] = None):
    """
    Dependency factory for requiring access to specific sources

    Args:
        source_id: Optional source ID for granular access control

    Returns:
        FastAPI dependency function
    """

    async def check_source_access(
        current_user: AuthenticatedUser = Depends(get_current_active_user),
    ) -> AuthenticatedUser:
        # Check if user has general source read permission
        if current_user.has_permission("sources:read") or current_user.has_permission(
            "*"
        ):
            return current_user

        # For specific source access, could implement more granular checks here
        # This would require additional database schema for source-specific permissions

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Source access required"
        )

    return check_source_access


class PermissionChecker:
    """Helper class for complex permission checking logic"""

    def __init__(self, user: AuthenticatedUser):
        self.user = user

    def can_create_sources(self) -> bool:
        """Check if user can create news sources"""
        return self.user.has_permission("sources:create")

    def can_modify_source(self, source_id: int) -> bool:
        """Check if user can modify a specific source"""
        return (
            self.user.has_permission("sources:update")
            or self.user.has_permission("sources:*")
            or self.user.has_permission("*")
        )

    def can_delete_sources(self) -> bool:
        """Check if user can delete sources"""
        return self.user.has_permission("sources:delete")

    def can_validate_compliance(self) -> bool:
        """Check if user can perform compliance validation"""
        return (
            self.user.has_permission("compliance:validate")
            or self.user.has_permission("compliance:*")
            or self.user.has_permission("*")
        )

    def can_review_audit_logs(self) -> bool:
        """Check if user can review audit logs"""
        return self.user.has_permission("audit:read")

    def can_manage_users(self) -> bool:
        """Check if user can manage other users"""
        return (
            self.user.has_permission("users:*")
            or self.user.has_permission("*")
            or self.user.is_superuser
        )


def get_permission_checker(
    current_user: AuthenticatedUser = Depends(get_current_active_user),
) -> PermissionChecker:
    """Get permission checker for complex authorization logic"""
    return PermissionChecker(current_user)
