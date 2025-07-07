# Scraping Strategy for New Sources - Implementation Plan

**Date:** 2025-07-04
**Version:** 1.0
**Status:** Planning Phase
**Estimated Duration:** 6-10 development sessions

## 🎯 Executive Summary

This document outlines the comprehensive strategy for implementing scalable scraping capabilities for new news sources in the PreventIA News Analytics system. The approach builds on the existing solid foundation of 4 operational scrapers and focuses on **compliance-first automation** while maintaining the current **100% legal compliance rate**.

## 📊 Current System Analysis

### ✅ Existing Strengths
- **4 Operational Scrapers**: 106 articles, 0% duplicates, 100% integrity
- **Registry Pattern**: Automatic domain-to-extractor matching
- **Compliance Framework**: Complete robots.txt validation and rate limiting
- **PostgreSQL Integration**: Analytics-ready data models
- **Playwright Integration**: Support for complex JavaScript sites
- **Testing Framework**: Automated validation with 95% automation coverage

### 🏗️ Current Architecture
```
External Sources → Compliance Validation → Scrapers →
Full-text Extraction → PostgreSQL Storage →
NLP Analysis → Analytics Dashboard
```

### 📋 Operational Scrapers Status
| Scraper | Status | Articles | Performance | Technology |
|---------|--------|----------|-------------|------------|
| Breast Cancer Org | ✅ Operational | 25 | ~2.5s | Playwright + PostgreSQL |
| WebMD | ✅ Operational | 31 | ~45s | Playwright + Date Parsing |
| CureToday | ✅ Operational | 30 | ~50s | Playwright + Duplicate Detection |
| News Medical | ✅ Operational | 20 | ~30s | Playwright + International Metadata |

## 🚀 Scalability Strategy

### **Phase 1: Semi-Automated Integration (2-3 sessions)**

#### 1.1 ScraperGenerator Implementation
```python
# services/scraper/automation/scraper_generator.py
class ScraperGenerator:
    """Automated scraper generation with compliance-first approach"""

    def __init__(self):
        self.compliance_validator = ComplianceValidator()
        self.structure_analyzer = SiteStructureAnalyzer()
        self.template_engine = ScraperTemplateEngine()
        self.testing_framework = AutomatedTestingFramework()

    async def generate_scraper_for_domain(self, domain: str, source_config: dict) -> ScraperResult:
        """Complete pipeline for new source integration"""
        # 1. MANDATORY: Compliance validation
        compliance_result = await self.compliance_validator.validate_source(domain)
        if not compliance_result.is_compliant:
            raise ComplianceViolationError(compliance_result.violations)

        # 2. Site structure analysis
        structure = await self.structure_analyzer.analyze_site(domain)

        # 3. Template-based scraper generation
        scraper_code = await self.template_engine.generate_scraper(structure)

        # 4. Automated testing
        test_results = await self.testing_framework.run_full_test_suite(scraper_code)

        # 5. Registry integration if tests pass
        if test_results.success_rate >= 0.8:
            await self.integrate_to_registry(domain, scraper_code)

        return ScraperResult(
            domain=domain,
            scraper_code=scraper_code,
            compliance_result=compliance_result,
            test_results=test_results,
            deployment_status="deployed" if test_results.success_rate >= 0.8 else "failed"
        )
```

#### 1.2 Site Structure Analysis
```python
# services/scraper/automation/structure_analyzer.py
class SiteStructureAnalyzer:
    """Analyzes website structure for automated scraper generation"""

    async def analyze_site(self, domain: str) -> SiteStructure:
        """Comprehensive site structure analysis"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Load main page
            await page.goto(f"https://{domain}")

            # Detect CMS type
            cms_type = await self._detect_cms_type(page)

            # Analyze navigation structure
            navigation = await self._analyze_navigation(page)

            # Detect article patterns
            article_patterns = await self._detect_article_patterns(page)

            # Analyze content structure
            content_structure = await self._analyze_content_structure(page)

            return SiteStructure(
                domain=domain,
                cms_type=cms_type,
                navigation=navigation,
                article_patterns=article_patterns,
                content_structure=content_structure,
                complexity_score=self._calculate_complexity(page)
            )

    async def _detect_cms_type(self, page) -> str:
        """Detect CMS type (WordPress, Drupal, custom, etc.)"""
        # WordPress detection
        if await page.locator('meta[name="generator"][content*="WordPress"]').count() > 0:
            return "wordpress"

        # Drupal detection
        if await page.locator('meta[name="generator"][content*="Drupal"]').count() > 0:
            return "drupal"

        # Custom medical CMS patterns
        if await page.locator('.medical-news, .health-article').count() > 0:
            return "custom_medical"

        # Generic detection
        return "generic"
```

