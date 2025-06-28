"""
Unit tests for database connection management
Tests DatabaseManager class functionality in isolation
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from services.data.database.connection import DatabaseManager

class TestDatabaseManager:
    """Test DatabaseManager class functionality"""
    
    def test_init_with_database_url(self):
        """Test DatabaseManager initialization with valid DATABASE_URL"""
        with patch.dict('os.environ', {'DATABASE_URL': 'postgresql://user:pass@localhost/db'}):
            db_manager = DatabaseManager()
            assert db_manager.database_url == 'postgresql://user:pass@localhost/db'
            assert 'postgresql+asyncpg://' in db_manager.sqlalchemy_url
    
    def test_init_without_database_url(self):
        """Test DatabaseManager initialization fails without DATABASE_URL"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="DATABASE_URL environment variable is required"):
                DatabaseManager()
    
    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """Test successful health check"""
        with patch.dict('os.environ', {'DATABASE_URL': 'postgresql://user:pass@localhost/db'}):
            db_manager = DatabaseManager()
            
            # Mock the connection pool and execute method
            mock_pool = AsyncMock()
            mock_conn = AsyncMock()
            mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
            mock_conn.fetchval.return_value = 1
            
            db_manager._pool = mock_pool
            
            result = await db_manager.health_check()
            assert result is True
            mock_conn.fetchval.assert_called_once_with("SELECT 1")
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self):
        """Test health check failure"""
        with patch.dict('os.environ', {'DATABASE_URL': 'postgresql://user:pass@localhost/db'}):
            db_manager = DatabaseManager()
            
            # Mock failed connection
            mock_pool = AsyncMock()
            mock_conn = AsyncMock()
            mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
            mock_conn.fetchval.side_effect = Exception("Connection failed")
            
            db_manager._pool = mock_pool
            
            result = await db_manager.health_check()
            assert result is False
    
    @pytest.mark.asyncio
    async def test_execute_sql_with_params(self):
        """Test executing SQL with parameters"""
        with patch.dict('os.environ', {'DATABASE_URL': 'postgresql://user:pass@localhost/db'}):
            db_manager = DatabaseManager()
            
            # Mock the connection and result
            mock_pool = AsyncMock()
            mock_conn = AsyncMock()
            mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
            mock_conn.fetch.return_value = [{'id': 1, 'name': 'test'}]
            
            db_manager._pool = mock_pool
            
            result = await db_manager.execute_sql("SELECT * FROM test WHERE id = $1", 1)
            
            assert result == [{'id': 1, 'name': 'test'}]
            mock_conn.fetch.assert_called_once_with("SELECT * FROM test WHERE id = $1", 1)

@pytest.mark.unit
class TestDatabaseHelpers:
    """Test database utility functions"""
    
    def test_url_conversion(self):
        """Test PostgreSQL URL conversion for SQLAlchemy"""
        with patch.dict('os.environ', {'DATABASE_URL': 'postgresql://user:pass@localhost/db'}):
            db_manager = DatabaseManager()
            assert db_manager.sqlalchemy_url == 'postgresql+asyncpg://user:pass@localhost/db'