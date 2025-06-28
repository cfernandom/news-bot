# Testing Suite - PreventIA News Analytics

## Overview

Comprehensive testing framework for PreventIA News Analytics system, organized in a professional structure for maintainability and clear separation of concerns.

## Structure

```
tests/
├── conftest.py                    # pytest configuration and fixtures
├── pytest.ini                    # pytest settings
├── requirements-test.txt          # testing dependencies
├── README.md                      # this file
│
├── unit/                          # Unit tests (isolated components)
│   ├── test_database/             # Database layer tests
│   ├── test_nlp/                  # NLP and sentiment analysis tests
│   ├── test_scrapers/             # Scraper component tests
│   └── test_services/             # Service layer tests
│
├── integration/                   # Integration tests (component interaction)
│   ├── test_nlp_pipeline.py       # NLP → Database integration
│   ├── test_scraper_database.py   # Scraper → Database integration
│   └── test_full_pipeline.py      # End-to-end article processing
│
├── e2e/                          # End-to-end tests (full system)
├── performance/                   # Performance and load tests
├── fixtures/                     # Test data and mocks
└── utils/                        # Testing utilities
```

## Quick Start

### 1. Install Testing Dependencies

```bash
# From project root
source venv/bin/activate
pip install -r tests/requirements-test.txt
```

### 2. Run Tests

```bash
# From project root
cd tests

# Run all tests
pytest

# Run by category
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m database      # Database-related tests

# Run specific test file
pytest unit/test_nlp/test_sentiment.py

# Run with coverage
pytest --cov=../services --cov-report=html
```

### 3. Test Categories

#### Unit Tests (`-m unit`)
- Test individual functions/classes in isolation
- Use mocks for external dependencies
- Fast execution (< 1s per test)
- Located in `tests/unit/`

#### Integration Tests (`-m integration`)
- Test component interactions
- Use real database (test instance)
- Moderate execution time (1-10s per test)
- Located in `tests/integration/`

#### End-to-End Tests (`-m e2e`)
- Test complete user workflows
- Use full system setup
- Longer execution time (10s+ per test)
- Located in `tests/e2e/`

## Current Implementation Status

### ✅ Completed

#### Unit Tests
- **Sentiment Analysis** (`unit/test_nlp/test_sentiment.py`)
  - 14 comprehensive tests covering all functionality
  - Tests for VADER + spaCy integration
  - Medical content threshold testing
  - Error handling and edge cases

- **Database Connection** (`unit/test_database/test_connection.py`)
  - Connection management testing
  - Health check validation
  - SQL execution testing

#### Integration Tests
- **NLP Pipeline** (`integration/test_nlp_pipeline.py`)
  - End-to-end sentiment analysis with database
  - Batch processing integration
  - Error handling in pipeline context

#### Configuration
- **pytest.ini** - Complete pytest configuration
- **conftest.py** - Fixtures and test setup
- **requirements-test.txt** - Verified testing dependencies

### 🚧 In Development

#### Legacy Tests Migration
- `legacy_test_sentiment_analysis.py` - Being migrated to new structure
- `legacy_test_database.py` - Being migrated to new structure
- `scrapers/` tests - Need reorganization into new structure

## Best Practices

### 1. Test Naming
```python
def test_analyze_sentiment_positive_medical_content():
    """Test sentiment analysis with positive medical content"""
    # Clear, descriptive test names that explain the scenario
```

### 2. Test Structure (AAA Pattern)
```python
def test_example():
    # Arrange - Set up test data
    analyzer = SentimentAnalyzer()
    text = "Medical breakthrough shows promising results"
    
    # Act - Execute the code under test
    result = analyzer.analyze_sentiment(text)
    
    # Assert - Verify the results
    assert result['sentiment_label'] == 'positive'
    assert result['confidence'] > 0.5
```

### 3. Fixtures Usage
```python
def test_with_database(test_db_manager):
    """Use fixtures for consistent test setup"""
    # test_db_manager provides clean database state
    pass

def test_with_sample_data(sample_articles):
    """Use data fixtures for consistent test data"""
    # sample_articles provides test articles
    pass
```

### 4. Markers
```python
@pytest.mark.unit
def test_isolated_function():
    """Mark tests by category"""
    pass

@pytest.mark.database
@pytest.mark.integration
async def test_database_integration():
    """Combine markers for specific test requirements"""
    pass
```

## Test Execution Examples

### Development Workflow
```bash
# Quick unit tests during development
pytest -m unit -v

# Test specific feature
pytest unit/test_nlp/ -v

# Test with coverage
pytest unit/test_nlp/test_sentiment.py --cov=../services/nlp --cov-report=term-missing
```

### CI/CD Pipeline
```bash
# Pre-commit: Fast unit tests
pytest -m unit --tb=short

# PR validation: Unit + Integration
pytest -m "unit or integration" --tb=short

# Pre-merge: All tests
pytest --tb=short
```

### Performance Testing
```bash
# Run performance tests
pytest -m performance --benchmark-only

# Profile specific tests
pytest unit/test_nlp/test_sentiment.py --profile
```

## Adding New Tests

### 1. Determine Test Category
- **Unit**: Testing isolated functions/classes
- **Integration**: Testing component interactions
- **E2E**: Testing complete workflows

### 2. Create Test File
```bash
# Unit test example
touch tests/unit/test_new_feature/test_new_component.py
```

### 3. Follow Template
```python
"""
Unit tests for new component
Tests NewComponent class functionality in isolation
"""

import pytest
from unittest.mock import Mock, patch
from services.new_feature.new_component import NewComponent

@pytest.mark.unit
class TestNewComponent:
    """Test NewComponent class functionality"""
    
    def test_component_initialization(self):
        """Test component initializes correctly"""
        component = NewComponent()
        assert component is not None
    
    def test_component_method_with_valid_input(self):
        """Test component method with valid input"""
        component = NewComponent()
        result = component.process("valid input")
        assert result is not None
    
    def test_component_method_with_invalid_input(self):
        """Test component method handles invalid input"""
        component = NewComponent()
        with pytest.raises(ValueError):
            component.process(None)
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the tests directory
   cd tests
   pytest unit/test_nlp/test_sentiment.py
   ```

2. **Database Connection**
   ```bash
   # Ensure test database is running
   docker compose up postgres -d
   
   # Check environment variables
   echo $DATABASE_URL
   ```

3. **Missing Dependencies**
   ```bash
   # Install test dependencies
   pip install -r tests/requirements-test.txt
   ```

### Performance Issues
- Use `pytest-benchmark` for performance testing
- Profile with `--profile` flag
- Check database queries with `--db-profile`

### Coverage Reports
```bash
# Generate HTML coverage report
pytest --cov=../services --cov-report=html

# Open coverage report
open htmlcov/index.html
```

## Future Enhancements

1. **Performance Testing Suite**
   - Database query optimization tests
   - Scraper performance benchmarks
   - NLP batch processing tests

2. **E2E Test Automation**
   - Complete article lifecycle tests
   - Analytics generation workflows
   - API endpoint testing (when implemented)

3. **Test Data Management**
   - Factory patterns for test data
   - Database fixtures with realistic data
   - Mock response libraries

4. **CI/CD Integration**
   - Automated test execution
   - Coverage reporting
   - Performance regression detection