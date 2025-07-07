"""
Pydantic models for authentication API endpoints
Includes request/response models for login, registration, and user management
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from services.api.auth.password_utils import check_password_strength


class LoginRequest(BaseModel):
    """Login request model"""

    username: str = Field(
        ..., min_length=3, max_length=100, description="Username or email address"
    )
    password: str = Field(..., min_length=1, description="User password")
    remember_me: bool = Field(
        default=False, description="Extend token expiration for persistent login"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin@preventia.com",
                "password": "secure_password",
                "remember_me": False,
            }
        }


class LoginResponse(BaseModel):
    """Login response model"""

    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(description="Token expiration time in seconds")
    user: "UserResponse" = Field(description="User information")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "jwt_token_here",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@preventia.com",
                    "full_name": "System Administrator",
                    "is_active": True,
                    "roles": ["system_admin"],
                },
            }
        }


class UserCreateRequest(BaseModel):
    """User creation request model"""

    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Unique username (alphanumeric, underscore, hyphen only)",
    )
    email: EmailStr = Field(..., description="Valid email address")
    full_name: str = Field(
        ..., min_length=2, max_length=255, description="User's full name"
    )
    password: str = Field(
        ..., min_length=8, description="Strong password (minimum 8 characters)"
    )
    roles: List[str] = Field(
        default_factory=list, description="List of role names to assign to user"
    )
    is_active: bool = Field(default=True, description="Account active status")

    @validator("password")
    def validate_password_strength(cls, v):
        """Validate password meets strength requirements"""
        strength = check_password_strength(v)
        if strength["strength"] == "weak":
            raise ValueError(
                "Password is too weak. Must include: "
                "8+ characters, uppercase, lowercase, number, special character"
            )
        return v

    @validator("username")
    def validate_username_format(cls, v):
        """Validate username format"""
        if v.lower() in ["admin", "root", "system", "api", "test"]:
            raise ValueError("Username not allowed")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@preventia.com",
                "full_name": "John Doe",
                "password": "SecureP@ssw0rd!",
                "roles": ["source_editor"],
                "is_active": True,
            }
        }


class UserUpdateRequest(BaseModel):
    """User update request model"""

    username: Optional[str] = Field(
        None, min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$"
    )
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John D. Doe",
                "email": "john.doe.new@preventia.com",
                "is_active": True,
                "roles": ["source_admin", "compliance_officer"],
            }
        }


class PasswordChangeRequest(BaseModel):
    """Password change request model"""

    current_password: str = Field(..., description="Current password for verification")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        """Validate passwords match"""
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("new_password")
    def validate_new_password_strength(cls, v):
        """Validate new password strength"""
        strength = check_password_strength(v)
        if strength["strength"] == "weak":
            raise ValueError(
                "Password is too weak. Must include: "
                "8+ characters, uppercase, lowercase, number, special character"
            )
        return v


class PasswordResetRequest(BaseModel):
    """Password reset request model"""

    email: EmailStr = Field(..., description="Email address for password reset")

    class Config:
        json_schema_extra = {"example": {"email": "user@preventia.com"}}


class RoleResponse(BaseModel):
    """Role response model"""

    id: int = Field(description="Role ID")
    name: str = Field(description="Role name")
    description: str = Field(description="Role description")
    permissions: List[str] = Field(description="List of permissions")
    is_system_role: bool = Field(description="Whether this is a system role")
    created_at: datetime = Field(description="Creation timestamp")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "source_admin",
                "description": "Source Administration Manager",
                "permissions": [
                    "sources:create",
                    "sources:read",
                    "sources:update",
                    "sources:delete",
                    "compliance:validate",
                ],
                "is_system_role": True,
                "created_at": "2025-07-07T12:00:00Z",
            }
        }


class UserResponse(BaseModel):
    """User response model"""

    id: int = Field(description="User ID")
    username: str = Field(description="Username")
    email: str = Field(description="Email address")
    full_name: str = Field(description="Full name")
    is_active: bool = Field(description="Account active status")
    is_superuser: bool = Field(description="Superuser status")
    roles: List[str] = Field(description="Assigned role names")
    permissions: List[str] = Field(description="Effective permissions")
    last_login: Optional[datetime] = Field(description="Last login timestamp")
    created_at: datetime = Field(description="Account creation timestamp")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "admin",
                "email": "admin@preventia.com",
                "full_name": "System Administrator",
                "is_active": True,
                "is_superuser": True,
                "roles": ["system_admin"],
                "permissions": ["*"],
                "last_login": "2025-07-07T11:30:00Z",
                "created_at": "2025-01-01T00:00:00Z",
            }
        }


class TokenValidationResponse(BaseModel):
    """Token validation response model"""

    valid: bool = Field(description="Whether token is valid")
    user_id: Optional[int] = Field(description="User ID if token is valid")
    username: Optional[str] = Field(description="Username if token is valid")
    expires_at: Optional[datetime] = Field(description="Token expiration time")

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "user_id": 1,
                "username": "admin",
                "expires_at": "2025-07-07T13:00:00Z",
            }
        }


class RefreshTokenRequest(BaseModel):
    """Token refresh request model"""

    refresh_token: str = Field(..., description="Current valid JWT token to refresh")


class RoleCreateRequest(BaseModel):
    """Role creation request model"""

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-z_]+$",
        description="Role name (lowercase, underscores only)",
    )
    description: str = Field(
        ..., min_length=10, max_length=500, description="Role description"
    )
    permissions: List[str] = Field(
        ..., min_items=1, description="List of permissions for this role"
    )

    @validator("permissions")
    def validate_permissions(cls, v):
        """Validate permission format"""
        from services.api.auth.role_manager import RoleManager

        rm = RoleManager(None)  # Just for validation

        for permission in v:
            if not rm.validate_permission_format(permission):
                raise ValueError(f"Invalid permission format: {permission}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "data_analyst",
                "description": "Data Analyst - Read access to analytics and reports",
                "permissions": ["analytics:read", "reports:read", "sources:read"],
            }
        }


class UserRoleAssignmentRequest(BaseModel):
    """User role assignment request model"""

    user_id: int = Field(..., description="User ID to assign role to")
    role_id: int = Field(..., description="Role ID to assign")
    expires_at: Optional[datetime] = Field(
        None, description="Optional expiration date for role assignment"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 5,
                "role_id": 2,
                "expires_at": "2025-12-31T23:59:59Z",
            }
        }
