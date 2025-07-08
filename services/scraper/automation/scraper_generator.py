"""
Automated scraper generation with compliance-first approach.
Generates scrapers based on site structure analysis and templates.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .compliance_validator import ComplianceValidator
from .models import (
    ComplianceValidationResult,
    ScraperResult,
    SiteStructure,
    TestResults,
)
from .structure_analyzer import SiteStructureAnalyzer
from .template_engine import ScraperTemplateEngine
from .testing_framework import AutomatedTestingFramework

logger = logging.getLogger(__name__)


class ScraperGenerator:
    """
    Main class for automated scraper generation.
    Implements compliance-first approach with template-based generation.
    """

    def __init__(self):
        self.compliance_validator = ComplianceValidator()
        self.structure_analyzer = SiteStructureAnalyzer()
        self.template_engine = ScraperTemplateEngine()
        self.testing_framework = AutomatedTestingFramework()
        self.generation_history: List[ScraperResult] = []

    async def generate_scraper_for_domain(
        self, domain: str, source_config: Dict = None
    ) -> ScraperResult:
        """
        Complete pipeline for new source integration.

        Args:
            domain: Target domain for scraper generation
            source_config: Optional configuration for the source

        Returns:
            ScraperResult with generated scraper and validation results
        """
        logger.info(f"🚀 Starting scraper generation for domain: {domain}")

        if source_config is None:
            source_config = {}

        try:
            # 1. MANDATORY: Compliance validation
            logger.info(f"🛡️ Validating compliance for {domain}")
            compliance_result = await self.compliance_validator.validate_source(domain)

            if not compliance_result.is_compliant:
                logger.error(f"❌ Compliance validation failed for {domain}")
                logger.error(f"Violations: {compliance_result.violations}")
                return ScraperResult(
                    domain=domain,
                    scraper_code="",
                    compliance_result=compliance_result,
                    site_structure=SiteStructure(
                        domain=domain,
                        cms_type="unknown",
                        navigation={},
                        article_patterns={},
                        content_structure={},
                        complexity_score=0.0,
                    ),
                    template_used="none",
                    deployment_status="compliance_failed",
                )

            # 2. Site structure analysis
            logger.info(f"🔍 Analyzing site structure for {domain}")
            site_structure = await self.structure_analyzer.analyze_site(domain)

            # 3. Template-based scraper generation
            logger.info(f"⚙️ Generating scraper code for {domain}")
            scraper_code = await self.template_engine.generate_scraper(
                site_structure, source_config
            )

            # 4. Automated testing
            logger.info(f"🧪 Running automated tests for {domain}")
            test_results = await self.testing_framework.run_full_test_suite(
                scraper_code, domain, site_structure
            )

            # 5. Determine deployment status
            deployment_status = self._determine_deployment_status(test_results)

            # 6. Create result object
            result = ScraperResult(
                domain=domain,
                scraper_code=scraper_code,
                compliance_result=compliance_result,
                site_structure=site_structure,
                template_used=self.template_engine.last_template_used,
                test_results=test_results.model_dump() if test_results else None,
                deployment_status=deployment_status,
                generation_timestamp=datetime.now(timezone.utc),
            )

            # 7. Store in history
            self.generation_history.append(result)

            logger.info(f"✅ Scraper generation completed for {domain}")
            logger.info(f"Status: {deployment_status}")
            logger.info(f"Template used: {self.template_engine.last_template_used}")

            return result

        except Exception as e:
            logger.error(f"❌ Error during scraper generation for {domain}: {str(e)}")
            return ScraperResult(
                domain=domain,
                scraper_code="",
                compliance_result=ComplianceValidationResult(
                    is_compliant=False,
                    robots_txt_compliant=False,
                    legal_contact_verified=False,
                    terms_acceptable=False,
                    fair_use_documented=False,
                    data_minimization_applied=False,
                    violations=[f"Generation error: {str(e)}"],
                ),
                site_structure=SiteStructure(
                    domain=domain,
                    cms_type="unknown",
                    navigation={},
                    article_patterns={},
                    content_structure={},
                    complexity_score=0.0,
                ),
                template_used="none",
                deployment_status="generation_failed",
            )

    def _determine_deployment_status(self, test_results: Optional[TestResults]) -> str:
        """
        Determine deployment status based on test results.

        Args:
            test_results: Results from automated testing

        Returns:
            Deployment status string
        """
        if not test_results:
            return "testing_failed"

        if test_results.success_rate >= 0.8:
            return "ready_for_deployment"
        elif test_results.success_rate >= 0.6:
            return "needs_manual_review"
        else:
            return "testing_failed"

    async def generate_scrapers_for_multiple_domains(
        self, domains: List[str]
    ) -> List[ScraperResult]:
        """
        Generate scrapers for multiple domains.

        Args:
            domains: List of domains to process

        Returns:
            List of ScraperResult objects
        """
        logger.info(f"🚀 Starting batch scraper generation for {len(domains)} domains")

        results = []
        for domain in domains:
            try:
                result = await self.generate_scraper_for_domain(domain)
                results.append(result)
                logger.info(f"✅ Completed {domain}: {result.deployment_status}")
            except Exception as e:
                logger.error(f"❌ Failed to generate scraper for {domain}: {str(e)}")
                continue

        logger.info(f"📊 Batch generation completed: {len(results)} scrapers generated")
        return results

    def get_generation_stats(self) -> Dict:
        """
        Get statistics about scraper generation history.

        Returns:
            Dictionary with generation statistics
        """
        total_generated = len(self.generation_history)
        if total_generated == 0:
            return {
                "total_generated": 0,
                "success_rate": 0.0,
                "compliance_rate": 0.0,
                "deployment_ready": 0,
                "templates_used": {},
                "last_generation": None,
            }

        successful = sum(
            1
            for r in self.generation_history
            if r.deployment_status == "ready_for_deployment"
        )
        compliant = sum(
            1 for r in self.generation_history if r.compliance_result.is_compliant
        )

        template_usage = {}
        for result in self.generation_history:
            template = result.template_used
            template_usage[template] = template_usage.get(template, 0) + 1

        return {
            "total_generated": total_generated,
            "success_rate": successful / total_generated,
            "compliance_rate": compliant / total_generated,
            "deployment_ready": successful,
            "templates_used": template_usage,
            "last_generation": (
                self.generation_history[-1].generation_timestamp
                if self.generation_history
                else None
            ),
        }

    def get_failed_generations(self) -> List[ScraperResult]:
        """
        Get list of failed scraper generations for debugging.

        Returns:
            List of failed ScraperResult objects
        """
        return [
            r
            for r in self.generation_history
            if r.deployment_status
            in ["compliance_failed", "generation_failed", "testing_failed"]
        ]

    def clear_history(self):
        """Clear generation history."""
        self.generation_history.clear()
        logger.info("🧹 Generation history cleared")
