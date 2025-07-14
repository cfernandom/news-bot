#!/bin/bash

echo "🗄️ PreventIA Fresh Database Test Setup"
echo "======================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get current sources for recreation
echo "1️⃣ Backing up current sources..."
echo "================================="

# Get admin token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@preventia.com","password":"admin123"}' | jq -r '.access_token')

if [ "$TOKEN" = "null" ]; then
    echo -e "${RED}❌ Failed to get admin token${NC}"
    exit 1
fi

# Backup current sources
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/sources/" > sources_backup.json
SOURCE_COUNT=$(cat sources_backup.json | jq '. | length')
echo -e "${GREEN}✅ Backed up $SOURCE_COUNT sources to sources_backup.json${NC}"

# Display current sources
echo ""
echo -e "${BLUE}📋 Current Sources to Recreate:${NC}"
cat sources_backup.json | jq -r '.[] | "  • \(.name) - \(.base_url)"'

echo ""
echo -e "${YELLOW}⚠️  WARNING: This will DELETE ALL data in the database!${NC}"
echo "   - All articles will be lost"
echo "   - All sources will be removed"  
echo "   - Analytics data will be reset"
echo ""
read -p "Are you sure you want to proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Operation cancelled"
    exit 1
fi

echo ""
echo "2️⃣ Resetting Database..."
echo "========================="

# Stop services
echo "Stopping services..."
docker-compose stop

# Remove database volume to completely reset
echo "Removing database volume..."
docker volume rm news_bot_3_postgres_data 2>/dev/null || true

# Restart services (will recreate database)
echo "Starting services with fresh database..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to initialize..."
sleep 30

# Check health
echo "Checking system health..."
for i in {1..12}; do
    HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null | jq -r '.status' 2>/dev/null)
    if [ "$HEALTH" = "healthy" ]; then
        echo -e "${GREEN}✅ System is healthy${NC}"
        break
    fi
    echo "Waiting for system to be ready... ($i/12)"
    sleep 5
done

# Verify empty database
ARTICLES=$(curl -s http://localhost:8000/health | jq -r '.articles_count')
echo -e "${GREEN}✅ Fresh database ready (Articles: $ARTICLES)${NC}"

echo ""
echo "3️⃣ Manual Recreation Instructions"
echo "=================================="
echo ""
echo -e "${BLUE}📋 Next Steps - Use Admin Interface:${NC}"
echo ""
echo "1. Open Admin Panel: http://localhost:5174/admin"
echo "2. Login with: admin@preventia.com / admin123"
echo "3. Recreate these sources one by one:"
echo ""

# Generate source creation instructions
cat sources_backup.json | jq -r '.[] | 
"   📰 \(.name)
   URL: \(.base_url)
   Language: \(.language)
   Country: \(.country)
   Robots.txt: \(.robots_txt_url // "https://\(.base_url | gsub("https://"; "") | gsub("http://"; ""))/robots.txt")
   Terms: \(.terms_of_service_url // "https://\(.base_url | gsub("https://"; "") | gsub("http://"; ""))/terms")
   Contact: \(.legal_contact_email // "legal@\(.base_url | gsub("https://"; "") | gsub("http://"; "") | gsub("www."; ""))")
   Crawl Delay: \(.crawl_delay_seconds)
   Fair Use: \(.fair_use_basis // "Academic research for breast cancer prevention analysis under fair use doctrine")
   "'

echo ""
echo "4️⃣ Validation After Recreation"
echo "==============================="
echo ""
echo "After recreating all sources:"
echo "• Check source count matches: $SOURCE_COUNT sources"
echo "• Verify compliance scores are calculated"
echo "• Test source validation workflow"
echo "• Run scrapers to populate articles"
echo ""

echo "💾 Files created:"
echo "  - sources_backup.json (backup of original sources)"
echo ""
echo -e "${GREEN}✅ Database reset complete - Ready for manual source recreation!${NC}"
echo ""
echo "🔗 Quick Links:"
echo "   • Admin Panel: http://localhost:5174/admin"
echo "   • API Health: http://localhost:8000/health"
echo "   • Dashboard: http://localhost:5174/"