### **Phase 2: Template-Based Generation (2-3 sessions)**

#### 2.1 Scraper Templates System
```python
# services/scraper/automation/templates.py
SCRAPER_TEMPLATES = {
    "wordpress": {
        "selectors": {
            "article_list": ".post-title a, .entry-title a",
            "article_content": ".entry-content, .post-content",
            "article_date": ".published, .post-date",
            "article_author": ".author, .byline"
        },
        "extraction_patterns": {
            "title": "h1.entry-title, h1.post-title",
            "content": ".entry-content p, .post-content p",
            "summary": ".entry-summary, .post-excerpt"
        },
        "compliance_config": {
            "crawl_delay": 2,
            "max_pages": 10,
            "respect_robots": True
        }
    },

    "drupal": {
        "selectors": {
            "article_list": ".node-title a, .field-name-title a",
            "article_content": ".field-name-body, .node-content",
            "article_date": ".date-display-single, .submitted"
        },
        "extraction_patterns": {
            "title": "h1.title, .node-title",
            "content": ".field-name-body .field-items",
            "summary": ".field-name-field-summary"
        },
        "compliance_config": {
            "crawl_delay": 3,
            "max_pages": 15,
            "respect_robots": True
        }
    },

    "custom_medical": {
        "selectors": {
            "article_list": ".news-item h3 a, .medical-news .title a",
            "article_content": ".article-body, .news-content",
            "article_date": ".publish-date, .article-date"
        },
        "extraction_patterns": {
            "title": "h1.article-title, .news-title",
            "content": ".article-body p, .news-content p",
            "summary": ".article-summary, .news-excerpt"
        },
        "compliance_config": {
            "crawl_delay": 2,
            "max_pages": 20,
            "respect_robots": True,
            "medical_disclaimer": True
        }
    }
}
```

#### 2.2 Template Engine Implementation
```python
# services/scraper/automation/template_engine.py
class ScraperTemplateEngine:
    """Generates scraper code from templates based on site structure"""

    def __init__(self):
        self.templates = SCRAPER_TEMPLATES
        self.jinja_env = Environment(loader=FileSystemLoader('templates/'))

    async def generate_scraper(self, structure: SiteStructure) -> str:
        """Generate scraper code based on site structure and templates"""
        template_config = self.templates.get(structure.cms_type, self.templates["generic"])

        # Customize template based on specific site characteristics
        customized_config = await self._customize_template(template_config, structure)

        # Generate scraper code using Jinja2 template
        template = self.jinja_env.get_template('scraper_template.py.j2')

        scraper_code = template.render(
            domain=structure.domain,
            config=customized_config,
            selectors=customized_config['selectors'],
            patterns=customized_config['extraction_patterns'],
            compliance=customized_config['compliance_config']
        )

        return scraper_code

    async def _customize_template(self, template_config: dict, structure: SiteStructure) -> dict:
        """Customize template based on specific site characteristics"""
        customized = template_config.copy()

        # Adjust selectors based on detected patterns
        if structure.article_patterns:
            customized['selectors'].update(structure.article_patterns)

        # Adjust compliance settings based on site requirements
        if structure.complexity_score > 0.8:
            customized['compliance_config']['crawl_delay'] += 1

        return customized
```

### **Phase 3: Automated Testing Framework (1-2 sessions)**

#### 3.1 Comprehensive Testing Suite
```python
# services/scraper/automation/testing_framework.py
class AutomatedTestingFramework:
    """Comprehensive testing framework for generated scrapers"""

    async def run_full_test_suite(self, scraper_code: str) -> TestResults:
        """Run complete test suite for generated scraper"""
        test_results = TestResults()

        # 1. Compliance tests
        test_results.compliance = await self._test_compliance(scraper_code)

        # 2. Functionality tests
        test_results.functionality = await self._test_functionality(scraper_code)

        # 3. Performance tests
        test_results.performance = await self._test_performance(scraper_code)

        # 4. Data quality tests
        test_results.data_quality = await self._test_data_quality(scraper_code)

        # 5. Error handling tests
        test_results.error_handling = await self._test_error_handling(scraper_code)

        # Calculate overall success rate
        test_results.success_rate = self._calculate_success_rate(test_results)

        return test_results

    async def _test_compliance(self, scraper_code: str) -> ComplianceTestResult:
        """Test compliance with legal and ethical requirements"""
        return ComplianceTestResult(
            robots_txt_respected=await self._test_robots_txt_compliance(scraper_code),
            rate_limiting_applied=await self._test_rate_limiting(scraper_code),
            user_agent_proper=await self._test_user_agent(scraper_code),
            data_minimization=await self._test_data_minimization(scraper_code)
        )

    async def _test_functionality(self, scraper_code: str) -> FunctionalityTestResult:
        """Test core scraping functionality"""
        return FunctionalityTestResult(
            articles_extracted=await self._test_article_extraction(scraper_code),
            metadata_complete=await self._test_metadata_completeness(scraper_code),
            deduplication_working=await self._test_deduplication(scraper_code),
            database_integration=await self._test_database_integration(scraper_code)
        )
```

