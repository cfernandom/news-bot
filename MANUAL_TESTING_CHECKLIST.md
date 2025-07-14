# 🧪 MANUAL TESTING CHECKLIST - PreventIA News Analytics

## 📋 Pre-requisitos
- [ ] Docker services running: `docker-compose ps` (5 services healthy)
- [ ] Frontend dev server: `cd preventia-dashboard && npm run dev`
- [ ] API health check: `curl http://localhost:8000/health` (should show 121 articles)

## 1️⃣ AUTHENTICATION & AUTHORIZATION

### Admin User Testing
- [ ] Navigate to http://localhost:5174/login
- [ ] Login with: `admin@preventia.com` / `admin123`
- [ ] Verify redirect to dashboard after successful login
- [ ] Check user menu shows "System Administrator" role
- [ ] Verify access to Admin Panel button in header

### Demo User Testing  
- [ ] Logout from admin account
- [ ] Login with: `demo@preventia.com` / `demo123`
- [ ] Verify limited permissions (read-only access)
- [ ] Check Admin Panel shows limited functionality
- [ ] Verify cannot create/edit/delete sources

### Session Management
- [ ] Test logout functionality
- [ ] Verify session persists on page refresh
- [ ] Check unauthorized access redirects to login

## 2️⃣ LEGACY DASHBOARD (http://localhost:5174/)

### Dashboard Overview
- [ ] Verify 4 KPI cards show:
  - [ ] Noticias Recolectadas: 121
  - [ ] Idioma Dominante: EN (99%)
  - [ ] País Más Activo: US
  - [ ] Medio Más Frecuente: (source name)

### Analytics Charts
- [ ] **Language Distribution Chart**: Shows EN/ES breakdown
- [ ] **Daily Articles Chart**: Shows 14-day trend
- [ ] **Topic Distribution**: Verify 10 medical categories
- [ ] **Sentiment Analysis**: Check positive/negative/neutral distribution
- [ ] **Geographic Map**: Verify US (65), UK (14+) article distribution
- [ ] **News Table**: Browse recent articles with pagination

### Export Functionality
- [ ] Click "Exportar Datos" button
- [ ] Test CSV export - verify file downloads
- [ ] Test Excel export - verify .xlsx file
- [ ] Test PDF export - verify report generation
- [ ] Check exported data matches dashboard numbers

## 3️⃣ ADMIN PANEL (http://localhost:5174/admin)

### Source Management
- [ ] Navigate to Admin Panel (requires admin login)
- [ ] Verify 14 sources listed with compliance scores
- [ ] Check source details:
  - [ ] Name, URL, Country, Language
  - [ ] Compliance score (0.8-1.0)
  - [ ] Last validation date
  - [ ] Active/Inactive status

### Source CRUD Operations
- [ ] Click "Agregar Fuente" to open modal
- [ ] Fill test source data:
  ```
  Name: Test Medical News
  URL: https://test-medical.example.com
  Country: US
  Language: en
  Robots.txt: https://test-medical.example.com/robots.txt
  Terms URL: https://test-medical.example.com/terms
  Contact: legal@test-medical.example.com
  Crawl Delay: 3
  Fair Use: Academic research for medical analysis
  ```
- [ ] Verify compliance validation runs
- [ ] Check error handling for duplicate URLs
- [ ] Test edit functionality on existing source
- [ ] Verify delete confirmation dialog

### Compliance Monitoring
- [ ] Check compliance dashboard shows:
  - [ ] Total sources: 14
  - [ ] Average compliance: ~0.9
  - [ ] Compliance distribution chart
  - [ ] Recent validation logs

## 4️⃣ API ENDPOINTS TESTING

### Public Analytics APIs
```bash
# Test these endpoints (no auth required):
curl http://localhost:8000/api/v1/stats/topics
curl http://localhost:8000/api/v1/stats/tones  
curl http://localhost:8000/api/v1/stats/geo
curl http://localhost:8000/api/v1/analytics/language-distribution
```

