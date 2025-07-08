"""
Integration tests for automation system workflows.
Tests complete end-to-end automation scenarios.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.scraper.automation import (
    AutomatedTestingFramework,
    ComplianceValidationResult,
    ComplianceValidator,
    ScraperGenerator,
    ScraperResult,
    ScraperTemplateEngine,
    SiteStructure,
    SiteStructureAnalyzer,
    TestResults,
)


class TestAutomationWorkflows:
    """Test complete automation workflows."""

    @pytest.fixture
    def mock_compliance_result(self):
        """Mock compliant validation result."""
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
    def mock_non_compliant_result(self):
        """Mock non-compliant validation result."""
        return ComplianceValidationResult(
            is_compliant=False,
            robots_txt_compliant=False,
            legal_contact_verified=False,
            terms_acceptable=True,
            fair_use_documented=False,
            data_minimization_applied=True,
            violations=["robots.txt disallows crawling", "no legal contact found"],
            crawl_delay=None,
        )

    @pytest.fixture
    def mock_site_structure(self):
        """Mock site structure analysis result."""
        return SiteStructure(
            domain="test-medical-news.com",
            cms_type="wordpress",
            navigation={"main_nav": ["Home", "Health News", "Research", "About"]},
            article_patterns={
                "title": "h1.entry-title",
                "content": "div.entry-content",
                "date": "time.published",
                "author": "span.author",
            },
            content_structure={
                "layout": "medical_blog",
                "has_sidebar": True,
                "article_list": "div.post-list",
                "pagination": True,
            },
            complexity_score=0.6,
            detected_selectors={
                "articles": ["article.post", "div.health-article"],
                "links": ["a.read-more", "a.article-link"],
                "images": ["img.featured-image", "img.article-image"],
            },
            javascript_heavy=False,
            requires_playwright=False,
        )

    @pytest.fixture
    def mock_complex_site_structure(self):
        """Mock complex JavaScript-heavy site structure."""
        return SiteStructure(
            domain="complex-medical-spa.com",
            cms_type="react",
            navigation={"dynamic_nav": True},
            article_patterns={
                "title": "[data-testid='article-title']",
                "content": "[data-testid='article-content']",
                "date": "[data-testid='publish-date']",
            },
            content_structure={
                "layout": "spa",
                "async_loading": True,
                "infinite_scroll": True,
            },
            complexity_score=0.9,
            detected_selectors={
                "articles": ["[data-component='Article']"],
                "buttons": ["[data-testid='load-more']"],
            },
            javascript_heavy=True,
            requires_playwright=True,
        )

    @pytest.fixture
    def mock_test_results_success(self):
        """Mock successful test results."""
        return TestResults(
            compliance_passed=True,
            functionality_passed=True,
            performance_passed=True,
            data_quality_passed=True,
            error_handling_passed=True,
            success_rate=0.95,
            detailed_results={
                "articles_extracted": 28,
                "extraction_time": 15.2,
                "errors": 1,
                "warnings": 2,
                "compliance_score": 0.98,
            },
            test_timestamp=datetime.now(timezone.utc),
        )

    @pytest.fixture
    def mock_test_results_failure(self):
        """Mock failed test results."""
        return TestResults(
            compliance_passed=False,
            functionality_passed=True,
            performance_passed=False,
            data_quality_passed=False,
            error_handling_passed=False,
            success_rate=0.3,
            detailed_results={
                "articles_extracted": 5,
                "extraction_time": 45.8,
                "errors": 15,
                "warnings": 8,
                "compliance_violations": ["rate_limit_exceeded"],
            },
            test_timestamp=datetime.now(timezone.utc),
        )

    def test_successful_scraper_generation_workflow(
        self, mock_compliance_result, mock_site_structure, mock_test_results_success
    ):
        """Test complete successful scraper generation workflow."""
        scraper_generator = ScraperGenerator()

        # Mock all components
        with (
            patch.object(
                scraper_generator.compliance_validator,
                "validate_source",
                return_value=mock_compliance_result,
            ) as mock_compliance,
            patch.object(
                scraper_generator.structure_analyzer,
                "analyze_site",
                return_value=mock_site_structure,
            ) as mock_analyze,
            patch.object(
                scraper_generator.template_engine,
                "generate_scraper",
                return_value="# Generated scraper code\nclass MedicalNewsScraper:\n    pass",
            ) as mock_generate,
            patch.object(
                scraper_generator.testing_framework,
                "run_full_test_suite",
                return_value=mock_test_results_success,
            ) as mock_test,
        ):

            # Make the async calls work properly
            mock_compliance.return_value = mock_compliance_result
            mock_analyze.return_value = mock_site_structure
            mock_generate.return_value = (
                "# Generated scraper code\nclass MedicalNewsScraper:\n    pass"
            )
            mock_test.return_value = mock_test_results_success

            # Execute workflow
            result = asyncio.run(
                scraper_generator.generate_scraper_for_domain(
                    "test-medical-news.com",
                    {
                        "language": "en",
                        "country": "US",
                        "max_articles": 30,
                        "crawl_delay": 2,
                    },
                )
            )

            # Verify workflow execution
            assert isinstance(result, ScraperResult)
            assert result.domain == "test-medical-news.com"
            assert result.compliance_result.is_compliant is True
            assert result.site_structure.cms_type == "wordpress"
            assert "Generated scraper code" in result.scraper_code
            assert result.deployment_status == "ready_for_deployment"

            # Verify all components were called
            mock_compliance.assert_called_once_with("test-medical-news.com")
            mock_analyze.assert_called_once_with("test-medical-news.com")
            mock_generate.assert_called_once()
            mock_test.assert_called_once()

            # Verify result is stored in history
            assert len(scraper_generator.generation_history) == 1
            assert (
                scraper_generator.generation_history[0].domain
                == "test-medical-news.com"
            )

    def test_compliance_failure_workflow(self, mock_non_compliant_result):
        """Test workflow when compliance validation fails."""
        scraper_generator = ScraperGenerator()

        with patch.object(
            scraper_generator.compliance_validator,
            "validate_source",
            return_value=mock_non_compliant_result,
        ) as mock_compliance:

            # Execute workflow
            result = asyncio.run(
                scraper_generator.generate_scraper_for_domain("blocked-site.com")
            )

            # Verify compliance failure handling
            assert isinstance(result, ScraperResult)
            assert result.domain == "blocked-site.com"
            assert result.compliance_result.is_compliant is False
            assert (
                result.scraper_code == ""
            )  # No code generated for non-compliant sites
            assert result.deployment_status == "compliance_failed"
            assert len(result.compliance_result.violations) == 2

            # Verify only compliance was checked
            mock_compliance.assert_called_once_with("blocked-site.com")

    def test_testing_failure_workflow(
        self, mock_compliance_result, mock_site_structure, mock_test_results_failure
    ):
        """Test workflow when automated testing fails."""
        scraper_generator = ScraperGenerator()

        with (
            patch.object(
                scraper_generator.compliance_validator,
                "validate_source",
                return_value=mock_compliance_result,
            ),
            patch.object(
                scraper_generator.structure_analyzer,
                "analyze_site",
                return_value=mock_site_structure,
            ),
            patch.object(
                scraper_generator.template_engine,
                "generate_scraper",
                return_value="# Buggy scraper code",
            ),
            patch.object(
                scraper_generator.testing_framework,
                "run_full_test_suite",
                return_value=mock_test_results_failure,
            ),
        ):

            # Execute workflow
            result = asyncio.run(
                scraper_generator.generate_scraper_for_domain("problematic-site.com")
            )

            # Verify testing failure handling
            assert isinstance(result, ScraperResult)
            assert result.domain == "problematic-site.com"
            assert result.compliance_result.is_compliant is True  # Compliance passed
            assert result.scraper_code == "# Buggy scraper code"
            assert result.deployment_status == "testing_failed"  # But testing failed

            # Verify test results indicate failure
            test_results = result.test_results
            assert test_results["compliance_passed"] is False
            assert test_results["success_rate"] == 0.3

    def test_complex_site_workflow(
        self,
        mock_compliance_result,
        mock_complex_site_structure,
        mock_test_results_success,
    ):
        """Test workflow for complex JavaScript-heavy site."""
        scraper_generator = ScraperGenerator()

        # Generate specialized scraper code for complex site
        complex_scraper_code = """
