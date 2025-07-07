# PreventIA Integration Test Suite

Comprehensive end-to-end integration tests for the PreventIA News Analytics system.

## Overview

This integration test suite validates the complete PreventIA system functionality including:

- **System Integration**: Complete data flow from sources to analytics
- **CLI Integration**: Command-line interface functionality
- **Authentication Integration**: JWT tokens, roles, and permissions
- **Data Pipeline Integration**: Scraping → Processing → Storage → Analytics
- **End-to-End Validation**: Full system workflows and performance

## Test Structure

```
tests/integration/
├── README.md                           # This file
├── test_system_integration.py          # Complete system workflow tests
├── test_cli_integration.py             # CLI tools integration tests
├── test_auth_integration.py            # Authentication system tests
├── test_data_pipeline_integration.py   # Data pipeline tests
├── test_end_to_end_validation.py       # Comprehensive validation tests
└── ../run_integration_tests.py         # Test runner script
```

## Quick Start

### Prerequisites

1. **Database Setup**: PostgreSQL test database running
2. **Environment Variables**: Configured in `.env` or environment
3. **Dependencies**: All project dependencies installed

```bash
# Setup test database
docker compose up postgres -d

# Install dependencies
pip install -r requirements.txt
pip install -r tests/requirements-test.txt
```

### Running Tests

```bash
# Run all integration tests
python tests/run_integration_tests.py

# Run specific test suite
python tests/run_integration_tests.py system

# Run with verbose output and generate report
python tests/run_integration_tests.py --verbose --report test-report.md

# Run multiple specific suites
python tests/run_integration_tests.py system cli auth
```

### Individual Test Files

```bash
# Run individual test files
cd tests
pytest integration/test_system_integration.py -v
pytest integration/test_cli_integration.py -v
pytest integration/test_auth_integration.py -v
pytest integration/test_data_pipeline_integration.py -v
pytest integration/test_end_to_end_validation.py -v
```

## Test Suites Description

### 1. System Integration Tests (`test_system_integration.py`)

Tests the complete system integration workflow:

- **Complete Pipeline**: Sources → Scraping → NLP → Database → API
- **Data Consistency**: Cross-component data validation
- **Error Resilience**: System behavior under error conditions
- **Performance Under Load**: Large dataset handling
- **Concurrent Operations**: Multi-user scenarios

**Key Tests:**
- `test_complete_news_processing_pipeline()` - Full data flow validation
- `test_data_consistency_across_system()` - Cross-endpoint consistency
- `test_error_resilience_across_system()` - Error handling validation
- `test_performance_under_load()` - Performance with 50+ articles
- `test_concurrent_operations()` - Concurrent API requests

### 2. CLI Integration Tests (`test_cli_integration.py`)

Tests command-line interface functionality:

- **CLI Execution**: Command validation and execution
- **Database Integration**: CLI database operations
- **Error Handling**: Graceful failure scenarios
- **Output Formats**: JSON, table, verbose modes
- **Concurrent Execution**: Multiple CLI processes

**Key Tests:**
- `test_cli_help_commands()` - Help system validation
- `test_cli_status_command()` - Status reporting functionality
- `test_cli_backup_functionality()` - Backup operations
- `test_cli_error_handling()` - Error scenario handling
- `test_cli_concurrent_execution()` - Multi-process execution

### 3. Authentication Integration Tests (`test_auth_integration.py`)

Tests the authentication and authorization system:

- **JWT Lifecycle**: Token creation, validation, expiration
- **Role Management**: Role assignment and permission checking
- **API Integration**: Authentication with API endpoints
- **Security Features**: Token tampering, expiration handling
- **Concurrent Auth**: Multi-user authentication scenarios

**Key Tests:**
- `test_jwt_token_lifecycle()` - Complete JWT workflow
- `test_role_manager_integration()` - RBAC system validation
- `test_api_authentication_integration()` - API auth integration
- `test_role_assignment_workflow()` - Role management workflow
- `test_token_security_features()` - Security validation

### 4. Data Pipeline Integration Tests (`test_data_pipeline_integration.py`)

Tests the complete data processing pipeline:

- **Pipeline Workflow**: Source → Article → NLP → Storage
- **Error Handling**: Malformed data processing
- **Performance Scalability**: Large dataset processing
- **Concurrent Operations**: Parallel data processing
- **Data Consistency**: Pipeline stage validation

**Key Tests:**
- `test_complete_data_pipeline_workflow()` - Full pipeline validation
- `test_data_pipeline_error_handling()` - Error resilience testing
- `test_data_pipeline_performance_scalability()` - Performance testing
- `test_data_pipeline_concurrent_operations()` - Concurrency testing
- `test_data_consistency_across_pipeline_stages()` - Consistency validation

### 5. End-to-End Validation Tests (`test_end_to_end_validation.py`)

Comprehensive system validation tests:

- **Complete System Workflows**: Real-world usage scenarios
- **Performance Benchmarks**: System performance validation
- **Error Recovery**: System resilience testing
- **Data Integrity**: Comprehensive data validation
- **API Documentation**: Schema and documentation validation

