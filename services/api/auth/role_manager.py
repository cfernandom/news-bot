"""
Role-based access control (RBAC) management
Implements permission checking and role management for the authentication system
"""

from datetime import datetime
from typing import Dict, List, Optional, Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import DatabaseManager
from services.data.database.models import User, UserRole, UserRoleAssignment


class RoleManager:
    """Manages roles and permissions for users"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

        # Permission hierarchy - higher level permissions include lower level ones
        self.permission_hierarchy = {
            "system_admin": ["*"],  # All permissions
            "source_admin": [
                "sources:create",
                "sources:read",
                "sources:update",
                "sources:delete",
                "sources:validate",
                "compliance:read",
                "compliance:validate",
                "audit:read",
                "users:read",
            ],
            "source_editor": [
                "sources:read",
                "sources:update",
                "sources:validate",
                "compliance:read",
            ],
            "source_viewer": ["sources:read", "compliance:read"],
            "compliance_officer": [
                "sources:read",
                "compliance:read",
                "compliance:validate",
                "compliance:review",
                "audit:read",
                "legal:manage",
            ],
        }

    async def get_user_roles(self, user_id: int) -> List[UserRole]:
        """
        Get all roles assigned to a user

        Args:
            user_id: User ID to get roles for

        Returns:
            List of UserRole objects
        """
        async with self.db_manager.get_session() as session:
            query = (
                select(UserRole)
                .join(UserRoleAssignment)
                .where(UserRoleAssignment.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def get_user_permissions(self, user_id: int) -> Set[str]:
        """
        Get all permissions for a user based on their roles

        Args:
            user_id: User ID to get permissions for

        Returns:
            Set of permission strings
        """
        roles = await self.get_user_roles(user_id)
        permissions = set()

        for role in roles:
            # Parse permissions from JSON field
            role_permissions = (
                role.permissions if isinstance(role.permissions, list) else []
            )

            # Add direct permissions
            permissions.update(role_permissions)

            # Check for wildcard permission (system admin)
            if "*" in role_permissions:
                permissions.add("*")
                break

        return permissions

    async def has_permission(self, user_id: int, required_permission: str) -> bool:
        """
        Check if user has a specific permission

        Args:
            user_id: User ID to check
            required_permission: Permission string to check for

        Returns:
            True if user has permission, False otherwise
        """
        user_permissions = await self.get_user_permissions(user_id)

        # Check for wildcard permission (system admin)
        if "*" in user_permissions:
            return True

        # Check for exact permission match
        if required_permission in user_permissions:
            return True

        # Check for resource-level permissions (e.g., sources:* covers sources:read)
        resource = (
            required_permission.split(":")[0] if ":" in required_permission else ""
        )
        if resource and f"{resource}:*" in user_permissions:
            return True

        return False

    async def has_role(self, user_id: int, required_role: str) -> bool:
        """
        Check if user has a specific role

        Args:
            user_id: User ID to check
            required_role: Role name to check for

        Returns:
            True if user has role, False otherwise
        """
        roles = await self.get_user_roles(user_id)
        role_names = [role.name for role in roles]
        return required_role in role_names

    async def assign_role(
        self,
        user_id: int,
        role_id: int,
        assigned_by: int,
        expires_at: Optional[datetime] = None,
    ) -> bool:
        """
        Assign a role to a user

        Args:
            user_id: User ID to assign role to
            role_id: Role ID to assign
            assigned_by: User ID of who is assigning the role
            expires_at: Optional expiration date for the role assignment

        Returns:
            True if role was assigned successfully
        """
        try:
            async with self.db_manager.get_session() as session:
                # Check if assignment already exists
                existing_query = select(UserRoleAssignment).where(
                    UserRoleAssignment.user_id == user_id,
                    UserRoleAssignment.role_id == role_id,
                )
                existing = await session.execute(existing_query)

                if existing.scalar():
                    return False  # Already assigned

                # Create new assignment
                assignment = UserRoleAssignment(
                    user_id=user_id,
                    role_id=role_id,
                    assigned_by=assigned_by,
                    expires_at=expires_at,
                )

                session.add(assignment)
                await session.commit()
                return True

        except Exception:
            return False

    async def revoke_role(self, user_id: int, role_id: int) -> bool:
        """
        Revoke a role from a user

        Args:
            user_id: User ID to revoke role from
            role_id: Role ID to revoke

        Returns:
            True if role was revoked successfully
        """
        try:
            async with self.db_manager.get_session() as session:
                query = select(UserRoleAssignment).where(
                    UserRoleAssignment.user_id == user_id,
                    UserRoleAssignment.role_id == role_id,
                )
                result = await session.execute(query)
                assignment = result.scalar()

                if assignment:
                    await session.delete(assignment)
                    await session.commit()
                    return True

                return False

        except Exception:
            return False

    async def create_role(
        self, name: str, description: str, permissions: List[str]
    ) -> Optional[UserRole]:
        """
        Create a new role

        Args:
            name: Role name (must be unique)
            description: Role description
            permissions: List of permissions for the role

        Returns:
            Created UserRole object or None if creation failed
        """
        try:
            async with self.db_manager.get_session() as session:
                role = UserRole(
                    name=name,
                    description=description,
                    permissions=permissions,
                    is_system_role=False,
                )

                session.add(role)
                await session.commit()
                await session.refresh(role)
                return role

        except Exception:
            return None

    async def get_role_by_name(self, role_name: str) -> Optional[UserRole]:
        """
        Get role by name

        Args:
            role_name: Name of role to find

        Returns:
            UserRole object or None if not found
        """
        async with self.db_manager.get_session() as session:
            query = select(UserRole).where(UserRole.name == role_name)
            result = await session.execute(query)
            return result.scalar()

    def validate_permission_format(self, permission: str) -> bool:
        """
        Validate permission string format

        Args:
            permission: Permission string to validate

        Returns:
            True if format is valid
        """
        # Permission format: resource:action (e.g., sources:read, compliance:validate)
        # Special case: * for wildcard
        if permission == "*":
            return True

        if ":" not in permission:
            return False

        resource, action = permission.split(":", 1)

        # Validate resource and action format
        valid_chars = set("abcdefghijklmnopqrstuvwxyz_")

        if not resource or not action:
            return False

        if not all(c in valid_chars for c in resource.lower()):
            return False

        if not all(c in valid_chars or c == "*" for c in action.lower()):
            return False

        return True


# Global role manager instance (will be initialized with database manager)
role_manager: Optional[RoleManager] = None


def initialize_role_manager(db_manager: DatabaseManager):
    """Initialize the global role manager with database connection"""
    global role_manager
    role_manager = RoleManager(db_manager)


async def check_permission(user_id: int, permission: str) -> bool:
    """Check if user has permission - convenience function"""
    if not role_manager:
        raise RuntimeError("Role manager not initialized")
    return await role_manager.has_permission(user_id, permission)


async def check_role(user_id: int, role: str) -> bool:
    """Check if user has role - convenience function"""
    if not role_manager:
        raise RuntimeError("Role manager not initialized")
    return await role_manager.has_role(user_id, role)


async def get_user_permissions(user_id: int) -> Set[str]:
    """Get user permissions - convenience function"""
    if not role_manager:
        raise RuntimeError("Role manager not initialized")
    return await role_manager.get_user_permissions(user_id)
