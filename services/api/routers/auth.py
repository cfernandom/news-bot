"""
Authentication router for FastAPI
Implements login, user management, and role administration endpoints
"""

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from services.api.auth.dependencies import (
    AuthenticatedUser,
    get_current_active_user,
    get_current_user,
    get_superuser,
    require_permission,
    require_role,
)
from services.api.auth.jwt_handler import create_access_token, decode_token
from services.api.auth.models import (
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
    RoleCreateRequest,
    RoleResponse,
    TokenValidationResponse,
    UserCreateRequest,
    UserResponse,
    UserRoleAssignmentRequest,
    UserUpdateRequest,
)
from services.api.auth.password_utils import hash_password, verify_password
from services.api.auth.role_manager import get_user_permissions, role_manager
from services.data.database.connection import db_manager
from services.data.database.models import User, UserRole, UserRoleAssignment

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """
    Authenticate user and return JWT token

    - **username**: Username or email address
    - **password**: User password
    - **remember_me**: Extend token expiration for persistent login
    """

    async with db_manager.get_session() as session:
        # Find user by username or email
        query = select(User).where(
            (User.username == login_data.username) | (User.email == login_data.username)
        )
        result = await session.execute(query)
        user = result.scalar()

        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Account is inactive"
            )

        # Check for account lockout
        if user.account_locked_until and user.account_locked_until > datetime.now(
            timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is temporarily locked",
            )

        # Get user roles and permissions
        roles = await role_manager.get_user_roles(user.id)
        permissions = await role_manager.get_user_permissions(user.id)

        # Create JWT token
        token_expiry = (
            24 * 60 if login_data.remember_me else 30
        )  # 24 hours or 30 minutes
        token_data = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "roles": [role.name for role in roles],
            "permissions": list(permissions),
        }

        access_token = create_access_token(
            token_data, expires_delta=timedelta(minutes=token_expiry)
        )

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        user.failed_login_attempts = 0  # Reset failed attempts
        await session.commit()

        # Prepare response
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            roles=[role.name for role in roles],
            permissions=list(permissions),
            last_login=user.last_login,
            created_at=user.created_at,
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=token_expiry * 60,  # Convert to seconds
            user=user_response,
        )


@router.post("/validate-token", response_model=TokenValidationResponse)
async def validate_token(current_user: AuthenticatedUser = Depends(get_current_user)):
    """
    Validate current JWT token and return user information
    """
    return TokenValidationResponse(
        valid=True,
        user_id=current_user.id,
        username=current_user.username,
        expires_at=current_user.token_data.exp,
    )


