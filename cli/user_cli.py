"""
User management CLI tools for PreventIA News Analytics
Command-line interface for user and role administration
"""

from datetime import datetime
from typing import List, Optional

import click
from sqlalchemy import select

from services.api.auth.password_utils import (
    check_password_strength,
    generate_secure_password,
    hash_password,
)
from services.api.auth.role_manager import role_manager
from services.data.database.models import User, UserRole, UserRoleAssignment

from .base import BaseCLI, async_command, common_options, validate_email


class UserCLI(BaseCLI):
    """CLI for user and role management"""

    def __init__(self):
        super().__init__()

    async def create_user(
        self,
        username: str,
        email: str,
        full_name: str,
        password: Optional[str] = None,
        roles: Optional[List[str]] = None,
    ) -> dict:
        """Create a new user"""
        async with self.db_manager.get_session() as session:
            # Check if user already exists
            existing_query = select(User).where(
                (User.username == username) | (User.email == email)
            )
            existing = await session.execute(existing_query)
            if existing.scalar():
                raise click.ClickException(
                    f"User with username '{username}' or email '{email}' already exists"
                )

            # Generate password if not provided
            if not password:
                password = generate_secure_password(16)
                self.log(f"Generated password: {password}", "warning")
                self.log("⚠️  Please save this password securely!", "warning")

            # Validate password strength
            strength = check_password_strength(password)
            if strength["strength"] == "weak":
                raise click.ClickException(
                    "Password is too weak. Must include: 8+ characters, uppercase, lowercase, number, special character"
                )

            # Create user
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                password_hash=hash_password(password),
                is_active=True,
                password_changed_at=datetime.utcnow(),
            )

            session.add(user)
            await session.flush()  # Get user ID

            # Assign roles if provided
            assigned_roles = []
            if roles:
                for role_name in roles:
                    role_query = select(UserRole).where(UserRole.name == role_name)
                    role_result = await session.execute(role_query)
                    role = role_result.scalar()

                    if role:
                        assignment = UserRoleAssignment(
                            user_id=user.id,
                            role_id=role.id,
                            assigned_by=user.id,  # Self-assigned for CLI creation
                        )
                        session.add(assignment)
                        assigned_roles.append(role_name)
                    else:
                        self.log(f"Role '{role_name}' not found, skipping", "warning")

            await session.commit()
            await session.refresh(user)

            self.log(f"Created user: {user.username} ({user.email})", "success")

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "roles": assigned_roles,
                "generated_password": (
                    password
                    if not click.get_current_context().params.get("password")
                    else None
                ),
                "created_at": user.created_at.isoformat(),
            }

    async def list_users(self, status_filter: Optional[str] = None) -> List[dict]:
        """List all users"""
        async with self.db_manager.get_session() as session:
            query = select(User)
            if status_filter == "active":
                query = query.where(User.is_active == True)
            elif status_filter == "inactive":
                query = query.where(User.is_active == False)

            result = await session.execute(query)
            users = result.scalars().all()

            user_data = []
            for user in users:
                # Get user roles
                roles = await role_manager.get_user_roles(user.id)
                role_names = [role.name for role in roles]

                user_data.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "full_name": user.full_name,
                        "is_active": user.is_active,
                        "is_superuser": user.is_superuser,
                        "roles": role_names,
                        "last_login": (
                            user.last_login.strftime("%Y-%m-%d %H:%M")
                            if user.last_login
                            else "Never"
                        ),
                        "created_at": user.created_at.strftime("%Y-%m-%d"),
                    }
                )

            return user_data

    async def get_user_details(self, user_identifier: str) -> dict:
        """Get detailed user information by username, email, or ID"""
        async with self.db_manager.get_session() as session:
            # Try to parse as ID first
            try:
                user_id = int(user_identifier)
                query = select(User).where(User.id == user_id)
            except ValueError:
                # Search by username or email
                query = select(User).where(
                    (User.username == user_identifier) | (User.email == user_identifier)
                )

            result = await session.execute(query)
            user = result.scalar()

            if not user:
                raise click.ClickException(f"User '{user_identifier}' not found")

            # Get roles and permissions
            roles = await role_manager.get_user_roles(user.id)
            permissions = await role_manager.get_user_permissions(user.id)

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "roles": [
                    {"id": role.id, "name": role.name, "description": role.description}
                    for role in roles
                ],
                "permissions": list(permissions),
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "failed_login_attempts": user.failed_login_attempts,
                "account_locked_until": (
                    user.account_locked_until.isoformat()
                    if user.account_locked_until
                    else None
                ),
                "password_changed_at": (
                    user.password_changed_at.isoformat()
                    if user.password_changed_at
                    else None
                ),
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            }

    async def update_user(self, user_identifier: str, **kwargs) -> dict:
        """Update user information"""
        async with self.db_manager.get_session() as session:
            # Find user
            try:
                user_id = int(user_identifier)
                query = select(User).where(User.id == user_id)
            except ValueError:
                query = select(User).where(
                    (User.username == user_identifier) | (User.email == user_identifier)
                )

            result = await session.execute(query)
            user = result.scalar()

            if not user:
                raise click.ClickException(f"User '{user_identifier}' not found")

            # Update fields
            updated_fields = []
            for field, value in kwargs.items():
                if value is not None and hasattr(user, field):
                    old_value = getattr(user, field)
                    setattr(user, field, value)
                    updated_fields.append(f"{field}: {old_value} → {value}")

            user.updated_at = datetime.utcnow()
            await session.commit()

            self.log(f"Updated user: {user.username}", "success")
            if updated_fields and self.verbose:
                for field in updated_fields:
                    self.log(f"  {field}")

            return {
                "id": user.id,
                "username": user.username,
                "updated_fields": len(updated_fields),
                "updated_at": user.updated_at.isoformat(),
            }

    async def reset_password(
        self, user_identifier: str, new_password: Optional[str] = None
    ) -> dict:
        """Reset user password"""
        async with self.db_manager.get_session() as session:
            # Find user
            try:
                user_id = int(user_identifier)
                query = select(User).where(User.id == user_id)
            except ValueError:
                query = select(User).where(
                    (User.username == user_identifier) | (User.email == user_identifier)
                )

            result = await session.execute(query)
            user = result.scalar()

            if not user:
                raise click.ClickException(f"User '{user_identifier}' not found")

            # Generate password if not provided
            if not new_password:
                new_password = generate_secure_password(16)
                self.log(f"Generated password: {new_password}", "warning")
                self.log("⚠️  Please save this password securely!", "warning")

            # Validate password strength
            strength = check_password_strength(new_password)
            if strength["strength"] == "weak":
                raise click.ClickException("Password is too weak")

            # Update password
            user.password_hash = hash_password(new_password)
            user.password_changed_at = datetime.utcnow()
            user.failed_login_attempts = 0  # Reset failed attempts
            user.account_locked_until = None  # Unlock account

            await session.commit()

            self.log(f"Password reset for user: {user.username}", "success")

            return {
                "id": user.id,
                "username": user.username,
                "password_reset": True,
                "generated_password": (
                    new_password
                    if not click.get_current_context().params.get("password")
                    else None
                ),
                "reset_at": datetime.now().isoformat(),
            }

    async def assign_role(self, user_identifier: str, role_name: str) -> dict:
        """Assign role to user"""
        async with self.db_manager.get_session() as session:
            # Find user
            try:
                user_id = int(user_identifier)
                user_query = select(User).where(User.id == user_id)
            except ValueError:
                user_query = select(User).where(
                    (User.username == user_identifier) | (User.email == user_identifier)
                )

            user_result = await session.execute(user_query)
            user = user_result.scalar()

            if not user:
                raise click.ClickException(f"User '{user_identifier}' not found")

            # Find role
            role_query = select(UserRole).where(UserRole.name == role_name)
            role_result = await session.execute(role_query)
            role = role_result.scalar()

            if not role:
                raise click.ClickException(f"Role '{role_name}' not found")

            # Check if already assigned
            existing_query = select(UserRoleAssignment).where(
                UserRoleAssignment.user_id == user.id,
                UserRoleAssignment.role_id == role.id,
            )
            existing = await session.execute(existing_query)

            if existing.scalar():
                raise click.ClickException(
                    f"User '{user.username}' already has role '{role_name}'"
                )

            # Create assignment
            assignment = UserRoleAssignment(
                user_id=user.id, role_id=role.id, assigned_by=user.id  # CLI assignment
            )

            session.add(assignment)
            await session.commit()

            self.log(
                f"Assigned role '{role_name}' to user '{user.username}'", "success"
            )

            return {
                "user_id": user.id,
                "username": user.username,
                "role_assigned": role_name,
                "assigned_at": datetime.now().isoformat(),
            }

    async def revoke_role(self, user_identifier: str, role_name: str) -> dict:
        """Revoke role from user"""
        async with self.db_manager.get_session() as session:
            # Find user
            try:
                user_id = int(user_identifier)
                user_query = select(User).where(User.id == user_id)
            except ValueError:
                user_query = select(User).where(
                    (User.username == user_identifier) | (User.email == user_identifier)
                )

            user_result = await session.execute(user_query)
            user = user_result.scalar()

            if not user:
                raise click.ClickException(f"User '{user_identifier}' not found")

            # Find role
            role_query = select(UserRole).where(UserRole.name == role_name)
            role_result = await session.execute(role_query)
            role = role_result.scalar()

            if not role:
                raise click.ClickException(f"Role '{role_name}' not found")

            # Find assignment
            assignment_query = select(UserRoleAssignment).where(
                UserRoleAssignment.user_id == user.id,
                UserRoleAssignment.role_id == role.id,
            )
            assignment_result = await session.execute(assignment_query)
            assignment = assignment_result.scalar()

            if not assignment:
                raise click.ClickException(
                    f"User '{user.username}' does not have role '{role_name}'"
                )

            # Delete assignment
            await session.delete(assignment)
            await session.commit()

            self.log(
                f"Revoked role '{role_name}' from user '{user.username}'", "success"
            )

            return {
                "user_id": user.id,
                "username": user.username,
                "role_revoked": role_name,
                "revoked_at": datetime.now().isoformat(),
            }

    async def list_roles(self) -> List[dict]:
        """List all available roles"""
        async with self.db_manager.get_session() as session:
            query = select(UserRole)
            result = await session.execute(query)
            roles = result.scalars().all()

            role_data = []
            for role in roles:
                # Count users with this role
                user_count_query = select(UserRoleAssignment).where(
                    UserRoleAssignment.role_id == role.id
                )
                user_count_result = await session.execute(user_count_query)
                user_count = len(user_count_result.scalars().all())

                role_data.append(
                    {
                        "id": role.id,
                        "name": role.name,
                        "description": role.description,
                        "permissions": role.permissions,
                        "is_system_role": role.is_system_role,
                        "user_count": user_count,
                        "created_at": role.created_at.strftime("%Y-%m-%d"),
                    }
                )

            return role_data


