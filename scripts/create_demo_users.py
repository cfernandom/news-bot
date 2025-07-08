#!/usr/bin/env python3
"""
Script para crear usuarios de demostración para el dashboard de administración
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from services.api.auth.password_utils import PasswordManager
from services.data.database.connection import DatabaseManager


async def create_demo_users():
    """Create demo users for admin dashboard"""

    password_manager = PasswordManager()
    db_manager = DatabaseManager()

    # Demo users data
    demo_users = [
        {
            "username": "admin",
            "email": "admin@preventia.com",
            "full_name": "System Administrator",
            "password": "admin123",
            "role": "system_admin",
        },
        {
            "username": "demo",
            "email": "demo@preventia.com",
            "full_name": "Demo User",
            "password": "demo123",
            "role": "source_viewer",
        },
    ]

    try:
        # First, let's verify if users already exist and check passwords
        for user_data in demo_users:
            print(f"Processing user: {user_data['username']}")

            # Check if user exists
            result = await db_manager.execute_sql(
                "SELECT id, username, email, password_hash FROM users WHERE username = $1 OR email = $2",
                user_data["username"],
                user_data["email"],
            )

            if result:
                user_id, username, email, stored_hash = result[0]
                print(f"  - User exists: {username} ({email})")

                # Verify password
                if password_manager.verify_password(user_data["password"], stored_hash):
                    print(f"  - Password is correct ✓")
                else:
                    print(f"  - Password is incorrect ✗")
                    # Update password
                    new_hash = password_manager.hash_password(user_data["password"])
                    await db_manager.execute_sql(
                        "UPDATE users SET password_hash = $1 WHERE id = $2",
                        new_hash,
                        user_id,
                    )
                    print(f"  - Password updated ✓")

            else:
                print(f"  - User does not exist, creating...")

                # Hash password
                password_hash = password_manager.hash_password(user_data["password"])

                # Create user
                user_result = await db_manager.execute_sql(
                    """
                    INSERT INTO users (username, email, full_name, password_hash, is_active, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
                    RETURNING id
                    """,
                    user_data["username"],
                    user_data["email"],
                    user_data["full_name"],
                    password_hash,
                    True,
                )

                if user_result:
                    user_id = user_result[0][0]
                    print(f"  - User created with ID: {user_id}")

                    # Get role ID
                    role_result = await db_manager.execute_sql(
                        "SELECT id FROM user_roles WHERE name = $1", user_data["role"]
                    )

                    if role_result:
                        role_id = role_result[0][0]

                        # Assign role
                        await db_manager.execute_sql(
                            """
                            INSERT INTO user_role_assignments (user_id, role_id, assigned_at)
                            VALUES ($1, $2, NOW())
                            """,
                            user_id,
                            role_id,
                        )
                        print(f"  - Role '{user_data['role']}' assigned ✓")
                    else:
                        print(f"  - Role '{user_data['role']}' not found ✗")
                else:
                    print(f"  - Failed to create user ✗")

        print("\nDemo users setup completed!")

        # List all users
        users = await db_manager.execute_sql(
            """
            SELECT u.username, u.email, u.full_name, r.name as role_name, u.is_active
            FROM users u
            LEFT JOIN user_role_assignments ura ON u.id = ura.user_id
            LEFT JOIN user_roles r ON ura.role_id = r.id
            ORDER BY u.username
            """
        )

        print("\nCurrent users:")
        for user in users:
            username, email, full_name, role_name, is_active = user
            status = "Active" if is_active else "Inactive"
            print(
                f"  - {username} ({email}) - {full_name} - Role: {role_name} - Status: {status}"
            )

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(create_demo_users())
