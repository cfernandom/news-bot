# Testing Structure Standard - PreventIA News Analytics

## Directory Structure

```
tests/
├── conftest.py                    # pytest configuration and fixtures
├── pytest.ini                    # pytest settings
├── requirements-test.txt          # testing dependencies
├── README.md                      # testing documentation
│
├── unit/                          # Unit tests (isolated components)
│   ├── test_database/
│   │   ├── test_connection.py     # Database connection tests
│   │   ├── test_models.py         # SQLAlchemy model tests
│   │   └── test_migrations.py     # Migration tests
│   ├── test_nlp/
│   │   ├── test_sentiment.py      # Sentiment analysis unit tests
│   │   ├── test_analyzer.py       # NLP analyzer tests
│   │   └── test_keywords.py       # Keyword extraction tests
│   ├── test_scrapers/
│   │   ├── test_extractors.py     # Individual extractor tests
│   │   └── test_utils.py          # Scraper utility tests
│   └── test_services/
│       ├── test_copywriter.py     # Copywriter service tests
│       └── test_orchestrator.py   # Orchestrator tests
│
├── integration/                   # Integration tests (component interaction)
│   ├── test_scraper_database.py   # Scraper → Database integration
│   ├── test_nlp_pipeline.py       # NLP → Database integration
│   ├── test_full_pipeline.py      # End-to-end article processing
│   └── test_api_endpoints.py      # API integration tests (future)
│
├── e2e/                          # End-to-end tests (full system)
│   ├── test_article_lifecycle.py  # Complete article processing
│   ├── test_batch_processing.py   # Batch operations
│   └── test_analytics_flow.py     # Analytics generation
│
├── performance/                   # Performance and load tests
│   ├── test_database_load.py     # Database performance
│   ├── test_scraper_speed.py     # Scraper performance
│   └── test_nlp_batch.py         # NLP batch processing
│
├── fixtures/                     # Test data and mocks
│   ├── sample_articles.json      # Sample article data
│   ├── mock_responses/           # HTTP response mocks
│   └── database_fixtures.py      # Database test data
│
└── utils/                        # Testing utilities
    ├── database_helpers.py       # Database testing helpers
    ├── mock_factories.py         # Mock object factories
    └── assertions.py             # Custom assertions
```

## Testing Standards

### 1. Naming Conventions
- **Files**: `test_*.py` or `*_test.py`
- **Classes**: `Test*` (for grouped tests)
- **Methods**: `test_*` (descriptive action)
- **Fixtures**: `*_fixture` or descriptive names

### 2. Test Categories

#### Unit Tests (`tests/unit/`)
- Test single functions/methods in isolation
- Use mocks for external dependencies
- Fast execution (< 1s per test)
- High coverage of business logic

#### Integration Tests (`tests/integration/`)
- Test component interactions
- Use real database (test instance)
- Moderate execution time (1-10s per test)
- Test data flow between services

#### End-to-End Tests (`tests/e2e/`)
- Test complete user workflows
- Use full system setup
- Longer execution time (10s+ per test)
- Test real-world scenarios

#### Performance Tests (`tests/performance/`)
- Measure execution speed and resource usage
- Load testing for scalability
- Memory and CPU profiling
- Database query optimization

### 3. Test Configuration

#### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --tb=short
    -v
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    performance: Performance tests
    slow: Slow running tests
    database: Tests requiring database
```

#### conftest.py Structure
```python
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from services.data.database.connection import DatabaseManager

# Test database fixture
@pytest.fixture(scope="session")
async def test_db():
    # Setup test database
    pass

# Async test support
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

### 4. Test Execution Commands

```bash
# Run all tests
pytest

# Run by category
pytest -m unit
pytest -m integration
pytest -m e2e

# Run specific test file
pytest tests/unit/test_nlp/test_sentiment.py

# Run with coverage
pytest --cov=services --cov-report=html

# Run performance tests
pytest -m performance --benchmark-only
```

### 5. Continuous Integration

Tests should run in CI pipeline with:
- **Unit tests**: Every commit
- **Integration tests**: Every PR
- **E2E tests**: Before merge to main
- **Performance tests**: Weekly/on-demand

### 6. Test Data Management

- Use factories for dynamic test data
- Isolate test data from production
- Clean up test data after each test
- Use database transactions for rollback

### 7. Mocking Strategy

- Mock external APIs and services
- Use real database for integration tests
- Mock file system operations
- Mock time-dependent functions

## Implementation Guidelines

1. **Start with unit tests** for new features
2. **Add integration tests** for component interactions
3. **Include e2e tests** for user-facing features
4. **Write performance tests** for critical paths
5. **Maintain test coverage** above 80%
6. **Keep tests fast** and independent
7. **Use descriptive test names** that explain the scenario
8. **Group related tests** in classes
9. **Follow AAA pattern**: Arrange, Act, Assert
10. **Test edge cases** and error conditions