# CLI Commands
@click.group()
@click.pass_context
def user(ctx):
    """User management commands"""
    ctx.ensure_object(dict)
    ctx.obj["cli"] = UserCLI()


@user.command()
@click.option(
    "--status", type=click.Choice(["active", "inactive"]), help="Filter by status"
)
@common_options
@click.pass_context
@async_command
async def list(ctx, status, verbose, quiet, format):
    """List all users"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    users = await cli.list_users(status)

    if format == "json":
        click.echo(cli.format_json({"users": users}))
    else:
        if not users:
            cli.log("No users found", "warning")
            return

        headers = [
            "ID",
            "Username",
            "Email",
            "Full Name",
            "Active",
            "Roles",
            "Last Login",
        ]
        rows = [
            [
                u["id"],
                u["username"],
                u["email"][:30],
                u["full_name"][:25],
                "✅" if u["is_active"] else "❌",
                ", ".join(u["roles"][:2]),
                u["last_login"],
            ]
            for u in users
        ]
        click.echo(cli.format_table(rows, headers))


@user.command()
@click.argument("user_identifier")
@common_options
@click.pass_context
@async_command
async def show(ctx, user_identifier, verbose, quiet, format):
    """Show detailed user information"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    details = await cli.get_user_details(user_identifier)

    if format == "json":
        click.echo(cli.format_json(details))
    else:
        click.echo(f"\n👤 User Details: {details['username']}")
        click.echo(f"  ID: {details['id']}")
        click.echo(f"  Email: {details['email']}")
        click.echo(f"  Full Name: {details['full_name']}")
        click.echo(f"  Active: {'✅' if details['is_active'] else '❌'}")
        click.echo(f"  Superuser: {'✅' if details['is_superuser'] else '❌'}")
        click.echo(f"  Last Login: {details['last_login'] or 'Never'}")

        if details["roles"]:
            click.echo(f"\n🔑 Roles:")
            for role in details["roles"]:
                click.echo(f"  - {role['name']}: {role['description']}")

        if details["permissions"] and verbose:
            click.echo(f"\n🛡️  Permissions:")
            for perm in sorted(details["permissions"]):
                click.echo(f"  - {perm}")


