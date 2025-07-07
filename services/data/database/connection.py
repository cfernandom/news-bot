"""
Database connection and session management for PreventIA News Analytics
Supports both SQLAlchemy ORM and raw SQL queries via asyncpg
"""

import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from .models import Base


class DatabaseManager:
    """
    Manages database connections for both ORM and raw SQL operations
    """

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        # Convert postgres:// to postgresql+asyncpg:// for SQLAlchemy
        self.sqlalchemy_url = self.database_url.replace(
            "postgresql://", "postgresql+asyncpg://"
        )

        # SQLAlchemy async engine with proper connection pooling
        self.engine = create_async_engine(
            self.sqlalchemy_url,
            echo=bool(os.getenv("DATABASE_ECHO", False)),  # Set to True for SQL logging
            pool_size=5,  # Base connection pool size
            max_overflow=10,  # Additional connections beyond pool_size
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600,  # Recycle connections every hour
            pool_timeout=30,  # Timeout for getting connection from pool
        )

        # Session factory
        self.session_factory = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

        # Connection pool for raw SQL queries
        self._pool: Optional[asyncpg.Pool] = None

    async def initialize(self):
        """Initialize database connection pool"""
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                self.database_url,
                min_size=2,
                max_size=8,  # Reduced from 10 to avoid conflicts
                command_timeout=30,  # Reduced timeout
                server_settings={
                    "application_name": "preventia_analytics",
                },
                max_inactive_connection_lifetime=300,  # 5 minutes
            )

    async def close(self):
        """Close all database connections with proper cleanup"""
        try:
            if self._pool:
                await self._pool.close()
                self._pool = None
        except Exception as e:
            # Log error but don't raise to allow engine cleanup
            print(f"Warning: Error closing asyncpg pool: {e}")

        try:
            await self.engine.dispose()
        except Exception as e:
            print(f"Warning: Error disposing SQLAlchemy engine: {e}")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get SQLAlchemy async session for ORM operations
        Usage:
            async with db.get_session() as session:
                result = await session.execute(select(Article))
        """
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """
        Get raw asyncpg connection for complex SQL queries with proper error handling
        Usage:
            async with db.get_connection() as conn:
                result = await conn.fetch("SELECT * FROM articles WHERE ...")
        """
        if not self._pool:
            await self.initialize()

        connection = None
        try:
            connection = await self._pool.acquire()
            yield connection
        except Exception as e:
            # Log error for debugging
            print(f"Database connection error: {e}")
            raise
        finally:
            if connection:
                try:
                    await self._pool.release(connection)
                except Exception as e:
                    print(f"Warning: Error releasing connection: {e}")

    async def execute_sql(self, query: str, *args) -> list:
        """
        Execute raw SQL query and return results
        Usage:
            results = await db.execute_sql(
                "SELECT COUNT(*) FROM articles WHERE published_at > $1",
                datetime.now()
            )
        """
        async with self.get_connection() as conn:
            return await conn.fetch(query, *args)

    async def execute_sql_one(self, query: str, *args) -> Optional[dict]:
        """
        Execute raw SQL query and return single result
        """
        async with self.get_connection() as conn:
            return await conn.fetchrow(query, *args)

    async def execute_sql_scalar(self, query: str, *args):
        """
        Execute raw SQL query and return single value
        """
        async with self.get_connection() as conn:
            return await conn.fetchval(query, *args)

    async def create_tables(self):
        """Create all tables (for development/testing)"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        """Drop all tables (for development/testing)"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def health_check(self) -> bool:
        """Check if database is accessible"""
        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()


# Dependency for FastAPI
async def get_db_session():
    """FastAPI dependency for getting database session"""
    async with db_manager.get_session() as session:
        yield session


async def get_db_connection():
    """FastAPI dependency for getting raw database connection"""
    async with db_manager.get_connection() as connection:
        yield connection


# Initialization functions for application startup/shutdown
async def init_database():
    """Initialize database on application startup"""
    await db_manager.initialize()

    # Run health check
    if not await db_manager.health_check():
        raise RuntimeError("Database connection failed")

    print("✅ Database initialized successfully")


async def close_database():
    """Close database connections on application shutdown"""
    await db_manager.close()
    print("📝 Database connections closed")


# Development utilities
async def reset_database():
    """Reset database (drop and recreate tables) - DEVELOPMENT ONLY"""
    print("⚠️  Resetting database...")
    await db_manager.drop_tables()
    await db_manager.create_tables()
    print("✅ Database reset complete")


if __name__ == "__main__":
    # Test database connection
    async def test_connection():
        await init_database()

        # Test ORM
        async with db_manager.get_session() as session:
            result = await session.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"PostgreSQL version (ORM): {version}")

        # Test raw SQL
        version = await db_manager.execute_sql_scalar("SELECT version()")
        print(f"PostgreSQL version (Raw SQL): {version}")

        await close_database()

    asyncio.run(test_connection())
