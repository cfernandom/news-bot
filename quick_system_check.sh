#!/bin/bash

echo "🔍 PreventIA Quick System Check"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check status
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        return 0
    else
        echo -e "${RED}❌ $2${NC}"
        return 1
    fi
}

# 1. Check Docker Services
echo "1️⃣ Checking Docker Services..."
HEALTHY_COUNT=$(docker-compose ps | grep -c "healthy")
RUNNING_COUNT=$(docker-compose ps | grep -c "Up")
if [ "$RUNNING_COUNT" -ge 5 ]; then
    echo -e "${GREEN}✅ Docker: $RUNNING_COUNT services running ($HEALTHY_COUNT healthy)${NC}"
else
    echo -e "${RED}❌ Docker: Only $RUNNING_COUNT/5 services running${NC}"
fi

# 2. Check API Health
echo ""
echo "2️⃣ Checking API Health..."
API_RESPONSE=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    ARTICLES=$(echo $API_RESPONSE | jq -r '.articles_count')
    STATUS=$(echo $API_RESPONSE | jq -r '.status')
    echo -e "${GREEN}✅ API Status: $STATUS (Articles: $ARTICLES)${NC}"
else
    echo -e "${RED}❌ API not responding${NC}"
fi

# 3. Check Frontend
echo ""
echo "3️⃣ Checking Frontend..."
FRONTEND_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5174)
if [ "$FRONTEND_CHECK" = "200" ]; then
    echo -e "${GREEN}✅ Frontend accessible at http://localhost:5174${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend not running on 5174 (run: npm run dev)${NC}"
fi

# 4. Test Authentication
echo ""
echo "4️⃣ Testing Authentication..."
AUTH_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@preventia.com","password":"admin123"}')
  
if echo $AUTH_RESPONSE | grep -q "access_token"; then
    echo -e "${GREEN}✅ Admin authentication working${NC}"
    TOKEN=$(echo $AUTH_RESPONSE | jq -r '.access_token')
else
    echo -e "${RED}❌ Authentication failed${NC}"
fi

# 5. Check Key Endpoints
echo ""
echo "5️⃣ Testing Key Endpoints..."

# Analytics endpoints
ENDPOINTS=(
    "http://localhost:8000/api/v1/stats/topics"
    "http://localhost:8000/api/v1/stats/tones"
    "http://localhost:8000/api/v1/stats/geo"
)

for endpoint in "${ENDPOINTS[@]}"; do
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" $endpoint)
    if [ "$STATUS_CODE" = "200" ]; then
        echo -e "${GREEN}✅ ${endpoint##*/} endpoint OK${NC}"
    else
        echo -e "${RED}❌ ${endpoint##*/} endpoint failed (HTTP $STATUS_CODE)${NC}"
    fi
done

# 6. Check Export Functionality
echo ""
echo "6️⃣ Testing Export System..."
CSV_CHECK=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/api/v1/export/news.csv?page_size=1")
if [ "$CSV_CHECK" = "200" ]; then
    echo -e "${GREEN}✅ CSV export working${NC}"
else
    echo -e "${RED}❌ CSV export failed${NC}"
fi

# 7. Database Check
echo ""
echo "7️⃣ Checking Database..."
DB_CHECK=$(docker-compose exec -T postgres psql -U preventia -d preventia_news -c "SELECT COUNT(*) FROM articles;" 2>/dev/null | grep -o '[0-9]\+' | head -1)
if [ ! -z "$DB_CHECK" ]; then
    echo -e "${GREEN}✅ Database accessible (Articles: $DB_CHECK)${NC}"
else
    echo -e "${RED}❌ Database connection failed${NC}"
fi

# Summary
echo ""
echo "📊 SYSTEM CHECK SUMMARY"
echo "======================="

# URLs for manual testing
echo ""
echo "🔗 Key URLs for Manual Testing:"
echo "   • Legacy Dashboard: http://localhost:5174/"
echo "   • Admin Panel: http://localhost:5174/admin"
echo "   • API Health: http://localhost:8000/health"
echo "   • API Docs: http://localhost:8000/docs"
echo ""
echo "👤 Test Accounts:"
echo "   • Admin: admin@preventia.com / admin123"
echo "   • Demo: demo@preventia.com / demo123"
echo ""

# Quick health assessment
ISSUES=0
[ "$RUNNING_COUNT" -lt 5 ] && ((ISSUES++))
[ "$FRONTEND_CHECK" != "200" ] && ((ISSUES++))
[ -z "$TOKEN" ] && ((ISSUES++))

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ SYSTEM STATUS: All components operational!${NC}"
    echo "   Ready for manual testing following MANUAL_TESTING_CHECKLIST.md"
else
    echo -e "${YELLOW}⚠️  SYSTEM STATUS: $ISSUES components need attention${NC}"
    echo "   Fix issues before proceeding with manual testing"
fi

echo ""
echo "📋 Next step: Follow MANUAL_TESTING_CHECKLIST.md for comprehensive testing"