#!/bin/bash

# Production Testing Script for PreventIA News Analytics
# Comprehensive testing suite for production deployment validation

set -e

echo "🚀 Starting Production Testing Suite for PreventIA News Analytics"
echo "=================================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="$PROJECT_ROOT/venv"
DASHBOARD_PATH="$PROJECT_ROOT/preventia-dashboard"
API_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:5173"

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print status
print_status() {
    case $1 in
        "PASS")
            echo -e "${GREEN}✅ PASS${NC}: $2"
            ((PASSED_TESTS++))
            ;;
        "FAIL")
            echo -e "${RED}❌ FAIL${NC}: $2"
            ((FAILED_TESTS++))
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  INFO${NC}: $2"
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  WARN${NC}: $2"
            ;;
    esac
    ((TOTAL_TESTS++))
}

# Function to run command with timeout
run_with_timeout() {
    timeout 30 "$@"
}

# Function to check if service is running
check_service() {
    local service_name=$1
    local url=$2
    local expected_status=${3:-200}

    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "$expected_status"; then
        print_status "PASS" "$service_name is running and responding"
        return 0
    else
        print_status "FAIL" "$service_name is not responding correctly"
        return 1
    fi
}

# Pre-flight checks
echo -e "\n${BLUE}📋 Pre-flight Checks${NC}"
echo "===================="

# Check if virtual environment exists
if [ -d "$VENV_PATH" ]; then
    print_status "PASS" "Python virtual environment found"
else
    print_status "FAIL" "Python virtual environment not found at $VENV_PATH"
    exit 1
fi

# Check if Node.js dependencies are installed
if [ -d "$DASHBOARD_PATH/node_modules" ]; then
    print_status "PASS" "Node.js dependencies installed"
else
    print_status "FAIL" "Node.js dependencies not installed"
    exit 1
fi

# Check if Docker is running
if docker info >/dev/null 2>&1; then
    print_status "PASS" "Docker is running"
else
    print_status "FAIL" "Docker is not running"
    exit 1
fi

# Environment setup
echo -e "\n${BLUE}🔧 Environment Setup${NC}"
echo "===================="

# Activate virtual environment
source "$VENV_PATH/bin/activate"
print_status "PASS" "Python virtual environment activated"

# Install test dependencies
pip install -q pytest pytest-asyncio pytest-cov httpx
print_status "PASS" "Test dependencies installed"

# Database tests
echo -e "\n${BLUE}🗄️  Database Tests${NC}"
echo "=================="

# Check database connection
if python -c "
import asyncio
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from services.data.database.connection import DatabaseManager

async def test_db():
    try:
        db = DatabaseManager()
        await db.initialize()
        health = await db.health_check()
        return health
    except Exception as e:
        print(f'Error: {e}')
        return False

result = asyncio.run(test_db())
sys.exit(0 if result else 1)
"; then
    print_status "PASS" "Database connection successful"
else
    print_status "FAIL" "Database connection failed"
fi

# Run database tests
cd "$PROJECT_ROOT/tests"
if pytest -m database --tb=short -q; then
    print_status "PASS" "Database unit tests"
else
    print_status "FAIL" "Database unit tests"
fi

# API tests
echo -e "\n${BLUE}🔌 API Tests${NC}"
echo "============"

# Start API server in background if not running
if ! check_service "API Server" "$API_URL/health" 200; then
    print_status "INFO" "Starting API server for testing..."
    cd "$PROJECT_ROOT"
    python -m services.api.main &
    API_PID=$!
    sleep 10

    if check_service "API Server" "$API_URL/health" 200; then
        print_status "PASS" "API server started successfully"
    else
        print_status "FAIL" "Failed to start API server"
        kill $API_PID 2>/dev/null || true
        exit 1
    fi
else
    API_PID=""
fi

# Run API unit tests
cd "$PROJECT_ROOT/tests"
if pytest unit/test_api/ --tb=short -q; then
    print_status "PASS" "API unit tests"
else
    print_status "FAIL" "API unit tests"
fi

# Run API integration tests
if pytest integration/test_api/ --tb=short -q; then
    print_status "PASS" "API integration tests"
else
    print_status "FAIL" "API integration tests"
fi

# Performance tests
if pytest performance/ --tb=short -q; then
    print_status "PASS" "API performance tests"
else
    print_status "FAIL" "API performance tests"
fi

# Test API endpoints
endpoints=(
    "/health"
    "/api/v1/articles/"
    "/api/v1/analytics/sentiment"
    "/api/v1/analytics/topics"
    "/api/v1/news"
    "/docs"
)

for endpoint in "${endpoints[@]}"; do
    if check_service "Endpoint $endpoint" "$API_URL$endpoint" 200; then
        print_status "PASS" "API endpoint $endpoint"
    else
        print_status "FAIL" "API endpoint $endpoint"
    fi
