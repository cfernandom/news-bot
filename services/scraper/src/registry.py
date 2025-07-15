"""
Centralized scraper registry for managing all scrapers with priority system.
Handles both manual and automatic scrapers with clear precedence rules.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ScraperType(Enum):
    """Types of scrapers available in the system."""

    MANUAL = "manual"
    AUTOMATIC = "automatic"
    POSTGRES = "postgres"
    LEGACY = "legacy"


@dataclass
class ScraperInfo:
    """Information about a registered scraper."""

    name: str
    domain: str
    scraper_type: ScraperType
    module_path: str
    function_name: str
    priority: int  # Lower number = higher priority
    description: str
    last_used: Optional[datetime] = None
    success_rate: float = 0.0
    is_active: bool = True


class ScraperRegistry:
    """
    Centralized registry for all scrapers with priority management.
    Handles scraper selection, fallback strategies, and performance tracking.
    """

    def __init__(self):
        self._scrapers: Dict[str, List[ScraperInfo]] = {}
        self._initialize_scrapers()

    def _initialize_scrapers(self):
        """Initialize the registry with all known scrapers."""

        # Medical Xpress scrapers (example of consolidation)
        self.register_scraper(
            ScraperInfo(
                name="medicalxpress_manual",
                domain="medicalxpress.com",
                scraper_type=ScraperType.MANUAL,
                module_path="services.scraper.src.extractors.www_medicalxpress_breast_cancer",
                function_name="scraper__medicalxpress_com_breast_cancer",
                priority=1,
                description="Manual scraper for Medical Xpress breast cancer articles",
                is_active=True,
            )
        )

        self.register_scraper(
            ScraperInfo(
                name="medicalxpress_postgres",
                domain="medicalxpress.com",
                scraper_type=ScraperType.POSTGRES,
                module_path="services.scraper.src.extractors.medicalxpress_com_postgres",
                function_name="scrape_medical_xpress_to_postgres",
                priority=2,
                description="PostgreSQL-direct scraper for Medical Xpress (fallback)",
                is_active=False,  # Disabled by default, manual has priority
            )
        )

        # Breast Cancer Now
        self.register_scraper(
            ScraperInfo(
                name="breastcancernow_manual",
                domain="breastcancernow.org",
                scraper_type=ScraperType.MANUAL,
                module_path="services.scraper.src.extractors.www_breastcancernow_org",
                function_name="scraper__breast_cancer_now_org",
                priority=1,
                description="Manual scraper for Breast Cancer Now articles",
            )
        )

        # Breast Cancer.org
        self.register_scraper(
            ScraperInfo(
                name="breastcancer_org_manual",
                domain="breastcancer.org",
                scraper_type=ScraperType.MANUAL,
                module_path="services.scraper.src.extractors.www_breastcancer_org",
                function_name="scraper__www_breast_cancer_org",
                priority=1,
                description="Manual scraper for BreastCancer.org articles",
            )
        )

        # WebMD
        self.register_scraper(
            ScraperInfo(
                name="webmd_manual",
                domain="webmd.com",
                scraper_type=ScraperType.MANUAL,
                module_path="services.scraper.src.extractors.www_breastcancernews_features",
                function_name="scraper__webmd_breast_cancer",
                priority=1,
                description="Manual scraper for WebMD breast cancer articles",
            )
        )

        # News Medical
        self.register_scraper(
            ScraperInfo(
                name="newsmedical_manual",
                domain="news-medical.net",
                scraper_type=ScraperType.MANUAL,
                module_path="services.scraper.src.extractors.www_scraper__news_medical",
                function_name="scraper__news_medical",
                priority=1,
                description="Manual scraper for News Medical articles",
            )
        )

        # Science Daily
        self.register_scraper(
            ScraperInfo(
                name="sciencedaily_manual",
                domain="sciencedaily.com",
                scraper_type=ScraperType.MANUAL,
                module_path="services.scraper.src.extractors.www_scraper_sciencedaily",
                function_name="scraper__sciencedaily",
                priority=1,
                description="Manual scraper for Science Daily articles",
            )
        )

        # Nature
        self.register_scraper(
            ScraperInfo(
                name="nature_manual",
                domain="nature.com",
                scraper_type=ScraperType.MANUAL,
                module_path="services.scraper.src.extractors.www_nature_com_breast_cancer",
                function_name="scraper__www_nature_com_breast_cancer",
                priority=1,
                description="Manual scraper for Nature breast cancer articles",
            )
        )

        # Cure Today
        self.register_scraper(
            ScraperInfo(
                name="curetoday_manual",
                domain="curetoday.com",
                scraper_type=ScraperType.MANUAL,
                module_path="services.scraper.src.extractors.www_curetoday_com_tumor_breast",
                function_name="scraper__www_curetoday_com_tumor_breast",
                priority=1,
                description="Manual scraper for Cure Today breast cancer articles",
            )
        )

    def register_scraper(self, scraper_info: ScraperInfo):
        """Register a new scraper in the registry."""
        domain = scraper_info.domain
        if domain not in self._scrapers:
            self._scrapers[domain] = []

        self._scrapers[domain].append(scraper_info)
        # Sort by priority (lower number = higher priority)
        self._scrapers[domain].sort(key=lambda x: x.priority)

        logger.info(f"Registered scraper: {scraper_info.name} for {domain}")

    def get_scrapers_for_domain(self, domain: str) -> List[ScraperInfo]:
        """Get all scrapers for a specific domain, sorted by priority."""
        return self._scrapers.get(domain, [])

    def get_active_scrapers_for_domain(self, domain: str) -> List[ScraperInfo]:
        """Get only active scrapers for a specific domain."""
        return [s for s in self.get_scrapers_for_domain(domain) if s.is_active]

    def get_primary_scraper(self, domain: str) -> Optional[ScraperInfo]:
        """Get the primary (highest priority) scraper for a domain."""
        active_scrapers = self.get_active_scrapers_for_domain(domain)
        return active_scrapers[0] if active_scrapers else None

    def get_fallback_scrapers(self, domain: str) -> List[ScraperInfo]:
        """Get fallback scrapers for a domain (excluding primary)."""
        active_scrapers = self.get_active_scrapers_for_domain(domain)
        return active_scrapers[1:] if len(active_scrapers) > 1 else []

    def get_all_active_scrapers(self) -> List[ScraperInfo]:
        """Get all active scrapers across all domains."""
        all_scrapers = []
        for domain_scrapers in self._scrapers.values():
            all_scrapers.extend([s for s in domain_scrapers if s.is_active])
        return all_scrapers

    def get_all_primary_scrapers(self) -> List[ScraperInfo]:
        """Get primary scraper for each domain."""
        primary_scrapers = []
        for domain in self._scrapers:
            primary = self.get_primary_scraper(domain)
            if primary:
                primary_scrapers.append(primary)
        return primary_scrapers

    def disable_scraper(self, domain: str, scraper_name: str):
        """Disable a specific scraper."""
        scrapers = self.get_scrapers_for_domain(domain)
        for scraper in scrapers:
            if scraper.name == scraper_name:
                scraper.is_active = False
                logger.info(f"Disabled scraper: {scraper_name} for {domain}")
                return
        logger.warning(f"Scraper not found: {scraper_name} for {domain}")

    def enable_scraper(self, domain: str, scraper_name: str):
        """Enable a specific scraper."""
        scrapers = self.get_scrapers_for_domain(domain)
        for scraper in scrapers:
            if scraper.name == scraper_name:
                scraper.is_active = True
                logger.info(f"Enabled scraper: {scraper_name} for {domain}")
                return
        logger.warning(f"Scraper not found: {scraper_name} for {domain}")

    def update_scraper_stats(
        self, domain: str, scraper_name: str, success: bool, last_used: datetime = None
    ):
        """Update scraper performance statistics."""
        scrapers = self.get_scrapers_for_domain(domain)
        for scraper in scrapers:
            if scraper.name == scraper_name:
                scraper.last_used = last_used or datetime.now()
                # Simple success rate calculation (could be improved)
                if success:
                    scraper.success_rate = min(1.0, scraper.success_rate + 0.1)
                else:
                    scraper.success_rate = max(0.0, scraper.success_rate - 0.1)
                logger.debug(
                    f"Updated stats for {scraper_name}: success_rate={scraper.success_rate}"
                )
                return
        logger.warning(f"Scraper not found for stats update: {scraper_name}")

    def get_registry_status(self) -> Dict[str, Any]:
        """Get overall registry status and statistics."""
        total_scrapers = sum(len(scrapers) for scrapers in self._scrapers.values())
        active_scrapers = len(self.get_all_active_scrapers())
        primary_scrapers = len(self.get_all_primary_scrapers())

        domains_with_scrapers = len(self._scrapers)
        domains_with_active_scrapers = len(
            [
                domain
                for domain in self._scrapers
                if self.get_active_scrapers_for_domain(domain)
            ]
        )

        return {
            "total_scrapers": total_scrapers,
            "active_scrapers": active_scrapers,
            "primary_scrapers": primary_scrapers,
            "domains_covered": domains_with_scrapers,
            "domains_active": domains_with_active_scrapers,
            "registry_health": (
                active_scrapers / total_scrapers if total_scrapers > 0 else 0.0
            ),
        }

    def get_domain_status(self, domain: str) -> Dict[str, Any]:
        """Get detailed status for a specific domain."""
        scrapers = self.get_scrapers_for_domain(domain)
        active_scrapers = self.get_active_scrapers_for_domain(domain)
        primary = self.get_primary_scraper(domain)

        return {
            "domain": domain,
            "total_scrapers": len(scrapers),
            "active_scrapers": len(active_scrapers),
            "primary_scraper": primary.name if primary else None,
            "fallback_count": len(self.get_fallback_scrapers(domain)),
            "scrapers": [
                {
                    "name": s.name,
                    "type": s.scraper_type.value,
                    "priority": s.priority,
                    "active": s.is_active,
                    "success_rate": s.success_rate,
                    "last_used": s.last_used.isoformat() if s.last_used else None,
                }
                for s in scrapers
            ],
        }


# Global registry instance
scraper_registry = ScraperRegistry()


def get_scraper_registry() -> ScraperRegistry:
    """Get the global scraper registry instance."""
    return scraper_registry
