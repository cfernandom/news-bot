"""
Unit tests for automation system models.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List

import pytest

from services.scraper.automation.models import (
    ComplianceValidationResult,
    DeploymentResult,
    HealthStatus,
    QualityScore,
    ScraperResult,
    SiteStructure,
    SourceCandidate,
    SourceEvaluationResult,
    SourceQualityMetrics,
    TestResults,
)


class TestComplianceValidationResult:
    """Test ComplianceValidationResult model."""

    def test_create_compliant_result(self):
        """Test creating a compliant validation result."""
        result = ComplianceValidationResult(
            is_compliant=True,
            robots_txt_compliant=True,
            legal_contact_verified=True,
            terms_acceptable=True,
            fair_use_documented=True,
            data_minimization_applied=True,
            violations=[],
            crawl_delay=2.0,
        )

        assert result.is_compliant is True
        assert result.robots_txt_compliant is True
        assert result.legal_contact_verified is True
        assert result.terms_acceptable is True
        assert result.fair_use_documented is True
        assert result.data_minimization_applied is True
        assert result.violations == []
        assert result.crawl_delay == 2.0

    def test_create_non_compliant_result(self):
        """Test creating a non-compliant validation result."""
        violations = ["robots.txt disallows crawling", "no legal contact found"]
        result = ComplianceValidationResult(
            is_compliant=False,
            robots_txt_compliant=False,
            legal_contact_verified=False,
            terms_acceptable=True,
            fair_use_documented=False,
            data_minimization_applied=True,
            violations=violations,
            crawl_delay=None,
        )

        assert result.is_compliant is False
        assert result.robots_txt_compliant is False
        assert result.legal_contact_verified is False
        assert result.violations == violations
        assert result.crawl_delay is None

    def test_default_values(self):
        """Test default values for optional fields."""
        result = ComplianceValidationResult(
            is_compliant=True,
            robots_txt_compliant=True,
            legal_contact_verified=True,
            terms_acceptable=True,
            fair_use_documented=True,
            data_minimization_applied=True,
        )

        assert result.violations == []
        assert result.crawl_delay is None


class TestSiteStructure:
    """Test SiteStructure model."""

    def test_create_basic_site_structure(self):
        """Test creating a basic site structure."""
        structure = SiteStructure(
            domain="example.com",
            cms_type="wordpress",
            navigation={"main_nav": ["Home", "News", "About"]},
            article_patterns={"title": "h1.post-title", "content": "div.post-content"},
            content_structure={"layout": "standard", "sidebar": True},
            complexity_score=0.7,
        )

        assert structure.domain == "example.com"
        assert structure.cms_type == "wordpress"
        assert structure.navigation["main_nav"] == ["Home", "News", "About"]
        assert structure.article_patterns["title"] == "h1.post-title"
        assert structure.complexity_score == 0.7

    def test_default_values(self):
        """Test default values for optional fields."""
        structure = SiteStructure(
            domain="example.com",
            cms_type="custom",
            navigation={},
            article_patterns={},
            content_structure={},
            complexity_score=0.5,
        )

        assert structure.detected_selectors == {}
        assert structure.javascript_heavy is False
        assert structure.requires_playwright is False

    def test_javascript_heavy_site(self):
        """Test site structure for JavaScript-heavy site."""
        structure = SiteStructure(
            domain="spa-site.com",
            cms_type="react",
            navigation={},
            article_patterns={},
            content_structure={},
            complexity_score=0.9,
            javascript_heavy=True,
            requires_playwright=True,
        )

        assert structure.javascript_heavy is True
        assert structure.requires_playwright is True


class TestSourceQualityMetrics:
    """Test SourceQualityMetrics model."""

    def test_create_quality_metrics(self):
        """Test creating quality metrics."""
        metrics = SourceQualityMetrics(
            content_freshness=0.8,
            content_volume=0.7,
            content_structure=0.9,
            update_frequency=0.6,
        )

        assert metrics.content_freshness == 0.8
        assert metrics.content_volume == 0.7
        assert metrics.content_structure == 0.9
        assert metrics.update_frequency == 0.6

    def test_metrics_range_validation(self):
        """Test that metrics can handle valid ranges."""
        # Test boundary values
        metrics = SourceQualityMetrics(
            content_freshness=0.0,
            content_volume=1.0,
            content_structure=0.5,
            update_frequency=0.3,
        )

        assert metrics.content_freshness == 0.0
        assert metrics.content_volume == 1.0


class TestQualityScore:
    """Test QualityScore model with automatic calculation."""

    def test_overall_score_calculation(self):
        """Test automatic overall score calculation."""
        score = QualityScore(
            content_quality=0.8,
            update_frequency=0.7,
            site_reliability=0.9,
            information_credibility=0.8,
            technical_compatibility=0.6,
        )

        expected_overall = (0.8 + 0.7 + 0.9 + 0.8 + 0.6) / 5.0
        assert score.overall_score == expected_overall
        assert score.overall_score == 0.76

    def test_perfect_score(self):
        """Test perfect quality score."""
        score = QualityScore(
            content_quality=1.0,
            update_frequency=1.0,
            site_reliability=1.0,
            information_credibility=1.0,
            technical_compatibility=1.0,
        )

        assert score.overall_score == 1.0

    def test_zero_score(self):
        """Test zero quality score."""
        score = QualityScore(
            content_quality=0.0,
            update_frequency=0.0,
            site_reliability=0.0,
            information_credibility=0.0,
            technical_compatibility=0.0,
        )

        assert score.overall_score == 0.0


class TestScraperResult:
    """Test ScraperResult model."""

    def test_create_scraper_result(self):
        """Test creating a scraper result."""
        compliance_result = ComplianceValidationResult(
            is_compliant=True,
            robots_txt_compliant=True,
            legal_contact_verified=True,
            terms_acceptable=True,
            fair_use_documented=True,
            data_minimization_applied=True,
        )

        site_structure = SiteStructure(
            domain="example.com",
            cms_type="wordpress",
            navigation={},
            article_patterns={},
            content_structure={},
            complexity_score=0.5,
        )

        result = ScraperResult(
            domain="example.com",
            scraper_code="import requests\n# Generated scraper code",
            compliance_result=compliance_result,
            site_structure=site_structure,
            template_used="wordpress",
            deployment_status="ready_for_deployment",
        )

        assert result.domain == "example.com"
        assert "import requests" in result.scraper_code
        assert result.template_used == "wordpress"
        assert result.deployment_status == "ready_for_deployment"
        assert result.compliance_result.is_compliant is True

    def test_default_values(self):
        """Test default values for optional fields."""
        compliance_result = ComplianceValidationResult(
            is_compliant=True,
            robots_txt_compliant=True,
            legal_contact_verified=True,
            terms_acceptable=True,
            fair_use_documented=True,
            data_minimization_applied=True,
        )

        site_structure = SiteStructure(
            domain="example.com",
            cms_type="custom",
            navigation={},
            article_patterns={},
            content_structure={},
            complexity_score=0.5,
        )

        result = ScraperResult(
            domain="example.com",
            scraper_code="# Code here",
            compliance_result=compliance_result,
            site_structure=site_structure,
            template_used="generic",
        )

        assert result.test_results is None
        assert result.deployment_status == "pending"
        assert result.performance_metrics == {}
        assert isinstance(result.generation_timestamp, datetime)

    def test_with_test_results(self):
        """Test scraper result with test results."""
        compliance_result = ComplianceValidationResult(
            is_compliant=True,
            robots_txt_compliant=True,
            legal_contact_verified=True,
            terms_acceptable=True,
            fair_use_documented=True,
            data_minimization_applied=True,
        )

        site_structure = SiteStructure(
            domain="example.com",
            cms_type="wordpress",
            navigation={},
            article_patterns={},
            content_structure={},
            complexity_score=0.5,
        )

        test_results = {"success_rate": 0.9, "articles_extracted": 25}

        result = ScraperResult(
            domain="example.com",
            scraper_code="# Code here",
            compliance_result=compliance_result,
            site_structure=site_structure,
            template_used="wordpress",
            test_results=test_results,
            deployment_status="tested",
        )

        assert result.test_results == test_results
        assert result.deployment_status == "tested"


class TestSourceCandidate:
    """Test SourceCandidate model."""

    def test_create_source_candidate(self):
        """Test creating a source candidate."""
        candidate = SourceCandidate(
            domain="medical-news.com",
            relevance_score=0.8,
            quality_score=0.7,
            discovery_method="google_search",
            compliance_status="compliant",
            estimated_articles_per_day=15,
            language="en",
            country="US",
        )

        assert candidate.domain == "medical-news.com"
        assert candidate.relevance_score == 0.8
        assert candidate.quality_score == 0.7
        assert candidate.discovery_method == "google_search"
        assert candidate.compliance_status == "compliant"
        assert candidate.estimated_articles_per_day == 15

    def test_default_values(self):
        """Test default values for optional fields."""
        candidate = SourceCandidate(
            domain="medical-news.com",
            relevance_score=0.8,
            quality_score=0.7,
            discovery_method="manual",
        )

        assert candidate.compliance_status is None
        assert candidate.estimated_articles_per_day is None
        assert candidate.language == "en"
        assert candidate.country == "US"


class TestTestResults:
    """Test TestResults model."""

    def test_create_test_results(self):
        """Test creating test results."""
        results = TestResults(
            compliance_passed=True,
            functionality_passed=True,
            performance_passed=True,
            data_quality_passed=True,
            error_handling_passed=True,
            success_rate=0.95,
            detailed_results={"articles_extracted": 28, "errors": 1},
        )

        assert results.compliance_passed is True
        assert results.functionality_passed is True
        assert results.performance_passed is True
        assert results.data_quality_passed is True
        assert results.error_handling_passed is True
        assert results.success_rate == 0.95
        assert results.detailed_results["articles_extracted"] == 28

    def test_failed_test_results(self):
        """Test creating failed test results."""
        results = TestResults(
            compliance_passed=False,
            functionality_passed=True,
            performance_passed=False,
            data_quality_passed=True,
            error_handling_passed=False,
            success_rate=0.3,
            detailed_results={"errors": ["compliance_error", "performance_timeout"]},
        )

        assert results.compliance_passed is False
        assert results.performance_passed is False
        assert results.error_handling_passed is False
        assert results.success_rate == 0.3

    def test_default_values(self):
        """Test default values for optional fields."""
        results = TestResults(
            compliance_passed=True,
            functionality_passed=True,
            performance_passed=True,
            data_quality_passed=True,
            error_handling_passed=True,
            success_rate=0.9,
        )

        assert results.detailed_results == {}
        assert isinstance(results.test_timestamp, datetime)


class TestDeploymentResult:
    """Test DeploymentResult model."""

    def test_successful_deployment(self):
        """Test successful deployment result."""
        result = DeploymentResult(
            domain="example.com",
            deployment_status="deployed",
            monitoring_enabled=True,
            health_check_scheduled=True,
            errors=[],
        )

        assert result.domain == "example.com"
        assert result.deployment_status == "deployed"
        assert result.monitoring_enabled is True
        assert result.health_check_scheduled is True
        assert result.errors == []

    def test_failed_deployment(self):
        """Test failed deployment result."""
        errors = ["connection_timeout", "authentication_failed"]
        result = DeploymentResult(
            domain="example.com",
            deployment_status="failed",
            monitoring_enabled=False,
            health_check_scheduled=False,
            errors=errors,
        )

        assert result.deployment_status == "failed"
        assert result.monitoring_enabled is False
        assert result.health_check_scheduled is False
        assert result.errors == errors

    def test_default_values(self):
        """Test default values for optional fields."""
        result = DeploymentResult(
            domain="example.com",
            deployment_status="pending",
            monitoring_enabled=False,
            health_check_scheduled=False,
        )

        assert result.errors == []
        assert isinstance(result.deployment_timestamp, datetime)


class TestHealthStatus:
    """Test HealthStatus model."""

    def test_healthy_status(self):
        """Test healthy scraper status."""
        status = HealthStatus(
            domain="example.com",
            is_operational=True,
            performance_metrics={"response_time": 1.2, "success_rate": 0.95},
            error_rate=0.05,
            compliance_status="compliant",
            last_successful_run=datetime.now(timezone.utc),
        )

        assert status.domain == "example.com"
        assert status.is_operational is True
        assert status.performance_metrics["response_time"] == 1.2
        assert status.error_rate == 0.05
        assert status.compliance_status == "compliant"
        assert status.last_successful_run is not None

    def test_unhealthy_status(self):
        """Test unhealthy scraper status."""
        status = HealthStatus(
            domain="example.com",
            is_operational=False,
            performance_metrics={"response_time": 30.0, "success_rate": 0.1},
            error_rate=0.9,
            compliance_status="violation_detected",
            last_successful_run=None,
        )

        assert status.is_operational is False
        assert status.performance_metrics["success_rate"] == 0.1
        assert status.error_rate == 0.9
        assert status.compliance_status == "violation_detected"
        assert status.last_successful_run is None

    def test_default_values(self):
        """Test default values for optional fields."""
        status = HealthStatus(
            domain="example.com",
            is_operational=True,
            performance_metrics={},
            error_rate=0.0,
            compliance_status="unknown",
        )

        assert status.last_successful_run is None
        assert isinstance(status.last_check, datetime)


class TestModelIntegration:
    """Test integration between models."""

    def test_source_evaluation_result_integration(self):
        """Test SourceEvaluationResult with all dependent models."""
        compliance_result = ComplianceValidationResult(
            is_compliant=True,
            robots_txt_compliant=True,
            legal_contact_verified=True,
            terms_acceptable=True,
            fair_use_documented=True,
            data_minimization_applied=True,
        )

        content_quality = SourceQualityMetrics(
            content_freshness=0.8,
            content_volume=0.7,
            content_structure=0.9,
            update_frequency=0.6,
        )

        technical_quality = SourceQualityMetrics(
            content_freshness=0.7,
            content_volume=0.8,
            content_structure=0.8,
            update_frequency=0.7,
        )

        evaluation = SourceEvaluationResult(
            domain="medical-news.com",
            compliance_result=compliance_result,
            content_quality=content_quality,
            technical_quality=technical_quality,
            medical_relevance=0.9,
            overall_score=0.8,
            recommendation="highly_recommended",
            evaluation_timestamp=datetime.now(timezone.utc),
        )

        assert evaluation.domain == "medical-news.com"
        assert evaluation.compliance_result.is_compliant is True
        assert evaluation.content_quality.content_freshness == 0.8
        assert evaluation.technical_quality.content_volume == 0.8
        assert evaluation.medical_relevance == 0.9
        assert evaluation.overall_score == 0.8
        assert evaluation.recommendation == "highly_recommended"

    def test_complex_scraper_result_integration(self):
        """Test complex ScraperResult with all components."""
        compliance_result = ComplianceValidationResult(
            is_compliant=True,
            robots_txt_compliant=True,
            legal_contact_verified=True,
            terms_acceptable=True,
            fair_use_documented=True,
            data_minimization_applied=True,
            crawl_delay=2.0,
        )

        site_structure = SiteStructure(
            domain="medical-journal.com",
            cms_type="drupal",
            navigation={"main": ["Articles", "Research", "News"]},
            article_patterns={"title": "h1.article-title", "body": "div.article-body"},
            content_structure={"layout": "academic", "has_authors": True},
            complexity_score=0.8,
            javascript_heavy=False,
            requires_playwright=False,
        )

        test_results = {
            "compliance_passed": True,
            "functionality_passed": True,
            "performance_passed": True,
            "articles_extracted": 30,
            "success_rate": 0.95,
        }

        scraper_result = ScraperResult(
            domain="medical-journal.com",
            scraper_code="# Generated Drupal scraper code\nimport requests\n...",
            compliance_result=compliance_result,
            site_structure=site_structure,
            template_used="drupal",
            test_results=test_results,
            deployment_status="ready_for_deployment",
            performance_metrics={"avg_response_time": 2.1, "memory_usage": 45.2},
        )

        assert scraper_result.domain == "medical-journal.com"
        assert scraper_result.compliance_result.crawl_delay == 2.0
        assert scraper_result.site_structure.cms_type == "drupal"
        assert scraper_result.test_results["success_rate"] == 0.95
        assert scraper_result.deployment_status == "ready_for_deployment"
        assert scraper_result.performance_metrics["avg_response_time"] == 2.1