done

# Frontend tests
echo -e "\n${BLUE}🖥️  Frontend Tests${NC}"
echo "=================="

cd "$DASHBOARD_PATH"

# Run unit tests
if npm run test:unit -- --run; then
    print_status "PASS" "Frontend unit tests"
else
    print_status "FAIL" "Frontend unit tests"
fi

# Build test
if npm run build; then
    print_status "PASS" "Frontend build"
else
    print_status "FAIL" "Frontend build"
fi

# Start development server for E2E tests
if ! check_service "Frontend Server" "$FRONTEND_URL" 200; then
    print_status "INFO" "Starting frontend server for E2E testing..."
    npm run dev &
    FRONTEND_PID=$!
    sleep 15

    if check_service "Frontend Server" "$FRONTEND_URL" 200; then
        print_status "PASS" "Frontend server started successfully"
    else
        print_status "FAIL" "Failed to start frontend server"
        kill $FRONTEND_PID 2>/dev/null || true
    fi
else
    FRONTEND_PID=""
fi

# Run E2E tests
if [ -f "tests/e2e/comprehensive-e2e.test.js" ]; then
    if npx vitest run tests/e2e/comprehensive-e2e.test.js; then
        print_status "PASS" "Frontend E2E tests"
    else
        print_status "FAIL" "Frontend E2E tests"
    fi
fi

# NLP tests
echo -e "\n${BLUE}🧠 NLP Tests${NC}"
echo "============"

cd "$PROJECT_ROOT/tests"

# Run NLP unit tests
if pytest unit/test_nlp/ --tb=short -q; then
    print_status "PASS" "NLP unit tests"
else
    print_status "FAIL" "NLP unit tests"
fi

# Run NLP integration tests
if pytest integration/test_nlp_pipeline.py --tb=short -q; then
    print_status "PASS" "NLP integration tests"
else
    print_status "FAIL" "NLP integration tests"
fi

# Docker tests
echo -e "\n${BLUE}🐳 Docker Tests${NC}"
echo "==============="

# Test Docker builds
if docker build -t preventia-api-test -f "$PROJECT_ROOT/Dockerfile.api" "$PROJECT_ROOT" >/dev/null 2>&1; then
    print_status "PASS" "API Docker build"
    docker rmi preventia-api-test >/dev/null 2>&1
else
    print_status "FAIL" "API Docker build"
fi

if docker build -t preventia-frontend-test -f "$DASHBOARD_PATH/Dockerfile" "$DASHBOARD_PATH" >/dev/null 2>&1; then
    print_status "PASS" "Frontend Docker build"
    docker rmi preventia-frontend-test >/dev/null 2>&1
else
    print_status "FAIL" "Frontend Docker build"
fi

# Security tests
echo -e "\n${BLUE}🔒 Security Tests${NC}"
echo "================="

# Check for environment file with secrets
if [ -f "$PROJECT_ROOT/.env" ]; then
    if grep -q "CHANGE_THIS" "$PROJECT_ROOT/.env"; then
        print_status "WARN" "Default secrets found in .env file"
    else
        print_status "PASS" "No default secrets in .env file"
    fi
fi

# Check API security headers
security_headers=("X-Frame-Options" "X-Content-Type-Options" "X-XSS-Protection")
for header in "${security_headers[@]}"; do
    if curl -s -I "$API_URL/health" | grep -q "$header"; then
        print_status "PASS" "Security header: $header"
    else
        print_status "WARN" "Missing security header: $header"
    fi
done

# Load tests
echo -e "\n${BLUE}⚡ Load Tests${NC}"
echo "============"

# Simple load test with curl
load_test_url="$API_URL/health"
load_requests=50
concurrent_requests=10

print_status "INFO" "Running load test: $load_requests requests with $concurrent_requests concurrent"

if command -v ab >/dev/null 2>&1; then
    if ab -n $load_requests -c $concurrent_requests "$load_test_url" >/dev/null 2>&1; then
        print_status "PASS" "Load test completed successfully"
    else
        print_status "FAIL" "Load test failed"
    fi
else
    print_status "WARN" "Apache Bench (ab) not available for load testing"
fi

# Cleanup
echo -e "\n${BLUE}🧹 Cleanup${NC}"
echo "=========="

# Kill background processes
if [ -n "$API_PID" ]; then
    kill $API_PID 2>/dev/null || true
    print_status "INFO" "API server stopped"
fi

if [ -n "$FRONTEND_PID" ]; then
    kill $FRONTEND_PID 2>/dev/null || true
    print_status "INFO" "Frontend server stopped"
fi

# Test summary
echo -e "\n${BLUE}📊 Test Summary${NC}"
echo "==============="

echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ALL TESTS PASSED! System is ready for production.${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Please review and fix issues before production deployment.${NC}"
    exit 1
fi
