"""
pytest configuration and fixtures for PreventIA News Analytics
Provides reusable fixtures for database, testing utilities, and mock data
"""

import asyncio
import os

# Add project root to path
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from datetime import datetime

from services.data.database.connection import DatabaseManager
from services.nlp.src.sentiment import SentimentAnalyzer
from services.shared.models.article import Article

# Configure test environment
os.environ["DATABASE_URL"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://preventia:test_password@localhost:5433/preventia_test",
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_manager() -> AsyncGenerator[DatabaseManager, None]:
    """
    Provide a database manager instance for testing
    Uses test database configuration
    """
    db_manager = DatabaseManager()

    try:
        # Initialize database connection
        await db_manager.initialize()

        # Verify connection
        health = await db_manager.health_check()
        if not health:
            pytest.skip("Test database not available")

        yield db_manager

    finally:
        # Cleanup
        if hasattr(db_manager, "_pool") and db_manager._pool:
            await db_manager._pool.close()


@pytest_asyncio.fixture
async def clean_database(test_db_manager):
    """
    Provide a clean database state for each test
    Runs in transaction that gets rolled back
    """
    # Begin transaction
    async with test_db_manager.get_connection() as conn:
        transaction = conn.transaction()
        await transaction.start()

        try:
            yield test_db_manager
        finally:
            # Rollback transaction to clean state
            await transaction.rollback()


@pytest.fixture
def sentiment_analyzer():
    """Provide a configured sentiment analyzer instance"""
    return SentimentAnalyzer()


@pytest.fixture
def sample_article():
    """Provide a sample article for testing"""
    return Article(
        title="Sample Medical News Article",
        published_at=datetime(2024, 1, 15),
        summary="This is a sample article about medical research with positive outcomes.",
        content="Detailed content about medical research findings that show promising results.",
        url="https://example.com/sample-article",
    )


@pytest.fixture
def sample_articles():
    """Provide multiple sample articles for batch testing"""
    return [
        Article(
            title="Positive Medical Breakthrough",
            published_at=datetime(2024, 1, 15),
            summary="Scientists discover new treatment with excellent results.",
            content="Detailed positive medical content.",
            url="https://example.com/positive",
        ),
        Article(
            title="Concerning Health Trend",
            published_at=datetime(2024, 1, 16),
            summary="Study shows worrying increase in disease rates.",
            content="Detailed negative medical content.",
            url="https://example.com/negative",
        ),
        Article(
            title="FDA Approves New Diagnostic Tool",
            published_at=datetime(2024, 1, 17),
            summary="Regulatory approval for medical device.",
            content="Neutral regulatory content.",
            url="https://example.com/neutral",
        ),
    ]


@pytest.fixture
def mock_http_responses():
    """Provide mock HTTP responses for scraper testing"""
    return {
        "www.breastcancer.org": """
        <html>
            <head><title>Breast Cancer News</title></head>
            <body>
                <article>
                    <h1>New Treatment Shows Promise</h1>
                    <p>Research indicates positive outcomes...</p>
                </article>
            </body>
        </html>
        """,
        "www.webmd.com": """
        <html>
            <head><title>WebMD Health News</title></head>
            <body>
                <h2>Medical Update</h2>
                <p>Latest health information...</p>
            </body>
        </html>
        """,
    }


# Pytest markers for test categorization
def pytest_configure(config):
    """Register custom pytest markers"""
    config.addinivalue_line("markers", "unit: Unit tests for isolated components")
    config.addinivalue_line(
        "markers", "integration: Integration tests for component interaction"
    )
    config.addinivalue_line("markers", "e2e: End-to-end tests for complete workflows")
    config.addinivalue_line("markers", "performance: Performance and load tests")
    config.addinivalue_line("markers", "slow: Slow running tests (>10s)")
    config.addinivalue_line("markers", "database: Tests requiring database connection")


# Test collection and execution helpers
def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their location"""
    for item in items:
        # Add markers based on test file path
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)

        # Add database marker for tests that use database fixtures
        if any(
            fixture in item.fixturenames
            for fixture in ["test_db_manager", "clean_database"]
        ):
            item.add_marker(pytest.mark.database)
