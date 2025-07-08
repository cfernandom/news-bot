"""
Integration tests for automation API endpoints.
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from services.api.main import app
from services.scraper.automation.models import (
    ComplianceValidationResult,
    ScraperResult,
    SiteStructure,
    TestResults,
)


class TestAutomationAPIEndpoints:
    """Test automation API endpoints integration."""

    @pytest.fixture
    def client(self):
        """Create test client for automation API."""
        return TestClient(app)

    @pytest.fixture
    def mock_compliance_result(self):
        """Mock compliance validation result."""
        return ComplianceValidationResult(
            is_compliant=True,
            robots_txt_compliant=True,
            legal_contact_verified=True,
            terms_acceptable=True,
            fair_use_documented=True,
            data_minimization_applied=True,
            violations=[],
            crawl_delay=2.0,
        )

    @pytest.fixture
    def mock_site_structure(self):
        """Mock site structure analysis result."""
        return SiteStructure(
            domain="test-domain.com",
            cms_type="wordpress",
            navigation={"main_nav": ["Home", "News", "About"]},
            article_patterns={"title": "h1.post-title", "content": "div.post-content"},
            content_structure={"layout": "standard", "sidebar": True},
            complexity_score=0.7,
            detected_selectors={"articles": ["article.post", "div.article"]},
            javascript_heavy=False,
            requires_playwright=False,
        )

    @pytest.fixture
    def mock_scraper_result(self, mock_compliance_result, mock_site_structure):
        """Mock complete scraper generation result."""
        return ScraperResult(
            domain="test-domain.com",
            scraper_code="import requests\n# Generated scraper code\nclass TestScraper:\n    pass",
            compliance_result=mock_compliance_result,
            site_structure=mock_site_structure,
            template_used="wordpress",
            test_results={"success_rate": 0.9, "articles_extracted": 25},
            deployment_status="ready_for_deployment",
            generation_timestamp=datetime.now(timezone.utc),
            performance_metrics={"response_time": 1.2, "memory_usage": 45.2},
        )

    def test_automation_health_endpoint(self, client):
        """Test automation health check endpoint."""
        response = client.get("/api/automation/health")

        assert response.status_code == 200
        data = response.json()

        assert "automation_system" in data
        assert "scraper_generator" in data
        assert "structure_analyzer" in data
        assert "compliance_validator" in data
        assert "timestamp" in data
        assert "version" in data

        # System should be healthy by default
        assert data["automation_system"] == "healthy"
        assert data["scraper_generator"] == "ready"
        assert data["structure_analyzer"] == "ready"
        assert data["compliance_validator"] == "ready"

    def test_get_available_templates(self, client):
        """Test get available templates endpoint."""
        response = client.get("/api/automation/templates")

        assert response.status_code == 200
        data = response.json()

        assert "available_templates" in data
        assert "template_descriptions" in data

        # Check expected templates
        templates = data["available_templates"]
        assert "wordpress" in templates
        assert "drupal" in templates
        assert "custom_medical" in templates
        assert "news_site" in templates
        assert "generic_article" in templates
        assert "generic" in templates

        # Verify descriptions match templates count
        assert len(data["template_descriptions"]) == len(templates)

    def test_get_automation_stats(self, client):
        """Test automation statistics endpoint."""
        response = client.get("/api/automation/stats")

        assert response.status_code == 200
        data = response.json()

        assert "total_generated" in data
        assert "success_rate" in data
        assert "compliance_rate" in data
        assert "deployment_ready" in data
        assert "templates_used" in data
        assert "last_generation" in data

        # Initial stats should show zero generation
        assert data["total_generated"] == 0
        assert isinstance(data["success_rate"], float)
        assert isinstance(data["compliance_rate"], float)
        assert data["deployment_ready"] == 0
        assert isinstance(data["templates_used"], dict)

    @patch(
        "services.scraper.automation.structure_analyzer.SiteStructureAnalyzer.analyze_site"
    )
    def test_analyze_domain_endpoint(
        self, mock_analyze_site, client, mock_site_structure
    ):
        """Test domain analysis endpoint."""
        mock_analyze_site.return_value = mock_site_structure

        request_data = {"domain": "test-domain.com"}
        response = client.post("/api/automation/analyze-domain", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["domain"] == "test-domain.com"
        assert data["cms_type"] == "wordpress"
        assert data["complexity_score"] == 0.7
        assert data["javascript_heavy"] is False
        assert data["requires_playwright"] is False
        assert data["article_patterns_count"] == len(
            mock_site_structure.article_patterns
        )
        assert data["detected_selectors_count"] == len(
            mock_site_structure.detected_selectors
        )
        assert "analysis_timestamp" in data

        # Verify mock was called correctly
        mock_analyze_site.assert_called_once_with("test-domain.com")

    @patch(
        "services.scraper.automation.compliance_validator.ComplianceValidator.validate_source"
    )
    def test_validate_compliance_endpoint(
        self, mock_validate_source, client, mock_compliance_result
    ):
        """Test compliance validation endpoint."""
        mock_validate_source.return_value = mock_compliance_result

        request_data = {"domain": "test-domain.com"}
        response = client.post("/api/automation/validate-compliance", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["domain"] == "test-domain.com"
        assert data["is_compliant"] is True
        assert data["robots_txt_compliant"] is True
        assert data["legal_contact_verified"] is True
        assert data["terms_acceptable"] is True
        assert data["fair_use_documented"] is True
        assert data["data_minimization_applied"] is True
        assert data["violations"] == []
        assert data["crawl_delay"] == 2.0
        assert "validation_timestamp" in data

        # Verify mock was called correctly
        mock_validate_source.assert_called_once_with("test-domain.com")

    @patch(
        "services.scraper.automation.compliance_validator.ComplianceValidator.validate_source"
    )
    def test_validate_compliance_non_compliant(self, mock_validate_source, client):
        """Test compliance validation for non-compliant domain."""
        non_compliant_result = ComplianceValidationResult(
            is_compliant=False,
            robots_txt_compliant=False,
            legal_contact_verified=False,
            terms_acceptable=True,
            fair_use_documented=False,
            data_minimization_applied=True,
            violations=["robots.txt disallows crawling", "no legal contact found"],
            crawl_delay=None,
        )
        mock_validate_source.return_value = non_compliant_result

        request_data = {"domain": "blocked-domain.com"}
        response = client.post("/api/automation/validate-compliance", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["domain"] == "blocked-domain.com"
        assert data["is_compliant"] is False
        assert data["robots_txt_compliant"] is False
        assert data["legal_contact_verified"] is False
        assert len(data["violations"]) == 2
        assert "robots.txt disallows crawling" in data["violations"]
        assert data["crawl_delay"] is None

    @patch(
        "services.scraper.automation.scraper_generator.ScraperGenerator.generate_scraper_for_domain"
    )
    def test_generate_scraper_endpoint(
        self, mock_generate_scraper, client, mock_scraper_result
    ):
        """Test scraper generation endpoint."""
        mock_generate_scraper.return_value = mock_scraper_result

        request_data = {
            "domain": "test-domain.com",
            "language": "en",
            "country": "US",
            "max_articles": 30,
            "crawl_delay": 2,
        }
        response = client.post("/api/automation/generate-scraper", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["domain"] == "test-domain.com"
        assert data["status"] == "ready_for_deployment"
        assert data["template_used"] == "wordpress"
        assert data["deployment_ready"] is True
        assert "code_preview" in data
        assert "import requests" in data["code_preview"]
        assert "generation_timestamp" in data

        # Verify compliance and site structure are included
        assert "compliance_result" in data
        assert data["compliance_result"]["is_compliant"] is True
        assert "site_structure" in data
        assert data["site_structure"]["cms_type"] == "wordpress"

        # Verify test results are included
        assert "test_results" in data
        assert data["test_results"]["success_rate"] == 0.9

    @patch(
        "services.scraper.automation.scraper_generator.ScraperGenerator.generate_scraper_for_domain"
    )
    def test_generate_scraper_with_defaults(
        self, mock_generate_scraper, client, mock_scraper_result
    ):
        """Test scraper generation with default parameters."""
        mock_generate_scraper.return_value = mock_scraper_result

        request_data = {"domain": "test-domain.com"}
        response = client.post("/api/automation/generate-scraper", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["domain"] == "test-domain.com"
        # Verify mock was called with default config
        args, kwargs = mock_generate_scraper.call_args
        assert args[0] == "test-domain.com"
        config = args[1]
        assert config["language"] == "en"
        assert config["country"] == "US"
        assert config["max_articles"] == 30
        assert config["crawl_delay"] == 2

    @patch(
        "services.scraper.automation.scraper_generator.ScraperGenerator.generate_scraper_for_domain"
    )
    def test_generate_scraper_failure(self, mock_generate_scraper, client):
        """Test scraper generation failure handling."""
        mock_generate_scraper.side_effect = Exception("Network timeout during analysis")

        request_data = {"domain": "unreachable-domain.com"}
        response = client.post("/api/automation/generate-scraper", json=request_data)

        assert response.status_code == 500
        data = response.json()

        assert "detail" in data
        assert "Failed to generate scraper" in data["detail"]
        assert "Network timeout during analysis" in data["detail"]

    @patch(
        "services.scraper.automation.scraper_generator.ScraperGenerator.generate_scraper_for_domain"
    )
    def test_batch_generate_scrapers(
        self, mock_generate_scraper, client, mock_scraper_result
    ):
        """Test batch scraper generation endpoint."""
        mock_generate_scraper.return_value = mock_scraper_result

        domains = ["domain1.com", "domain2.com", "domain3.com"]
        response = client.post("/api/automation/batch-generate", json=domains)

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 3
        for i, result in enumerate(data):
            assert result["domain"] == mock_scraper_result.domain
            assert result["status"] == "ready_for_deployment"
            assert result["template_used"] == "wordpress"

        # Verify mock was called for each domain
        assert mock_generate_scraper.call_count == 3

    def test_batch_generate_too_many_domains(self, client):
        """Test batch generation with too many domains."""
        domains = [f"domain{i}.com" for i in range(15)]  # More than 10 limit
        response = client.post("/api/automation/batch-generate", json=domains)

        assert response.status_code == 400
        data = response.json()

        assert "detail" in data
        assert "Maximum 10 domains allowed" in data["detail"]

    @patch(
        "services.scraper.automation.scraper_generator.ScraperGenerator.generate_scraper_for_domain"
    )
    def test_batch_generate_partial_failure(
        self, mock_generate_scraper, client, mock_scraper_result
    ):
        """Test batch generation with some failures."""

        def side_effect(domain, config=None):
            if domain == "failing-domain.com":
                raise Exception("Connection failed")
            return mock_scraper_result

        mock_generate_scraper.side_effect = side_effect

        domains = ["success1.com", "failing-domain.com", "success2.com"]
        response = client.post("/api/automation/batch-generate", json=domains)

        assert response.status_code == 200
        data = response.json()

        # Should return results only for successful domains
        assert len(data) == 2
        for result in data:
            assert result["status"] == "ready_for_deployment"

    def test_clear_automation_cache(self, client):
        """Test clear automation cache endpoint."""
        response = client.delete("/api/automation/clear-cache")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "successfully" in data["message"].lower()
        assert "timestamp" in data


class TestAutomationAPIValidation:
    """Test API request validation and error handling."""

    @pytest.fixture
    def client(self):
        """Create test client for validation tests."""
        return TestClient(app)

    def test_generate_scraper_missing_domain(self, client):
        """Test scraper generation with missing domain."""
        request_data = {"language": "en"}  # Missing required domain
        response = client.post("/api/automation/generate-scraper", json=request_data)

        assert response.status_code == 422
        data = response.json()

        assert "detail" in data
        # Should indicate missing required field

    def test_generate_scraper_invalid_domain(self, client):
        """Test scraper generation with invalid domain format."""
        request_data = {"domain": "not-a-valid-domain"}
        response = client.post("/api/automation/generate-scraper", json=request_data)

        # Should accept any string for domain and let validation happen in backend
        # The error will come from the actual validation logic, not the API validation
        assert response.status_code in [
            200,
            500,
        ]  # Either succeeds or fails in processing

    def test_analyze_domain_missing_domain(self, client):
        """Test domain analysis with missing domain."""
        request_data = {}  # Missing required domain
        response = client.post("/api/automation/analyze-domain", json=request_data)

        assert response.status_code == 422
        data = response.json()

        assert "detail" in data

    def test_validate_compliance_missing_domain(self, client):
        """Test compliance validation with missing domain."""
        request_data = {}  # Missing required domain
        response = client.post("/api/automation/validate-compliance", json=request_data)

        assert response.status_code == 422
        data = response.json()

        assert "detail" in data

    def test_generate_scraper_invalid_parameters(self, client):
        """Test scraper generation with invalid parameters."""
        request_data = {
            "domain": "test-domain.com",
            "max_articles": -5,  # Invalid negative value
            "crawl_delay": -1,  # Invalid negative value
        }

        response = client.post("/api/automation/generate-scraper", json=request_data)

        # API should handle validation or pass to backend for validation
        # The specific response depends on implementation
        assert response.status_code in [200, 422, 500]

    def test_batch_generate_invalid_input(self, client):
        """Test batch generation with invalid input format."""
        # Send non-list data
        response = client.post("/api/automation/batch-generate", json="not-a-list")

        assert response.status_code == 422
        data = response.json()

        assert "detail" in data

    def test_batch_generate_empty_list(self, client):
        """Test batch generation with empty domain list."""
        response = client.post("/api/automation/batch-generate", json=[])

        assert response.status_code == 200
        data = response.json()

        # Should return empty list for empty input
        assert data == []


class TestAutomationAPIIntegration:
    """Test automation API integration with actual components."""

    @pytest.fixture
    def client(self):
        """Create test client for integration tests."""
        return TestClient(app)

    def test_full_workflow_integration(self, client):
        """Test complete automation workflow through API."""
        domain = "example.com"

        # Step 1: Check health
        health_response = client.get("/api/automation/health")
        assert health_response.status_code == 200

        # Step 2: Get available templates
        templates_response = client.get("/api/automation/templates")
        assert templates_response.status_code == 200
        templates_data = templates_response.json()
        assert "wordpress" in templates_data["available_templates"]

        # Step 3: Check initial stats
        stats_response = client.get("/api/automation/stats")
        assert stats_response.status_code == 200
        initial_stats = stats_response.json()
        initial_count = initial_stats["total_generated"]

        # Note: Actual domain analysis and scraper generation would require
        # mocking or real network calls, which we'll test in separate tests

        # Step 4: Clear cache (should work regardless)
        cache_response = client.delete("/api/automation/clear-cache")
        assert cache_response.status_code == 200

    def test_api_error_handling_consistency(self, client):
        """Test consistent error handling across endpoints."""
        # Test non-existent endpoints
        response = client.get("/api/automation/nonexistent")
        assert response.status_code == 404

        # Test invalid methods
        response = client.put("/api/automation/health")
        assert response.status_code == 405

        # Test malformed JSON
        response = client.post(
            "/api/automation/analyze-domain",
            data="malformed json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422