@router.post("/refresh-token", response_model=LoginResponse)
async def refresh_token(current_user: AuthenticatedUser = Depends(get_current_user)):
    """
    Refresh JWT token with new expiration
    """
    # Create new token with same data
    token_data = {
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "roles": current_user.roles,
        "permissions": current_user.permissions,
    }

    new_token = create_access_token(token_data)

    user_response = UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        roles=current_user.roles,
        permissions=current_user.permissions,
        last_login=datetime.now(timezone.utc),
        created_at=datetime.now(
            timezone.utc
        ),  # Would need to fetch from DB for real value
    )

    return LoginResponse(
        access_token=new_token,
        token_type="bearer",
        expires_in=1800,  # 30 minutes
        user=user_response,
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: AuthenticatedUser = Depends(get_current_active_user),
):
    """
    Get current user information
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        roles=current_user.roles,
        permissions=current_user.permissions,
        last_login=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
    )


@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: AuthenticatedUser = Depends(get_current_active_user),
):
    """
    Change current user's password
    """

    async with db_manager.get_session() as session:
        # Get user from database
        query = select(User).where(User.id == current_user.id)
        result = await session.execute(query)
        user = result.scalar()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Verify current password
        if not verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        # Update password
        user.password_hash = hash_password(password_data.new_password)
        user.password_changed_at = datetime.now(timezone.utc)
        await session.commit()

        return {"message": "Password changed successfully"}


# User Management Endpoints (Admin only)


@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreateRequest,
    current_user: AuthenticatedUser = Depends(require_permission("users:create")),
):
    """
    Create a new user (requires users:create permission)
    """

    async with db_manager.get_session() as session:
        # Check if username or email already exists
        existing_query = select(User).where(
            (User.username == user_data.username) | (User.email == user_data.email)
        )
        existing = await session.execute(existing_query)
        if existing.scalar():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists",
            )

        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=hash_password(user_data.password),
            is_active=user_data.is_active,
            password_changed_at=datetime.now(timezone.utc),
        )

        session.add(user)
        await session.flush()  # Get user ID

        # Assign roles
        for role_name in user_data.roles:
            role_query = select(UserRole).where(UserRole.name == role_name)
            role_result = await session.execute(role_query)
            role = role_result.scalar()

            if role:
                assignment = UserRoleAssignment(
                    user_id=user.id, role_id=role.id, assigned_by=current_user.id
                )
                session.add(assignment)

        await session.commit()
        await session.refresh(user)

        # Get user permissions
        permissions = await role_manager.get_user_permissions(user.id)

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            roles=user_data.roles,
            permissions=list(permissions),
            last_login=user.last_login,
            created_at=user.created_at,
        )


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: AuthenticatedUser = Depends(require_permission("users:read")),
):
    """
    List all users (requires users:read permission)
    """

    async with db_manager.get_session() as session:
        query = select(User).offset(skip).limit(limit)
        result = await session.execute(query)
        users = result.scalars().all()

        user_responses = []
        for user in users:
            roles = await role_manager.get_user_roles(user.id)
            permissions = await role_manager.get_user_permissions(user.id)

            user_responses.append(
                UserResponse(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    full_name=user.full_name,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                    roles=[role.name for role in roles],
                    permissions=list(permissions),
                    last_login=user.last_login,
                    created_at=user.created_at,
                )
            )

        return user_responses


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: AuthenticatedUser = Depends(require_permission("users:read")),
):
    """
    Get specific user by ID (requires users:read permission)
    """

    async with db_manager.get_session() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        roles = await role_manager.get_user_roles(user.id)
        permissions = await role_manager.get_user_permissions(user.id)

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            roles=[role.name for role in roles],
            permissions=list(permissions),
            last_login=user.last_login,
            created_at=user.created_at,
        )


# Role Management Endpoints


@router.get("/roles", response_model=List[RoleResponse])
async def list_roles(
    current_user: AuthenticatedUser = Depends(require_permission("roles:read")),
):
    """
    List all available roles (requires roles:read permission)
    """

    async with db_manager.get_session() as session:
        query = select(UserRole)
        result = await session.execute(query)
        roles = result.scalars().all()

        return [
            RoleResponse(
                id=role.id,
                name=role.name,
                description=role.description,
                permissions=role.permissions,
                is_system_role=role.is_system_role,
                created_at=role.created_at,
            )
            for role in roles
        ]


@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreateRequest,
    current_user: AuthenticatedUser = Depends(require_permission("roles:create")),
):
    """
    Create a new role (requires roles:create permission)
    """

    async with db_manager.get_session() as session:
        # Check if role name already exists
        existing_query = select(UserRole).where(UserRole.name == role_data.name)
        existing = await session.execute(existing_query)
        if existing.scalar():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists",
            )

        # Create role
        role = UserRole(
            name=role_data.name,
            description=role_data.description,
            permissions=role_data.permissions,
            is_system_role=False,
        )

        session.add(role)
        await session.commit()
        await session.refresh(role)

        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=role.permissions,
            is_system_role=role.is_system_role,
            created_at=role.created_at,
        )


@router.post("/users/{user_id}/roles")
async def assign_role_to_user(
    user_id: int,
    assignment_data: UserRoleAssignmentRequest,
    current_user: AuthenticatedUser = Depends(require_permission("users:update")),
):
    """
    Assign role to user (requires users:update permission)
    """
    if assignment_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID in path must match user ID in request body",
        )

    success = await role_manager.assign_role(
        user_id=assignment_data.user_id,
        role_id=assignment_data.role_id,
        assigned_by=current_user.id,
        expires_at=assignment_data.expires_at,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to assign role (role may already be assigned)",
        )

    return {"message": "Role assigned successfully"}


@router.delete("/users/{user_id}/roles/{role_id}")
async def revoke_role_from_user(
    user_id: int,
    role_id: int,
    current_user: AuthenticatedUser = Depends(require_permission("users:update")),
):
    """
    Revoke role from user (requires users:update permission)
    """
    success = await role_manager.revoke_role(user_id, role_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role assignment not found"
        )

    return {"message": "Role revoked successfully"}