# Generated Playwright scraper for SPA site
from playwright.async_api import async_playwright

class ComplexMedicalScraper:
    def __init__(self):
        self.requires_playwright = True
        self.javascript_heavy = True

    async def scrape_articles(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            # Scraping logic here
            pass
"""

        with (
            patch.object(
                scraper_generator.compliance_validator,
                "validate_source",
                return_value=mock_compliance_result,
            ),
            patch.object(
                scraper_generator.structure_analyzer,
                "analyze_site",
                return_value=mock_complex_site_structure,
            ),
            patch.object(
                scraper_generator.template_engine,
                "generate_scraper",
                return_value=complex_scraper_code,
            ),
            patch.object(
                scraper_generator.testing_framework,
                "run_full_test_suite",
                return_value=mock_test_results_success,
            ),
        ):

            # Execute workflow
            result = asyncio.run(
                scraper_generator.generate_scraper_for_domain("complex-medical-spa.com")
            )

            # Verify complex site handling
            assert isinstance(result, ScraperResult)
            assert result.domain == "complex-medical-spa.com"
            assert result.site_structure.javascript_heavy is True
            assert result.site_structure.requires_playwright is True
            assert result.site_structure.complexity_score == 0.9
            assert "playwright" in result.scraper_code.lower()
            assert result.deployment_status == "ready_for_deployment"

    def test_batch_workflow_mixed_results(
        self,
        mock_compliance_result,
        mock_non_compliant_result,
        mock_site_structure,
        mock_test_results_success,
    ):
        """Test batch processing with mixed success/failure results."""
        scraper_generator = ScraperGenerator()

        # Mock different results for different domains
        def mock_compliance_side_effect(domain):
            if domain == "compliant-site.com":
                return mock_compliance_result
            else:
                return mock_non_compliant_result

        with (
            patch.object(
                scraper_generator.compliance_validator,
                "validate_source",
                side_effect=mock_compliance_side_effect,
            ),
            patch.object(
                scraper_generator.structure_analyzer,
                "analyze_site",
                return_value=mock_site_structure,
            ),
            patch.object(
                scraper_generator.template_engine,
                "generate_scraper",
                return_value="# Generated code",
            ),
            patch.object(
                scraper_generator.testing_framework,
                "run_full_test_suite",
                return_value=mock_test_results_success,
            ),
        ):

            # Execute batch workflow
            domains = [
                "compliant-site.com",
                "non-compliant-site.com",
                "another-compliant.com",
            ]
            results = []

            for domain in domains:
                result = asyncio.run(
                    scraper_generator.generate_scraper_for_domain(domain)
                )
                results.append(result)

            # Verify mixed results
            assert len(results) == 3

            # First domain should succeed
            assert results[0].domain == "compliant-site.com"
            assert results[0].deployment_status == "ready_for_deployment"

            # Second domain should fail compliance
            assert results[1].domain == "non-compliant-site.com"
            assert results[1].deployment_status == "compliance_failed"

            # Third domain should fail compliance (same as second)
            assert results[2].domain == "another-compliant.com"
            assert results[2].deployment_status == "compliance_failed"

            # Verify history contains successful attempts only (compliance failures return early)
            # Only the first domain should be in history since it was compliant
            assert len(scraper_generator.generation_history) == 1
            assert (
                scraper_generator.generation_history[0].domain == "compliant-site.com"
            )

    def test_workflow_error_handling(self):
        """Test workflow error handling for unexpected failures."""
        scraper_generator = ScraperGenerator()

        # Mock a failure in site structure analysis
        with (
            patch.object(
                scraper_generator.compliance_validator, "validate_source"
            ) as mock_compliance,
            patch.object(
                scraper_generator.structure_analyzer, "analyze_site"
            ) as mock_analyze,
        ):

            # Set up successful compliance but failed analysis
            mock_compliance.return_value = ComplianceValidationResult(
                is_compliant=True,
                robots_txt_compliant=True,
                legal_contact_verified=True,
                terms_acceptable=True,
                fair_use_documented=True,
                data_minimization_applied=True,
            )
            mock_analyze.side_effect = Exception("Network timeout during analysis")

            # Execute workflow - the system handles exceptions internally and returns a result
            result = asyncio.run(
                scraper_generator.generate_scraper_for_domain("unreachable-site.com")
            )

            # Verify error handling - system should return a failed result, not raise exception
            assert isinstance(result, ScraperResult)
            assert result.domain == "unreachable-site.com"
            assert result.deployment_status == "generation_failed"
            assert result.scraper_code == ""

    def test_workflow_performance_tracking(
        self, mock_compliance_result, mock_site_structure, mock_test_results_success
    ):
        """Test workflow performance metrics tracking."""
        scraper_generator = ScraperGenerator()

        with (
            patch.object(
                scraper_generator.compliance_validator,
                "validate_source",
                return_value=mock_compliance_result,
            ),
            patch.object(
                scraper_generator.structure_analyzer,
                "analyze_site",
                return_value=mock_site_structure,
            ),
            patch.object(
                scraper_generator.template_engine,
                "generate_scraper",
                return_value="# Generated code",
            ),
            patch.object(
                scraper_generator.testing_framework,
                "run_full_test_suite",
                return_value=mock_test_results_success,
            ),
        ):

            # Execute workflow
            start_time = datetime.now(timezone.utc)
            result = asyncio.run(
                scraper_generator.generate_scraper_for_domain("performance-test.com")
            )
            end_time = datetime.now(timezone.utc)

            # Verify timing tracking
            assert isinstance(result, ScraperResult)
            assert result.generation_timestamp >= start_time
            assert result.generation_timestamp <= end_time

            # Verify performance metrics can be tracked
            assert isinstance(result.performance_metrics, dict)

    def test_workflow_statistics_tracking(
        self,
        mock_compliance_result,
        mock_non_compliant_result,
        mock_site_structure,
        mock_test_results_success,
    ):
        """Test workflow statistics collection."""
        scraper_generator = ScraperGenerator()

        # Execute multiple workflows to build statistics
        test_scenarios = [
            ("success1.com", mock_compliance_result, "ready_for_deployment"),
            ("failure1.com", mock_non_compliant_result, "compliance_failed"),
            ("success2.com", mock_compliance_result, "ready_for_deployment"),
            ("success3.com", mock_compliance_result, "ready_for_deployment"),
        ]

        for domain, compliance_result, expected_status in test_scenarios:
            with (
                patch.object(
                    scraper_generator.compliance_validator,
                    "validate_source",
                    return_value=compliance_result,
                ),
                patch.object(
                    scraper_generator.structure_analyzer,
                    "analyze_site",
                    return_value=mock_site_structure,
                ),
                patch.object(
                    scraper_generator.template_engine,
                    "generate_scraper",
                    return_value="# Code",
                ),
                patch.object(
                    scraper_generator.testing_framework,
                    "run_full_test_suite",
                    return_value=mock_test_results_success,
                ),
            ):

                result = asyncio.run(
                    scraper_generator.generate_scraper_for_domain(domain)
                )
                assert result.deployment_status == expected_status

        # Verify statistics - only successful generations are added to history
        stats = scraper_generator.get_generation_stats()

        # Only 3 successful generations should be in history (compliance failures return early)
        assert stats["total_generated"] == 3
        assert stats["deployment_ready"] == 3  # All 3 successful
        assert stats["success_rate"] == 1.0  # 3/3 success rate
        assert (
            stats["compliance_rate"] == 1.0
        )  # 3/3 compliance rate (only compliant ones in history)
        assert stats["last_generation"] is not None


import asyncio  # Import for async test execution
