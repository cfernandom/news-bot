"""
Authentication system startup and initialization
Creates default admin user and initializes role manager
"""

import asyncio
from datetime import datetime

from sqlalchemy import select

from services.api.auth.password_utils import hash_password
from services.api.auth.role_manager import initialize_role_manager
from services.data.database.connection import db_manager
from services.data.database.models import User, UserRole, UserRoleAssignment


async def create_default_admin():
    """Create default admin user if no users exist"""

    async with db_manager.get_session() as session:
        # Check if any users exist
        user_count_query = select(User)
        result = await session.execute(user_count_query)
        existing_users = result.scalars().all()

        if len(existing_users) > 0:
            print(
                f"Found {len(existing_users)} existing users. Skipping admin creation."
            )
            return

        # Get system_admin role
        admin_role_query = select(UserRole).where(UserRole.name == "system_admin")
        admin_role_result = await session.execute(admin_role_query)
        admin_role = admin_role_result.scalar()

        if not admin_role:
            print("ERROR: system_admin role not found. Run database migration first.")
            return

        # Create default admin user
        admin_user = User(
            username="admin",
            email="admin@preventia.com",
            full_name="System Administrator",
            password_hash=hash_password("PreventIA@2025!"),  # Strong default password
            is_active=True,
            is_superuser=True,
            password_changed_at=datetime.utcnow(),
        )

        session.add(admin_user)
        await session.flush()  # Get user ID

        # Assign system_admin role
        role_assignment = UserRoleAssignment(
            user_id=admin_user.id,
            role_id=admin_role.id,
            assigned_by=admin_user.id,  # Self-assigned
        )

        session.add(role_assignment)
        await session.commit()

        print("✅ Default admin user created successfully!")
        print("   Username: admin")
        print("   Email: admin@preventia.com")
        print("   Password: PreventIA@2025!")
        print("   ⚠️  PLEASE CHANGE THE DEFAULT PASSWORD IMMEDIATELY!")


async def verify_role_permissions():
    """Verify that default roles have correct permissions"""

    async with db_manager.get_session() as session:
        roles_query = select(UserRole)
        result = await session.execute(roles_query)
        roles = result.scalars().all()

        print(f"✅ Found {len(roles)} roles in database:")
        for role in roles:
            permissions_count = len(role.permissions) if role.permissions else 0
            print(f"   - {role.name}: {permissions_count} permissions")


async def initialize_auth_system():
    """Initialize the complete authentication system"""
    print("🔐 Initializing authentication system...")

    # Initialize role manager
    initialize_role_manager(db_manager)
    print("✅ Role manager initialized")

    # Verify roles exist
    await verify_role_permissions()

    # Create default admin if needed
    await create_default_admin()

    print("🔐 Authentication system initialization complete!")


if __name__ == "__main__":
    # Run initialization
    asyncio.run(initialize_auth_system())
