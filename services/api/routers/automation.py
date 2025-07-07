"""
FastAPI router for automated scraper generation endpoints.
Provides API access to the scraper automation system.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from services.scraper.automation import (
    ComplianceValidationResult,
    ComplianceValidator,
    ScraperGenerator,
    ScraperResult,
    SiteStructure,
    SiteStructureAnalyzer,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/automation", tags=["Scraper Automation"])

# Global automation instances
scraper_generator = ScraperGenerator()
structure_analyzer = SiteStructureAnalyzer()
compliance_validator = ComplianceValidator()


# Request/Response Models
class GenerateScraperRequest(BaseModel):
    """Request model for scraper generation."""

    domain: str = Field(..., description="Domain to generate scraper for")
    language: str = Field(default="en", description="Content language")
    country: str = Field(default="US", description="Content country")
    max_articles: int = Field(default=30, description="Maximum articles to scrape")
    crawl_delay: int = Field(default=2, description="Delay between requests in seconds")


class AnalyzeDomainRequest(BaseModel):
    """Request model for domain analysis."""

    domain: str = Field(..., description="Domain to analyze")


class ComplianceCheckRequest(BaseModel):
    """Request model for compliance validation."""

    domain: str = Field(..., description="Domain to validate")


class ScraperGenerationResponse(BaseModel):
    """Response model for scraper generation."""

    domain: str
    status: str
    template_used: str
    compliance_result: Dict[str, Any]
    site_structure: Dict[str, Any]
    test_results: Optional[Dict[str, Any]]
    code_preview: str
    generation_timestamp: datetime
    deployment_ready: bool


class AutomationStatsResponse(BaseModel):
    """Response model for automation statistics."""

    total_generated: int
    success_rate: float
    compliance_rate: float
    deployment_ready: int
    templates_used: Dict[str, int]
    last_generation: Optional[datetime]


# Endpoints
@router.post("/generate-scraper", response_model=ScraperGenerationResponse)
async def generate_scraper(
    request: GenerateScraperRequest, background_tasks: BackgroundTasks
) -> ScraperGenerationResponse:
    """
    Generate a scraper for the specified domain.

    This endpoint analyzes the domain, validates compliance,
    generates scraper code, and runs automated tests.
    """
    logger.info(f"🤖 Generating scraper for domain: {request.domain}")

    try:
        # Generate scraper
        result = await scraper_generator.generate_scraper_for_domain(
            request.domain,
            {
                "language": request.language,
                "country": request.country,
                "max_articles": request.max_articles,
                "crawl_delay": request.crawl_delay,
            },
        )

        # Create code preview (first 20 lines)
        code_lines = result.scraper_code.split("\n")
        code_preview = "\n".join(code_lines[:20])
        if len(code_lines) > 20:
            code_preview += f"\n... ({len(code_lines)} total lines)"

        # Determine deployment readiness
        deployment_ready = result.deployment_status == "ready_for_deployment"

        logger.info(f"✅ Scraper generation completed for {request.domain}")
        logger.info(f"Status: {result.deployment_status}, Ready: {deployment_ready}")

        return ScraperGenerationResponse(
            domain=result.domain,
            status=result.deployment_status,
            template_used=result.template_used,
            compliance_result=result.compliance_result.dict(),
            site_structure=result.site_structure.dict(),
            test_results=result.test_results,
            code_preview=code_preview,
            generation_timestamp=result.generation_timestamp,
            deployment_ready=deployment_ready,
        )

    except Exception as e:
        logger.error(f"❌ Error generating scraper for {request.domain}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate scraper: {str(e)}"
        )


@router.post("/analyze-domain", response_model=Dict[str, Any])
async def analyze_domain(request: AnalyzeDomainRequest) -> Dict[str, Any]:
    """
    Analyze domain structure without generating scraper.

    Provides detailed analysis of the website structure,
    CMS type detection, and complexity assessment.
    """
    logger.info(f"🔍 Analyzing domain: {request.domain}")

    try:
        site_structure = await structure_analyzer.analyze_site(request.domain)

        logger.info(f"✅ Domain analysis completed for {request.domain}")

        return {
            "domain": site_structure.domain,
            "cms_type": site_structure.cms_type,
            "complexity_score": site_structure.complexity_score,
            "javascript_heavy": site_structure.javascript_heavy,
            "requires_playwright": site_structure.requires_playwright,
            "article_patterns_count": len(site_structure.article_patterns),
            "detected_selectors_count": len(site_structure.detected_selectors),
            "navigation_links": len(site_structure.navigation.get("main_nav", [])),
            "content_structure": site_structure.content_structure,
            "analysis_timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error(f"❌ Error analyzing domain {request.domain}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze domain: {str(e)}"
        )


@router.post("/validate-compliance", response_model=Dict[str, Any])
async def validate_compliance(request: ComplianceCheckRequest) -> Dict[str, Any]:
    """
    Validate domain compliance without full scraper generation.

    Checks robots.txt, legal contact, terms of service,
    and other compliance requirements.
    """
    logger.info(f"🛡️ Validating compliance for domain: {request.domain}")

    try:
        compliance_result = await compliance_validator.validate_source(request.domain)

        logger.info(f"✅ Compliance validation completed for {request.domain}")

        return {
            "domain": request.domain,
            "is_compliant": compliance_result.is_compliant,
            "robots_txt_compliant": compliance_result.robots_txt_compliant,
            "legal_contact_verified": compliance_result.legal_contact_verified,
            "terms_acceptable": compliance_result.terms_acceptable,
            "fair_use_documented": compliance_result.fair_use_documented,
            "data_minimization_applied": compliance_result.data_minimization_applied,
            "violations": compliance_result.violations,
            "crawl_delay": compliance_result.crawl_delay,
            "validation_timestamp": datetime.utcnow(),
        }

    except Exception as e:
        logger.error(f"❌ Error validating compliance for {request.domain}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to validate compliance: {str(e)}"
        )


@router.get("/stats", response_model=AutomationStatsResponse)
async def get_automation_stats() -> AutomationStatsResponse:
    """
    Get automation system statistics.

    Returns metrics about scraper generation history,
    success rates, and template usage.
    """
    logger.info("📊 Retrieving automation statistics")

    try:
        stats = scraper_generator.get_generation_stats()

        return AutomationStatsResponse(
            total_generated=stats["total_generated"],
            success_rate=stats["success_rate"],
            compliance_rate=stats["compliance_rate"],
            deployment_ready=stats["deployment_ready"],
            templates_used=stats["templates_used"],
            last_generation=stats["last_generation"],
        )

    except Exception as e:
        logger.error(f"❌ Error retrieving automation stats: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve statistics: {str(e)}"
        )


@router.get("/templates", response_model=Dict[str, List[str]])
async def get_available_templates() -> Dict[str, List[str]]:
    """
    Get list of available scraper templates.

    Returns template names and their descriptions.
    """
    logger.info("📋 Retrieving available templates")

    templates_info = {
        "available_templates": [
            "wordpress",
            "drupal",
            "custom_medical",
            "news_site",
            "generic_article",
            "generic",
        ],
        "template_descriptions": [
            "WordPress CMS sites",
            "Drupal CMS sites",
            "Medical/health news sites",
            "General news sites",
            "Article-based sites",
            "Generic fallback template",
        ],
    }

    return templates_info


@router.post("/batch-generate", response_model=List[ScraperGenerationResponse])
async def batch_generate_scrapers(
    domains: List[str], background_tasks: BackgroundTasks
) -> List[ScraperGenerationResponse]:
    """
    Generate scrapers for multiple domains in batch.

    Processes multiple domains and returns results for each.
    Limited to 10 domains per request to prevent overload.
    """
    if len(domains) > 10:
        raise HTTPException(
            status_code=400, detail="Maximum 10 domains allowed per batch request"
        )

    logger.info(f"🔄 Batch generating scrapers for {len(domains)} domains")

    try:
        results = []

        for domain in domains:
            try:
                # Generate scraper with default config
                result = await scraper_generator.generate_scraper_for_domain(domain)

                # Create code preview
                code_lines = result.scraper_code.split("\n")
                code_preview = "\n".join(code_lines[:20])
                if len(code_lines) > 20:
                    code_preview += f"\n... ({len(code_lines)} total lines)"

                deployment_ready = result.deployment_status == "ready_for_deployment"

                results.append(
                    ScraperGenerationResponse(
                        domain=result.domain,
                        status=result.deployment_status,
                        template_used=result.template_used,
                        compliance_result=result.compliance_result.dict(),
                        site_structure=result.site_structure.dict(),
                        test_results=result.test_results,
                        code_preview=code_preview,
                        generation_timestamp=result.generation_timestamp,
                        deployment_ready=deployment_ready,
                    )
                )

                logger.info(f"✅ Completed batch item: {domain}")

            except Exception as e:
                logger.error(f"❌ Failed batch item {domain}: {str(e)}")
                # Continue with other domains even if one fails
                continue

        logger.info(
            f"🎯 Batch generation completed: {len(results)}/{len(domains)} successful"
        )

        return results

    except Exception as e:
        logger.error(f"❌ Error in batch generation: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Batch generation failed: {str(e)}"
        )


@router.delete("/clear-cache")
async def clear_automation_cache() -> Dict[str, str]:
    """
    Clear automation system caches.

    Clears analysis cache, compliance cache, and generation history.
    """
    logger.info("🧹 Clearing automation caches")

    try:
        # Clear all caches
        structure_analyzer.clear_cache()
        compliance_validator.clear_cache()
        scraper_generator.clear_history()

        logger.info("✅ Automation caches cleared")

        return {
            "message": "Automation caches cleared successfully",
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"❌ Error clearing caches: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear caches: {str(e)}")


@router.get("/health")
async def automation_health_check() -> Dict[str, Any]:
    """
    Health check for automation system.

    Verifies that all automation components are working.
    """
    logger.info("🔍 Performing automation health check")

    health_status = {
        "automation_system": "healthy",
        "scraper_generator": "ready",
        "structure_analyzer": "ready",
        "compliance_validator": "ready",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
    }

    # Quick component test
    try:
        # Test stats retrieval
        stats = scraper_generator.get_generation_stats()
        health_status["generation_history"] = (
            f"{stats['total_generated']} scrapers generated"
        )

        logger.info("✅ Automation health check passed")

    except Exception as e:
        logger.error(f"❌ Automation health check failed: {str(e)}")
        health_status["automation_system"] = "unhealthy"
        health_status["error"] = str(e)

    return health_status