### **Phase 4: Advanced Automation (2-3 sessions)**

#### 4.1 Source Discovery and Evaluation
```python
# services/scraper/automation/source_discovery.py
class SourceDiscoverySystem:
    """Automated discovery and evaluation of new news sources"""

    async def discover_sources(self, keywords: List[str], language: str = "es") -> List[SourceCandidate]:
        """Discover potential news sources based on keywords"""
        candidates = []

        # 1. Search engine discovery
        search_results = await self._search_for_sources(keywords, language)

        # 2. Domain analysis
        for domain in search_results:
            relevance_score = await self._calculate_relevance_score(domain, keywords)
            quality_score = await self._calculate_quality_score(domain)

            if relevance_score > 0.7 and quality_score > 0.6:
                candidates.append(SourceCandidate(
                    domain=domain,
                    relevance_score=relevance_score,
                    quality_score=quality_score,
                    discovery_method="search_engine"
                ))

        # 3. Social media discovery
        social_sources = await self._discover_from_social_media(keywords)
        candidates.extend(social_sources)

        # 4. Academic/institutional discovery
        academic_sources = await self._discover_academic_sources(keywords)
        candidates.extend(academic_sources)

        return sorted(candidates, key=lambda x: x.relevance_score * x.quality_score, reverse=True)

    async def evaluate_source_quality(self, domain: str) -> QualityScore:
        """Comprehensive quality evaluation of potential source"""
        return QualityScore(
            content_quality=await self._evaluate_content_quality(domain),
            update_frequency=await self._evaluate_update_frequency(domain),
            site_reliability=await self._evaluate_site_reliability(domain),
            information_credibility=await self._evaluate_credibility(domain),
            technical_compatibility=await self._evaluate_technical_compatibility(domain)
        )
```

#### 4.2 Automated Deployment and Monitoring
```python
# services/scraper/automation/deployment_monitor.py
class DeploymentMonitor:
    """Automated deployment and continuous monitoring of scrapers"""

    async def deploy_scraper(self, scraper_code: str, domain: str) -> DeploymentResult:
        """Deploy scraper with monitoring setup"""
        # 1. Create scraper module
        scraper_module = await self._create_scraper_module(scraper_code, domain)

        # 2. Register in scraper registry
        await self._register_in_registry(domain, scraper_module)

        # 3. Setup monitoring
        await self._setup_monitoring(domain)

        # 4. Schedule health checks
        await self._schedule_health_checks(domain)

        return DeploymentResult(
            domain=domain,
            deployment_status="deployed",
            monitoring_enabled=True,
            health_check_scheduled=True
        )

    async def monitor_scraper_health(self, domain: str) -> HealthStatus:
        """Monitor scraper health and performance"""
        return HealthStatus(
            is_operational=await self._check_operational_status(domain),
            performance_metrics=await self._get_performance_metrics(domain),
            error_rate=await self._calculate_error_rate(domain),
            compliance_status=await self._check_compliance_status(domain),
            last_successful_run=await self._get_last_successful_run(domain)
        )
```

## 🛡️ Compliance Integration

### **Mandatory Compliance Checks**
All new scrapers must pass these compliance validations:

1. **Robots.txt Compliance**: 100% validation before any scraping
2. **Rate Limiting**: Configurable delays per domain (minimum 2 seconds)
3. **Legal Contact Verification**: Valid legal contact information
4. **Terms of Service Review**: Acceptable terms for academic use
5. **Fair Use Documentation**: Academic research justification
6. **Data Minimization**: Metadata-only storage approach

### **Compliance Validation Pipeline**
```python
async def validate_source_compliance(domain: str) -> ComplianceValidationResult:
    """Comprehensive compliance validation"""
    return ComplianceValidationResult(
        robots_txt_compliant=await check_robots_txt(domain),
        rate_limiting_configured=await configure_rate_limiting(domain),
        legal_contact_verified=await verify_legal_contact(domain),
        terms_acceptable=await review_terms_of_service(domain),
        fair_use_documented=await document_fair_use_basis(domain),
        data_minimization_applied=await apply_data_minimization(domain),
        gdpr_compliant=await check_gdpr_compliance(domain)
    )
```

