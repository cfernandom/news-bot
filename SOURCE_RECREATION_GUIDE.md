# 📋 Source Recreation Guide - Fresh Database Test

## Overview
This guide helps you recreate the 14 existing news sources using only the admin interface, starting from a completely empty database.

## Pre-requisites
✅ Run `./fresh_database_test.sh` first to reset database and backup sources
✅ Services running: `docker-compose ps` (5 healthy services)
✅ Admin panel accessible: http://localhost:5174/admin

## 🔐 Admin Access
- **URL:** http://localhost:5174/admin
- **Login:** admin@preventia.com / admin123

## 📰 Sources to Recreate (14 total)

### 1. Breast Cancer Org ⭐ (Primary Source)
```
Name: Breast Cancer Org
Base URL: https://www.breastcancer.org
Language: en
Country: United States
Robots.txt URL: https://www.breastcancer.org/robots.txt
Terms of Service: https://www.breastcancer.org/about-us/terms-conditions
Legal Contact: info@breastcancer.org
Crawl Delay: 2
Fair Use Basis: Academic research for breast cancer prevention analysis under fair use doctrine
```

### 2. News Medical ⭐ (High Volume)
```
Name: News Medical
Base URL: https://www.news-medical.net
Language: en
Country: International
Robots.txt URL: https://www.news-medical.net/robots.txt
Terms of Service: https://www.news-medical.net/privacy-policy
Legal Contact: info@news-medical.net
Crawl Delay: 2
Fair Use Basis: Academic research for medical content analysis under educational fair use
```

### 3. Medical Xpress ⭐ (Research Focus)
```
Name: Medical Xpress
Base URL: https://medicalxpress.com
Language: en
Country: International
Robots.txt URL: https://medicalxpress.com/robots.txt
Terms of Service: https://medicalxpress.com/help/terms/
Legal Contact: feedback@medicalxpress.com
Crawl Delay: 2
Fair Use Basis: Academic research for medical news analysis under fair use doctrine
```

### 4. Science Daily
```
Name: Science Daily
Base URL: https://www.sciencedaily.com
Language: en
Country: International
Robots.txt URL: https://www.sciencedaily.com/robots.txt
Terms of Service: https://www.sciencedaily.com/terms.htm
Legal Contact: editor@sciencedaily.com
Crawl Delay: 2
Fair Use Basis: Academic research for scientific content analysis under educational use
```

### 5. WebMD
```
Name: WebMD
Base URL: https://www.webmd.com
Language: en
Country: United States
Robots.txt URL: https://www.webmd.com/robots.txt
Terms of Service: https://www.webmd.com/about-webmd-policies/about-terms-and-conditions-of-use
Legal Contact: legal@webmd.net
Crawl Delay: 3
Fair Use Basis: Academic research for health information analysis under fair use doctrine
```

### 6. Nature
```
Name: Nature
Base URL: https://www.nature.com
Language: en
Country: International
Robots.txt URL: https://www.nature.com/robots.txt
Terms of Service: https://www.nature.com/info/terms_conditions.html
Legal Contact: permissions@nature.com
Crawl Delay: 3
Fair Use Basis: Academic research for scientific publication analysis under educational fair use
```

### 7. CureToday
```
Name: CureToday
Base URL: https://www.curetoday.com
Language: en
Country: United States
Robots.txt URL: https://www.curetoday.com/robots.txt
Terms of Service: https://www.curetoday.com/terms-of-use
Legal Contact: info@curetoday.com
Crawl Delay: 2
Fair Use Basis: Academic research for cancer treatment information analysis
```

### 8. Breast Cancer Now (UK)
```
Name: Breast Cancer Now
Base URL: https://breastcancernow.org
Language: en
Country: United Kingdom
Robots.txt URL: https://breastcancernow.org/robots.txt
Terms of Service: https://breastcancernow.org/about-us/website-terms-use
Legal Contact: info@breastcancernow.org
Crawl Delay: 2
Fair Use Basis: Academic research for breast cancer awareness analysis under UK fair dealing
```