@user.command()
@click.argument("username")
@click.argument("email", callback=validate_email)
@click.argument("full_name")
@click.option("--password", help="User password (will be generated if not provided)")
@click.option(
    "--role",
    "roles",
    multiple=True,
    help="Assign roles to user (can be used multiple times)",
)
@common_options
@click.pass_context
@async_command
async def create(
    ctx, username, email, full_name, password, roles, verbose, quiet, format
):
    """Create a new user"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    result = await cli.create_user(
        username=username,
        email=email,
        full_name=full_name,
        password=password,
        roles=list(roles) if roles else None,
    )

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(f"✅ Created user: {result['username']} (ID: {result['id']})")
        if result["roles"]:
            click.echo(f"   Assigned roles: {', '.join(result['roles'])}")
        if result.get("generated_password"):
            click.echo(f"   Generated password: {result['generated_password']}")
            click.echo("   ⚠️  Please save this password securely!")


@user.command()
@click.argument("user_identifier")
@click.option("--full-name", help="Update full name")
@click.option("--email", callback=validate_email, help="Update email address")
@click.option("--active/--inactive", default=None, help="Update active status")
@common_options
@click.pass_context
@async_command
async def update(
    ctx, user_identifier, full_name, email, active, verbose, quiet, format
):
    """Update user information"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    kwargs = {}
    if full_name:
        kwargs["full_name"] = full_name
    if email:
        kwargs["email"] = email
    if active is not None:
        kwargs["is_active"] = active

    if not kwargs:
        raise click.ClickException("No update parameters provided")

    result = await cli.update_user(user_identifier, **kwargs)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(
            f"✅ Updated user: {result['username']} ({result['updated_fields']} fields)"
        )