## 📋 Implementation Roadmap

### **Session 1-2: Core Infrastructure**
- Implement `ScraperGenerator` class
- Create `SiteStructureAnalyzer`
- Setup basic template system
- Integrate compliance validation

### **Session 3-4: Template Engine**
- Implement `ScraperTemplateEngine`
- Create scraper templates for common CMS types
- Setup Jinja2 template rendering
- Test template customization

### **Session 5-6: Testing Framework**
- Implement `AutomatedTestingFramework`
- Create comprehensive test suites
- Setup performance benchmarking
- Integrate with existing testing infrastructure

### **Session 7-8: Advanced Automation**
- Implement `SourceDiscoverySystem`
- Create automated quality evaluation
- Setup deployment monitoring
- Integrate with existing API endpoints

### **Session 9-10: Production Integration**
- Frontend integration for scraper management
- API endpoints for scraper operations
- Monitoring dashboard
- Documentation and training materials

## 🎯 Success Metrics

### **Technical Metrics**
- **Scraper Generation Success Rate**: > 80%
- **Compliance Pass Rate**: 100% (no exceptions)
- **Automated Testing Coverage**: > 95%
- **Performance Benchmarks**: < 60s per scraper run
- **Error Rate**: < 5% for deployed scrapers

### **Operational Metrics**
- **Time to Deploy New Source**: < 2 hours (from 2-3 days manual)
- **Quality Score**: > 0.8 for all deployed scrapers
- **Maintenance Overhead**: < 10% of development time
- **Monitoring Coverage**: 100% of deployed scrapers

## 🔧 Technical Requirements

### **New Dependencies**
```python
# requirements.txt additions
jinja2>=3.1.0          # Template engine
playwright>=1.40.0     # Already installed
beautifulsoup4>=4.12.0 # Already installed
asyncpg>=0.29.0        # Already installed
```

### **Directory Structure**
```
services/scraper/automation/
├── __init__.py
├── scraper_generator.py     # Main generator class
├── structure_analyzer.py    # Site structure analysis
├── template_engine.py       # Template-based generation
├── testing_framework.py     # Automated testing
├── source_discovery.py      # Source discovery system
├── deployment_monitor.py    # Deployment and monitoring
└── templates/
    ├── scraper_template.py.j2
    ├── wordpress_template.py.j2
    ├── drupal_template.py.j2
    └── generic_template.py.j2
```

### **Database Schema Extensions**
```sql
-- Add scraper automation tracking
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS
    scraper_type VARCHAR(50) DEFAULT 'manual',
    generation_method VARCHAR(50),
    template_used VARCHAR(50),
    automation_score NUMERIC(3, 2),
    last_health_check TIMESTAMP,
    health_status VARCHAR(20) DEFAULT 'unknown';

-- Create scraper automation log
CREATE TABLE IF NOT EXISTS scraper_automation_log (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    result VARCHAR(20) NOT NULL,
    details JSON,
    performance_metrics JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚨 Risk Mitigation

### **Technical Risks**
- **Template Limitations**: Fallback to manual configuration
- **Site Structure Changes**: Automated monitoring and alerts
- **Performance Degradation**: Automated performance testing
- **Compliance Violations**: Mandatory pre-deployment validation

### **Legal Risks**
- **Robots.txt Changes**: Daily compliance monitoring
- **Terms of Service Updates**: Quarterly review process
- **Legal Challenges**: Complete audit trail and documentation
- **Academic Use Violations**: Fair use documentation maintenance

## 📝 Next Steps

1. **Technical Review**: Validate architecture and implementation approach
2. **Legal Review**: Ensure compliance framework adequacy
3. **Resource Allocation**: Assign development sessions and priorities
4. **Begin Implementation**: Start with Phase 1 core infrastructure
5. **Continuous Integration**: Maintain existing 100% compliance rate

---

**⚖️ Legal Compliance Commitment**: This implementation maintains the existing comprehensive legal compliance framework (🔴 CRITICAL → 🟢 LOW RISK status) while adding scalable automation capabilities. All new scrapers will be subject to the same rigorous compliance standards as existing operational scrapers.

**Contact**: cfernandom@ucompensar.edu.co
**Framework Status**: Legal compliance preserved and enhanced
**Academic Standards**: UCOMPENSAR research standards maintained
