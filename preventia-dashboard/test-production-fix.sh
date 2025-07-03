#!/bin/bash

echo "🔧 Testing Production Docker Fix - CORS Resolution..."

# Clean up previous test
docker stop test-prod-frontend 2>/dev/null || true
docker rm test-prod-frontend 2>/dev/null || true

# Build optimized version
echo "📦 Building optimized production bundle..."
npm run build

# Check build success
if [ ! -d "dist" ]; then
    echo "❌ Build failed - dist directory not found"
    exit 1
fi

# Build Docker image
echo "🐳 Building production Docker image..."
docker build -f Dockerfile -t preventia-dashboard-prod . --quiet

# Run with host networking for API access
echo "🚀 Starting production container..."
docker run -d --name test-prod-frontend \
  --add-host=host.docker.internal:host-gateway \
  -p 3001:80 \
  preventia-dashboard-prod

# Wait for container to start
sleep 5

# Test connectivity
echo "🔍 Testing connectivity..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001)
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/api/health)

echo "Frontend (3001): $FRONTEND_STATUS"
echo "API Proxy (/api/health): $API_STATUS"

if [ "$FRONTEND_STATUS" = "200" ] && [ "$API_STATUS" = "200" ]; then
    echo "✅ Production container ready on http://localhost:3001"
    echo ""
    echo "🔗 CORS Fix Applied:"
    echo "   - Frontend uses relative URL: /api/"
    echo "   - Nginx proxies to host.docker.internal:8000"
    echo "   - No direct cross-origin requests"
    echo ""
    echo "📋 Validation steps:"
    echo "1. Open http://localhost:3001"
    echo "2. Console should be CORS-error free"
    echo "3. Network tab shows /api/* calls (not localhost:8000)"
    echo "4. Dashboard data loads successfully"
else
    echo "❌ Container not ready. Check logs:"
    echo "Frontend logs:"
    docker logs test-prod-frontend --tail 10
fi

echo ""
echo "🧹 Cleanup: docker stop test-prod-frontend && docker rm test-prod-frontend"