@user.command()
@click.argument("user_identifier")
@click.option("--password", help="New password (will be generated if not provided)")
@common_options
@click.pass_context
@async_command
async def reset_password(ctx, user_identifier, password, verbose, quiet, format):
    """Reset user password"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    if not cli.confirm_action(f"Reset password for user '{user_identifier}'?", False):
        click.echo("Operation cancelled")
        return

    result = await cli.reset_password(user_identifier, password)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(f"✅ Password reset for user: {result['username']}")
        if result.get("generated_password"):
            click.echo(f"   New password: {result['generated_password']}")
            click.echo("   ⚠️  Please save this password securely!")


@user.command()
@click.argument("user_identifier")
@click.argument("role_name")
@common_options
@click.pass_context
@async_command
async def assign_role(ctx, user_identifier, role_name, verbose, quiet, format):
    """Assign role to user"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    result = await cli.assign_role(user_identifier, role_name)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(
            f"✅ Assigned role '{result['role_assigned']}' to user '{result['username']}'"
        )


@user.command()
@click.argument("user_identifier")
@click.argument("role_name")
@common_options
@click.pass_context
@async_command
async def revoke_role(ctx, user_identifier, role_name, verbose, quiet, format):
    """Revoke role from user"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    if not cli.confirm_action(
        f"Revoke role '{role_name}' from user '{user_identifier}'?", False
    ):
        click.echo("Operation cancelled")
        return

    result = await cli.revoke_role(user_identifier, role_name)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(
            f"✅ Revoked role '{result['role_revoked']}' from user '{result['username']}'"
        )


@user.command()
@common_options
@click.pass_context
@async_command
async def list_roles(ctx, verbose, quiet, format):
    """List all available roles"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    roles = await cli.list_roles()

    if format == "json":
        click.echo(cli.format_json({"roles": roles}))
    else:
        if not roles:
            cli.log("No roles found", "warning")
            return

        headers = ["ID", "Name", "Description", "System", "Users", "Permissions"]
        rows = [
            [
                r["id"],
                r["name"],
                r["description"][:40],
                "✅" if r["is_system_role"] else "❌",
                r["user_count"],
                len(r["permissions"]),
            ]
            for r in roles
        ]
        click.echo(cli.format_table(rows, headers))


if __name__ == "__main__":
    user()