### 9. Medical News Today
```
Name: Medical News Today
Base URL: https://www.medicalnewstoday.com
Language: en
Country: US
Robots.txt URL: https://www.medicalnewstoday.com/robots.txt
Terms of Service: https://www.medicalnewstoday.com/terms
Legal Contact: legal@medicalnewstoday.com
Crawl Delay: 2
Fair Use Basis: Academic research for medical news analysis under fair use doctrine
```

### 10. Mayo Clinic News
```
Name: Mayo Clinic News
Base URL: https://newsnetwork.mayoclinic.org
Language: en
Country: US
Robots.txt URL: https://newsnetwork.mayoclinic.org/robots.txt
Terms of Service: https://www.mayoclinic.org/about-this-site/terms-conditions-use-policy
Legal Contact: news@mayoclinic.org
Crawl Delay: 3
Fair Use Basis: Academic research for medical education content analysis
```

### 11. Cleveland Clinic News
```
Name: Cleveland Clinic News
Base URL: https://newsroom.clevelandclinic.org
Language: en
Country: US
Robots.txt URL: https://newsroom.clevelandclinic.org/robots.txt
Terms of Service: https://my.clevelandclinic.org/footer/terms-of-use
Legal Contact: media@ccf.org
Crawl Delay: 3
Fair Use Basis: Academic research for medical institution news analysis
```

### 12. BBC Health
```
Name: BBC Health
Base URL: https://www.bbc.com/news/health
Language: en
Country: UK
Robots.txt URL: https://www.bbc.com/robots.txt
Terms of Service: https://www.bbc.com/terms
Legal Contact: legal@bbc.co.uk
Crawl Delay: 3
Fair Use Basis: Academic research for health news analysis under UK fair dealing
```

### 13. La República (Spanish)
```
Name: La República
Base URL: https://www.larepublica.co/cancer-de-seno
Language: es
Country: Colombia
Robots.txt URL: https://www.larepublica.co/robots.txt
Terms of Service: https://www.larepublica.co/aviso-legal
Legal Contact: basesdedatos@larepublica.com.co
Crawl Delay: 2
Fair Use Basis: Investigación académica bajo la Ley Colombiana 1581/2012 y doctrina de uso justo
```

### 14. Harvard Health (Test Source)
```
Name: Harvard Health Publishing
Base URL: https://www.health.harvard.edu
Language: en
Country: US
Robots.txt URL: https://www.health.harvard.edu/robots.txt
Terms of Service: https://www.health.harvard.edu/terms-of-use
Legal Contact: webmaster@harvard.edu
Crawl Delay: 3
Fair Use Basis: Academic research for health education content analysis under educational fair use
```

## 🔄 Recreation Process

### Step-by-Step Instructions:

1. **Open Admin Panel**
   - Navigate to http://localhost:5174/admin
   - Login with admin credentials

2. **For Each Source Above:**
   - Click "Agregar Fuente" button
   - Fill in all fields exactly as specified
   - Click "Validar Compliance" 
   - Wait for validation to complete
   - Save the source

3. **Monitor Progress:**
   - Check source count in dashboard
   - Verify compliance scores are calculated
   - Ensure no validation errors

### ✅ Success Criteria:
- [ ] All 14 sources created successfully
- [ ] Compliance scores between 0.8-1.0
- [ ] No validation errors in admin panel
- [ ] Source list matches original backup
- [ ] Admin dashboard shows 14 active sources

### 🚨 Common Issues:
- **Duplicate URL errors:** Check for typos in base URLs
- **Compliance validation fails:** Verify robots.txt URLs are accessible
- **Missing fields:** Ensure all required fields are filled

### 📊 Post-Recreation Validation:
1. Check dashboard shows 14 sources
2. Verify compliance dashboard shows metrics
3. Test source edit functionality
4. Confirm source deletion workflow (optional)

## 🎯 Next Steps After Recreation:
1. Run manual scrapers to populate articles
2. Test NLP processing on new articles
3. Verify analytics dashboard updates
4. Test export functionality with fresh data

---

**Estimated Time:** 30-45 minutes  
**Difficulty:** Medium  
**Purpose:** Validate complete source administration workflow from scratch