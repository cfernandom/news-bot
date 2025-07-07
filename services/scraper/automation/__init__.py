"""
Automated scraper generation system for PreventIA News Analytics.
Compliance-first approach with template-based generation.
"""

from .compliance_validator import ComplianceValidator
from .models import (
    ComplianceValidationResult,
    QualityScore,
    ScraperResult,
    SiteStructure,
    SourceCandidate,
    TestResults,
)
from .scraper_generator import ScraperGenerator
from .structure_analyzer import SiteStructureAnalyzer
from .template_engine import ScraperTemplateEngine
from .testing_framework import AutomatedTestingFramework

__all__ = [
    "ScraperGenerator",
    "SiteStructureAnalyzer",
    "ScraperTemplateEngine",
    "ComplianceValidator",
    "AutomatedTestingFramework",
    "ScraperResult",
    "SiteStructure",
    "ComplianceValidationResult",
    "TestResults",
    "SourceCandidate",
    "QualityScore",
]
