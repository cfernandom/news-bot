"""
Data models for automated scraper generation system.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ComplianceValidationResult(BaseModel):
    """Result of compliance validation for a source."""

    is_compliant: bool
    robots_txt_compliant: bool
    legal_contact_verified: bool
    terms_acceptable: bool
    fair_use_documented: bool
    data_minimization_applied: bool
    violations: List[str] = []
    crawl_delay: Optional[float] = None


class SiteStructure(BaseModel):
    """Analyzed structure of a website."""

    domain: str
    cms_type: str
    navigation: Dict[str, Any]
    article_patterns: Dict[str, str]
    content_structure: Dict[str, Any]
    complexity_score: float
    detected_selectors: Dict[str, List[str]] = {}
    javascript_heavy: bool = False
    requires_playwright: bool = False


class SourceQualityMetrics(BaseModel):
    """Quality metrics for source evaluation."""

    content_freshness: float
    content_volume: float
    content_structure: float
    update_frequency: float


class SourceEvaluationResult(BaseModel):
    """Result of source discovery and evaluation."""

    domain: str
    compliance_result: ComplianceValidationResult
    content_quality: SourceQualityMetrics
    technical_quality: SourceQualityMetrics
    medical_relevance: float
    overall_score: float
    recommendation: str
    evaluation_timestamp: datetime


class ScraperResult(BaseModel):
    """Result of scraper generation process."""

    domain: str
    scraper_code: str
    compliance_result: ComplianceValidationResult
    site_structure: SiteStructure
    template_used: str
    test_results: Optional[Dict[str, Any]] = None
    deployment_status: str = "pending"
    generation_timestamp: datetime = datetime.now(timezone.utc)
    performance_metrics: Dict[str, float] = {}


class SourceCandidate(BaseModel):
    """Candidate source for automated scraping."""

    domain: str
    relevance_score: float
    quality_score: float
    discovery_method: str
    compliance_status: Optional[str] = None
    estimated_articles_per_day: Optional[int] = None
    language: str = "en"
    country: str = "US"


class QualityScore(BaseModel):
    """Quality assessment for a news source."""

    content_quality: float
    update_frequency: float
    site_reliability: float
    information_credibility: float
    technical_compatibility: float
    overall_score: float = 0.0

    def __init__(self, **data):
        super().__init__(**data)
        self.overall_score = (
            self.content_quality
            + self.update_frequency
            + self.site_reliability
            + self.information_credibility
            + self.technical_compatibility
        ) / 5.0


class TestResults(BaseModel):
    """Results of automated scraper testing."""

    compliance_passed: bool
    functionality_passed: bool
    performance_passed: bool
    data_quality_passed: bool
    error_handling_passed: bool
    success_rate: float
    detailed_results: Dict[str, Any] = {}
    test_timestamp: datetime = datetime.now(timezone.utc)


class DeploymentResult(BaseModel):
    """Result of scraper deployment."""

    domain: str
    deployment_status: str
    monitoring_enabled: bool
    health_check_scheduled: bool
    deployment_timestamp: datetime = datetime.now(timezone.utc)
    errors: List[str] = []


class HealthStatus(BaseModel):
    """Health status of a deployed scraper."""

    domain: str
    is_operational: bool
    performance_metrics: Dict[str, float]
    error_rate: float
    compliance_status: str
    last_successful_run: Optional[datetime] = None
    last_check: datetime = datetime.now(timezone.utc)