**Key Tests:**
- `test_complete_system_workflow_validation()` - Full system validation
- `test_system_performance_under_load()` - Performance benchmarking
- `test_system_error_recovery_and_resilience()` - Error recovery testing
- `test_data_integrity_and_validation()` - Data integrity validation
- `test_api_documentation_and_schema_validation()` - Documentation validation

## Test Configuration

### Environment Variables

```bash
# Required
DATABASE_URL=postgresql://preventia:preventia123@localhost:5433/preventia_news
TEST_DATABASE_URL=postgresql://preventia:preventia123@localhost:5433/preventia_test

# Optional
JWT_SECRET_KEY=test-secret-key-for-integration-testing
API_HOST=localhost
API_PORT=8000
```

### Test Database Setup

```bash
# Create test database
createdb -h localhost -p 5433 -U preventia preventia_test

# Or use Docker
docker compose exec postgres createdb -U preventia preventia_test
```

### Pytest Configuration

The tests use custom pytest markers:

- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.slow` - Long-running tests (>10s)
- `@pytest.mark.database` - Tests requiring database
- `@pytest.mark.performance` - Performance benchmarks

```bash
# Run only integration tests
pytest -m integration

# Run only e2e tests
pytest -m e2e

# Run fast tests only
pytest -m "not slow"

# Run database tests
pytest -m database
```

## Performance Benchmarks

The integration tests include performance benchmarks:

### API Response Time Benchmarks
- Health check: < 1.0s
- Articles listing: < 5.0s
- Analytics endpoints: < 10.0s
- Documentation: < 3.0s

### Data Processing Benchmarks
- 100 articles processing: < 30s
- Database operations: < 5s per operation
- NLP analysis: ~2 articles/second
- Concurrent requests: 90%+ success rate

### Scalability Tests
- 50 sources, 200 articles: < 45s total processing
- 20 concurrent API requests: < 5s average response
- Large dataset analytics: < 15s for dashboard loading

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check PostgreSQL is running
   docker compose ps postgres

   # Check database exists
   docker compose exec postgres psql -U preventia -l
   ```

2. **Import Errors**
   ```bash
   # Ensure dependencies installed
   pip install -r requirements.txt
   pip install -r tests/requirements-test.txt

   # Check Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

3. **Tests Timeout**
   ```bash
   # Increase timeout for slow systems
   pytest --timeout=300 integration/

   # Run specific slow tests individually
   pytest integration/test_end_to_end_validation.py::TestEndToEndSystemValidation::test_complete_system_workflow_validation -s
   ```

4. **CLI Tests Fail**
   ```bash
   # Ensure CLI is built
   python setup_cli.py

   # Check CLI executable exists
   ls -la preventia-cli
   ```

### Debug Mode

```bash
# Run with debug output
pytest integration/ -v -s --tb=long

# Run single test with debug
pytest integration/test_system_integration.py::TestCompleteSystemIntegration::test_complete_news_processing_pipeline -v -s

# Enable SQL logging
export DATABASE_ECHO=true
```

### Test Data Cleanup

```bash
# Manual cleanup
docker compose exec postgres psql -U preventia -d preventia_test -c "
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
"

# Or recreate test database
docker compose exec postgres dropdb -U preventia preventia_test
docker compose exec postgres createdb -U preventia preventia_test
```

## Contributing

### Adding New Integration Tests

1. **Choose appropriate test file** based on functionality
2. **Follow existing patterns** for async tests and fixtures
3. **Use descriptive test names** indicating what is being validated
4. **Add proper markers** (`@pytest.mark.integration`, etc.)
5. **Include cleanup** in fixtures to avoid test interference

### Test Writing Guidelines

```python
@pytest.mark.integration
@pytest.mark.database
@pytest.mark.asyncio
async def test_new_integration_feature(clean_test_environment):
    """Test description explaining what is being validated"""

    # Setup phase
    async with clean_test_environment.get_session() as session:
        # Create test data
        pass

    # Action phase
    # Perform the operation being tested

    # Validation phase
    # Assert expected outcomes
    assert condition, "Descriptive error message"
```

### Performance Test Guidelines

- Set realistic performance targets
- Test with representative data sizes
- Include concurrent operation tests
- Validate both success rate and response times
- Use appropriate timeouts for slow operations

## Continuous Integration

### GitHub Actions Integration

```yaml
name: Integration Tests
on: [push, pull_request]
jobs:
  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: preventia123
          POSTGRES_USER: preventia
          POSTGRES_DB: preventia_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r tests/requirements-test.txt
      - name: Run integration tests
        run: python tests/run_integration_tests.py --report integration-report.md
        env:
          TEST_DATABASE_URL: postgresql://preventia:preventia123@localhost:5432/preventia_test
      - name: Upload test report
        uses: actions/upload-artifact@v3
        with:
          name: integration-test-report
          path: integration-report.md
```

## Monitoring and Alerting

### Test Metrics to Monitor

- **Pass Rate**: Should maintain >95%
- **Execution Time**: Monitor for performance regressions
- **Coverage**: Integration test coverage of new features
- **Failure Patterns**: Identify recurring failure points

### Alerting Thresholds

- Pass rate drops below 90%
- Average test execution time increases >20%
- Any test suite times out consistently
- Database connection failures

---

For more information, see the main project documentation in `docs/README.md` or contact the development team.