### Protected APIs (requires token)
```bash
# Get token first:
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@preventia.com","password":"admin123"}' | jq -r '.access_token')

# Test protected endpoints:
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/sources/
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/users/me
```

### Export APIs
```bash
# Test export endpoints:
curl "http://localhost:8000/api/v1/export/news.csv?page_size=10" -o test.csv
curl "http://localhost:8000/api/v1/export/news.xlsx?page_size=10" -o test.xlsx
curl "http://localhost:8000/api/v1/export/charts/sentiment.png" -o sentiment.png
```

## 5️⃣ MOBILE RESPONSIVENESS

### Tablet View (768px)
- [ ] Open Chrome DevTools → Toggle device toolbar
- [ ] Set viewport to iPad (768x1024)
- [ ] Verify:
  - [ ] Navigation collapses to hamburger menu
  - [ ] Charts stack vertically
  - [ ] Tables are scrollable
  - [ ] Export modal fits screen

### Mobile View (375px)
- [ ] Set viewport to iPhone SE (375x667)
- [ ] Check:
  - [ ] All text is readable
  - [ ] Buttons are touch-friendly
  - [ ] Charts resize properly
  - [ ] No horizontal scrolling

## 6️⃣ PERFORMANCE TESTING

### Page Load Times
- [ ] Open Network tab in DevTools
- [ ] Hard refresh (Ctrl+Shift+R)
- [ ] Verify initial load < 3 seconds
- [ ] Check API responses < 100ms

### Chart Interactions
- [ ] Test chart hover tooltips
- [ ] Verify smooth animations
- [ ] Check no lag when switching views

## 7️⃣ DATA INTEGRITY

### Cross-Reference Checks
- [ ] Dashboard shows 121 total articles
- [ ] Topic sum equals total articles
- [ ] Sentiment distribution adds to 100%
- [ ] Geographic totals match article count
- [ ] Export data matches displayed data

### Filter Testing (if implemented)
- [ ] Apply date range filters
- [ ] Test topic filters
- [ ] Verify filtered counts update
- [ ] Check "clear filters" functionality

## 8️⃣ ERROR HANDLING

### Network Errors
- [ ] Stop backend: `docker-compose stop api`
- [ ] Try to load dashboard - should show error message
- [ ] Restart backend: `docker-compose start api`
- [ ] Verify auto-recovery

### Invalid Inputs
- [ ] Try login with wrong credentials
- [ ] Submit empty source form
- [ ] Enter invalid URLs
- [ ] Test SQL injection in search (should be safe)

## 9️⃣ BROWSER COMPATIBILITY

Test on multiple browsers:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (if on Mac)
- [ ] Edge (latest)

## 🔟 ACCESSIBILITY

### Keyboard Navigation
- [ ] Tab through all interactive elements
- [ ] Enter/Space activate buttons
- [ ] Escape closes modals
- [ ] Focus indicators visible

### Screen Reader (optional)
- [ ] Enable screen reader
- [ ] Verify main navigation readable
- [ ] Check chart descriptions
- [ ] Test form labels

## ✅ ACCEPTANCE CRITERIA

The system passes manual testing if:
- [ ] All authentication flows work correctly
- [ ] Dashboard displays accurate real-time data
- [ ] Export functionality produces valid files
- [ ] Admin panel allows full source management
- [ ] Mobile responsive design works on all devices
- [ ] Performance meets <3s load time requirement
- [ ] No critical errors in any workflow
- [ ] Data integrity maintained across all views

## 📝 ISSUES LOG

Document any issues found:

| Test Case | Issue Description | Severity | Status |
|-----------|------------------|----------|---------|
| Example   | Login timeout    | Medium   | Open    |

---

**Testing Date:** _______________  
**Tested By:** _________________  
**Environment:** Local Development  
**Result:** ⬜ PASS / ⬜ FAIL

## 🚀 POST-TESTING ACTIONS

1. Document all issues found
2. Create GitHub issues for bugs
3. Update documentation if needed
4. Plan fixes for critical issues
5. Re-test after fixes applied