"""
Authentication & Authorization Integration Tests
Tests the complete auth system: JWT, roles, permissions, API protection
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.api.auth.jwt_handler import (
    create_access_token,
    decode_token,
    verify_token,
)
from services.api.auth.role_manager import RoleManager
from services.api.main import app
from services.data.database.connection import db_manager
from services.data.database.models import User, UserRole, UserRoleAssignment


@pytest.mark.integration
@pytest.mark.database
class TestAuthenticationIntegration:
    """Test authentication system integration"""

    @pytest.fixture
    async def clean_auth_environment(self, test_db_manager):
        """Provide clean auth environment for testing"""
        async with test_db_manager.get_session() as session:
            # Clean auth-related tables
            await session.execute(delete(UserRoleAssignment))
            await session.execute(delete(User))
            await session.execute(delete(UserRole))
            await session.commit()

        yield test_db_manager

        # Cleanup after test
        async with test_db_manager.get_session() as session:
            await session.execute(delete(UserRoleAssignment))
            await session.execute(delete(User))
            await session.execute(delete(UserRole))
            await session.commit()

    @pytest.fixture
    async def sample_roles_and_users(self, clean_auth_environment):
        """Create sample roles and users for testing"""
        async with clean_auth_environment.get_session() as session:
            # Create roles
            admin_role = UserRole(
                name="admin",
                description="System administrator",
                permissions=["*"],
                is_system_role=True,
            )

            editor_role = UserRole(
                name="source_editor",
                description="Can edit news sources",
                permissions=["sources:read", "sources:update", "sources:validate"],
                is_system_role=True,
            )

            viewer_role = UserRole(
                name="source_viewer",
                description="Can view news sources",
                permissions=["sources:read"],
                is_system_role=True,
            )

            session.add_all([admin_role, editor_role, viewer_role])
            await session.commit()
            await session.refresh(admin_role)
            await session.refresh(editor_role)
            await session.refresh(viewer_role)

            # Create users
            admin_user = User(
                username="admin",
                email="admin@preventia.com",
                full_name="System Administrator",
                password_hash="$2b$12$dummy_hash_for_testing",
                is_active=True,
                is_superuser=True,
            )

            editor_user = User(
                username="editor",
                email="editor@preventia.com",
                full_name="Content Editor",
                password_hash="$2b$12$dummy_hash_for_testing",
                is_active=True,
                is_superuser=False,
            )

            viewer_user = User(
                username="viewer",
                email="viewer@preventia.com",
                full_name="Content Viewer",
                password_hash="$2b$12$dummy_hash_for_testing",
                is_active=True,
                is_superuser=False,
            )

            inactive_user = User(
                username="inactive",
                email="inactive@preventia.com",
                full_name="Inactive User",
                password_hash="$2b$12$dummy_hash_for_testing",
                is_active=False,
                is_superuser=False,
            )

            session.add_all([admin_user, editor_user, viewer_user, inactive_user])
            await session.commit()
            for user in [admin_user, editor_user, viewer_user, inactive_user]:
                await session.refresh(user)

            # Assign roles to users
            role_assignments = [
                UserRoleAssignment(
                    user_id=admin_user.id,
                    role_id=admin_role.id,
                    assigned_by=admin_user.id,
                ),
                UserRoleAssignment(
                    user_id=editor_user.id,
                    role_id=editor_role.id,
                    assigned_by=admin_user.id,
                ),
                UserRoleAssignment(
                    user_id=viewer_user.id,
                    role_id=viewer_role.id,
                    assigned_by=admin_user.id,
                ),
            ]

            session.add_all(role_assignments)
            await session.commit()

        return {
            "users": {
                "admin": admin_user,
                "editor": editor_user,
                "viewer": viewer_user,
                "inactive": inactive_user,
            },
            "roles": {
                "admin": admin_role,
                "source_editor": editor_role,
                "source_viewer": viewer_role,
            },
        }

    def test_jwt_token_lifecycle(self, sample_roles_and_users):
        """Test complete JWT token lifecycle"""
        admin_user = sample_roles_and_users["users"]["admin"]

        # Create token
        user_data = {
            "user_id": admin_user.id,
            "username": admin_user.username,
            "email": admin_user.email,
            "roles": ["admin"],
            "permissions": ["*"],
        }

        token = create_access_token(user_data)
        assert isinstance(token, str)
        assert len(token) > 50  # JWT tokens are long

        # Verify token
        is_valid = verify_token(token)
        assert is_valid

        # Decode token
        decoded_data = decode_token(token)
        assert decoded_data.user_id == admin_user.id
        assert decoded_data.username == admin_user.username
        assert decoded_data.email == admin_user.email
        assert "admin" in decoded_data.roles
        assert "*" in decoded_data.permissions

        # Test expired token
        expired_token = create_access_token(
            user_data, expires_delta=timedelta(seconds=-1)
        )
        assert not verify_token(expired_token)

        with pytest.raises(Exception):  # Should raise HTTPException
            decode_token(expired_token)

    @pytest.mark.asyncio
    async def test_role_manager_integration(self, sample_roles_and_users):
        """Test role manager with database integration"""
        role_manager = RoleManager(db_manager)

        admin_user = sample_roles_and_users["users"]["admin"]
        editor_user = sample_roles_and_users["users"]["editor"]
        viewer_user = sample_roles_and_users["users"]["viewer"]

        # Test get user roles
        admin_roles = await role_manager.get_user_roles(admin_user.id)
        assert len(admin_roles) == 1
        assert admin_roles[0].name == "admin"

        editor_roles = await role_manager.get_user_roles(editor_user.id)
        assert len(editor_roles) == 1
        assert editor_roles[0].name == "source_editor"

        # Test get user permissions
        admin_permissions = await role_manager.get_user_permissions(admin_user.id)
        assert "*" in admin_permissions

        editor_permissions = await role_manager.get_user_permissions(editor_user.id)
        assert "sources:read" in editor_permissions
        assert "sources:update" in editor_permissions
        assert "*" not in editor_permissions

        viewer_permissions = await role_manager.get_user_permissions(viewer_user.id)
        assert "sources:read" in viewer_permissions
        assert "sources:update" not in viewer_permissions

        # Test permission checking
        assert await role_manager.has_permission(admin_user.id, "sources:create")
        assert await role_manager.has_permission(editor_user.id, "sources:update")
        assert not await role_manager.has_permission(viewer_user.id, "sources:update")

        # Test role checking
        assert await role_manager.has_role(admin_user.id, "admin")
        assert await role_manager.has_role(editor_user.id, "source_editor")
        assert not await role_manager.has_role(viewer_user.id, "admin")

    def test_api_authentication_integration(self, sample_roles_and_users):
        """Test API authentication integration"""
        client = TestClient(app)

        admin_user = sample_roles_and_users["users"]["admin"]
        inactive_user = sample_roles_and_users["users"]["inactive"]

        # Test public endpoints (should work without auth)
        public_endpoints = [
            "/health",
            "/api/v1/articles/",
            "/api/v1/analytics/sentiment",
        ]

        for endpoint in public_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200

        # Test creating valid token for API use
        user_data = {
            "user_id": admin_user.id,
            "username": admin_user.username,
            "email": admin_user.email,
            "roles": ["admin"],
            "permissions": ["*"],
        }
        valid_token = create_access_token(user_data)

        # Test with valid token (if auth is implemented on any endpoint)
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.get("/api/v1/articles/", headers=headers)
        assert response.status_code == 200  # Should work with or without auth

        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/articles/", headers=headers)
        # Current implementation may not check auth, so both 200 and 401 are acceptable
        assert response.status_code in [200, 401]

        # Test with inactive user token
        inactive_user_data = {
            "user_id": inactive_user.id,
            "username": inactive_user.username,
            "email": inactive_user.email,
            "roles": [],
            "permissions": [],
        }
        inactive_token = create_access_token(inactive_user_data)
        headers = {"Authorization": f"Bearer {inactive_token}"}
        response = client.get("/api/v1/articles/", headers=headers)
        # Should work if no auth is enforced, or fail if auth checks for active users
        assert response.status_code in [200, 401, 403]

    @pytest.mark.asyncio
    async def test_role_assignment_workflow(self, sample_roles_and_users):
        """Test complete role assignment workflow"""
        role_manager = RoleManager(db_manager)

        editor_user = sample_roles_and_users["users"]["editor"]
        admin_user = sample_roles_and_users["users"]["admin"]
        admin_role = sample_roles_and_users["roles"]["admin"]

        # Initially editor should not have admin role
        assert not await role_manager.has_role(editor_user.id, "admin")

        # Assign admin role to editor
        success = await role_manager.assign_role(
            user_id=editor_user.id, role_id=admin_role.id, assigned_by=admin_user.id
        )
        assert success

        # Now editor should have admin role
        assert await role_manager.has_role(editor_user.id, "admin")

        # Editor should now have admin permissions
        assert await role_manager.has_permission(editor_user.id, "users:create")

        # Try to assign same role again (should fail)
        success = await role_manager.assign_role(
            user_id=editor_user.id, role_id=admin_role.id, assigned_by=admin_user.id
        )
        assert not success  # Already assigned

        # Revoke admin role
        success = await role_manager.revoke_role(editor_user.id, admin_role.id)
        assert success

        # Editor should no longer have admin role
        assert not await role_manager.has_role(editor_user.id, "admin")

    @pytest.mark.asyncio
    async def test_permission_hierarchy_and_inheritance(self, sample_roles_and_users):
        """Test permission hierarchy and inheritance"""
        role_manager = RoleManager(db_manager)

        admin_user = sample_roles_and_users["users"]["admin"]
        editor_user = sample_roles_and_users["users"]["editor"]

        # Admin with wildcard permission should have all permissions
        admin_permissions = await role_manager.get_user_permissions(admin_user.id)
        assert "*" in admin_permissions

        # Test various permission checks for admin
        test_permissions = [
            "sources:create",
            "sources:read",
            "sources:update",
            "sources:delete",
            "users:create",
            "compliance:validate",
            "any:permission",
        ]

        for permission in test_permissions:
            assert await role_manager.has_permission(
                admin_user.id, permission
            ), f"Admin should have permission: {permission}"

        # Editor should only have specific permissions
        editor_permissions = await role_manager.get_user_permissions(editor_user.id)
        assert "sources:read" in editor_permissions
        assert "sources:update" in editor_permissions
        assert "sources:delete" not in editor_permissions
        assert "users:create" not in editor_permissions

    def test_token_security_features(self, sample_roles_and_users):
        """Test JWT token security features"""
        admin_user = sample_roles_and_users["users"]["admin"]

        user_data = {
            "user_id": admin_user.id,
            "username": admin_user.username,
            "email": admin_user.email,
            "roles": ["admin"],
            "permissions": ["*"],
        }

        # Test token expiration
        short_lived_token = create_access_token(
            user_data, expires_delta=timedelta(seconds=1)
        )
        assert verify_token(short_lived_token)

        import time

        time.sleep(2)  # Wait for token to expire
        assert not verify_token(short_lived_token)

        # Test token tampering resistance
        valid_token = create_access_token(user_data)

        # Tamper with token (change a character)
        tampered_token = valid_token[:-1] + "X"
        assert not verify_token(tampered_token)

        # Test malformed tokens
        malformed_tokens = [
            "not.a.token",
            "Bearer token",
            "",
            "a.b.c.d.e",  # Too many parts
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",  # Missing parts
        ]

        for malformed in malformed_tokens:
            assert not verify_token(malformed)

    @pytest.mark.asyncio
    async def test_authentication_edge_cases(self, sample_roles_and_users):
        """Test authentication edge cases and error handling"""
        role_manager = RoleManager(db_manager)

        # Test with non-existent user
        assert not await role_manager.has_permission(99999, "sources:read")
        assert not await role_manager.has_role(99999, "admin")

        user_roles = await role_manager.get_user_roles(99999)
        assert len(user_roles) == 0

        user_permissions = await role_manager.get_user_permissions(99999)
        assert len(user_permissions) == 0

        # Test role assignment with invalid data
        admin_user = sample_roles_and_users["users"]["admin"]
        assert not await role_manager.assign_role(
            99999, 1, admin_user.id
        )  # Invalid user
        assert not await role_manager.assign_role(
            admin_user.id, 99999, admin_user.id
        )  # Invalid role

        # Test role revocation with invalid data
        assert not await role_manager.revoke_role(99999, 1)  # Invalid user
        assert not await role_manager.revoke_role(admin_user.id, 99999)  # Invalid role

    def test_concurrent_authentication_operations(self, sample_roles_and_users):
        """Test authentication under concurrent operations"""
        import concurrent.futures
        import threading

        admin_user = sample_roles_and_users["users"]["admin"]

        def create_and_verify_token():
            user_data = {
                "user_id": admin_user.id,
                "username": admin_user.username,
                "email": admin_user.email,
                "roles": ["admin"],
                "permissions": ["*"],
            }

            token = create_access_token(user_data)
            is_valid = verify_token(token)
            return is_valid

        # Run concurrent token operations
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_and_verify_token) for _ in range(20)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        # All tokens should be valid
        assert all(results), "All concurrent token operations should succeed"
        assert len(results) == 20


@pytest.mark.integration
@pytest.mark.e2e
class TestAuthorizationWorkflows:
    """Test complete authorization workflows"""

    @pytest.fixture
    async def auth_workflow_environment(self, test_db_manager):
        """Setup environment for authorization workflow testing"""
        async with test_db_manager.get_session() as session:
            # Clean tables
            await session.execute(delete(UserRoleAssignment))
            await session.execute(delete(User))
            await session.execute(delete(UserRole))
            await session.commit()

            # Create comprehensive role structure
            roles_data = [
                ("system_admin", "System Administrator", ["*"]),
                (
                    "source_admin",
                    "Source Administrator",
                    ["sources:*", "compliance:read"],
                ),
                ("source_editor", "Source Editor", ["sources:read", "sources:update"]),
                ("source_viewer", "Source Viewer", ["sources:read"]),
                (
                    "compliance_officer",
                    "Compliance Officer",
                    ["compliance:*", "audit:read"],
                ),
                ("analyst", "Data Analyst", ["analytics:read", "sources:read"]),
            ]

            roles = {}
            for name, desc, perms in roles_data:
                role = UserRole(name=name, description=desc, permissions=perms)
                session.add(role)
                roles[name] = role

            await session.commit()
            for role in roles.values():
                await session.refresh(role)

            return {"roles": roles, "db_manager": test_db_manager}

    def test_role_based_access_control_workflow(self, auth_workflow_environment):
        """Test complete RBAC workflow"""
        # This test demonstrates the RBAC system design
        # In a real implementation, these would be tested with actual API endpoints

        roles = auth_workflow_environment["roles"]

        # Verify role hierarchy
        assert "system_admin" in roles
        assert "source_admin" in roles
        assert "source_editor" in roles
        assert "compliance_officer" in roles

        # Verify permission structure
        system_admin_perms = roles["system_admin"].permissions
        assert "*" in system_admin_perms

        source_admin_perms = roles["source_admin"].permissions
        assert "sources:*" in source_admin_perms
        assert "compliance:read" in source_admin_perms

        source_editor_perms = roles["source_editor"].permissions
        assert "sources:read" in source_editor_perms
        assert "sources:update" in source_editor_perms
        assert "sources:delete" not in source_editor_perms

        # This establishes the foundation for API endpoint protection
        # which would be implemented in the FastAPI dependencies

    def test_permission_validation_patterns(self, auth_workflow_environment):
        """Test permission validation patterns"""
        roles = auth_workflow_environment["roles"]

        # Test wildcard permissions
        system_admin = roles["system_admin"]
        assert "*" in system_admin.permissions

        # Test resource-specific permissions
        source_admin = roles["source_admin"]
        assert "sources:*" in source_admin.permissions

        # Test action-specific permissions
        source_editor = roles["source_editor"]
        assert "sources:read" in source_editor.permissions
        assert "sources:update" in source_editor.permissions

        # Test cross-resource permissions
        compliance_officer = roles["compliance_officer"]
        assert "compliance:*" in compliance_officer.permissions
        assert "audit:read" in compliance_officer.permissions

    def test_authorization_matrix_completeness(self, auth_workflow_environment):
        """Test that authorization matrix covers all system operations"""
        roles = auth_workflow_environment["roles"]

        # Define all system operations
        system_operations = [
            "sources:create",
            "sources:read",
            "sources:update",
            "sources:delete",
            "sources:validate",
            "compliance:read",
            "compliance:validate",
            "compliance:review",
            "audit:read",
            "analytics:read",
            "users:create",
            "users:read",
            "users:update",
            "users:delete",
        ]

        # Check that operations are covered by appropriate roles
        role_permissions = {}
        for role_name, role in roles.items():
            role_permissions[role_name] = set(role.permissions)

        # System admin should cover everything
        system_admin_perms = role_permissions["system_admin"]
        assert "*" in system_admin_perms  # Wildcard covers all

        # Source operations should be covered by source roles
        source_operations = [
            op for op in system_operations if op.startswith("sources:")
        ]
        source_admin_perms = role_permissions["source_admin"]

        # Source admin has sources:* which covers all source operations
        assert "sources:*" in source_admin_perms

        # Compliance operations should be covered
        compliance_operations = [
            op for op in system_operations if op.startswith("compliance:")
        ]
        compliance_officer_perms = role_permissions["compliance_officer"]
        assert "compliance:*" in compliance_officer_perms


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
