# Authentication framework for PreventIA News Analytics
# Implements JWT-based authentication with role-based access control

from .dependencies import get_current_user, require_permission, require_role
from .jwt_handler import create_access_token, decode_token, verify_token
from .password_utils import hash_password, verify_password
from .role_manager import RoleManager, check_permission

__all__ = [
    "create_access_token",
    "verify_token",
    "decode_token",
    "hash_password",
    "verify_password",
    "RoleManager",
    "check_permission",
    "get_current_user",
    "require_permission",
    "require_role",
]
