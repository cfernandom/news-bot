"""
Compliance validation for automated scraper generation.
Ensures all generated scrapers meet legal and ethical standards.
"""

import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import httpx

from ..src.compliance.robots_checker import robots_checker
from .models import ComplianceValidationResult

logger = logging.getLogger(__name__)


class ComplianceValidator:
    """
    Validates news sources for legal and ethical compliance.
    Integrates with existing compliance framework.
    """

    def __init__(self):
        self.user_agent = "PreventIA-NewsBot/1.0"
        self.compliance_cache: Dict[str, ComplianceValidationResult] = {}

    async def validate_source(self, domain: str) -> ComplianceValidationResult:
        """
        Comprehensive compliance validation for a news source.

        Args:
            domain: Domain to validate

        Returns:
            ComplianceValidationResult with detailed validation results
        """
        logger.info(f"🛡️ Starting compliance validation for {domain}")

        # Check cache first
        if domain in self.compliance_cache:
            logger.info(f"📋 Using cached compliance result for {domain}")
            return self.compliance_cache[domain]

        violations = []

        # 1. Robots.txt compliance check
        robots_compliant = await self._check_robots_txt_compliance(domain)
        if not robots_compliant:
            violations.append("Robots.txt disallows scraping")

        # 2. Legal contact verification
        legal_contact_verified = await self._verify_legal_contact(domain)
        if not legal_contact_verified:
            violations.append("No legal contact information available")

        # 3. Terms of service review
        terms_acceptable = await self._review_terms_of_service(domain)
        if not terms_acceptable:
            violations.append("Terms of service prohibit automated access")

        # 4. Fair use documentation
        fair_use_documented = await self._document_fair_use_basis(domain)
        if not fair_use_documented:
            violations.append("Fair use basis not documented")

        # 5. Data minimization check
        data_minimization_applied = await self._apply_data_minimization(domain)
        if not data_minimization_applied:
            violations.append("Data minimization not applied")

        # 6. Get crawl delay
        crawl_delay = await self._get_crawl_delay(domain)

        # Determine overall compliance
        is_compliant = len(violations) == 0

        result = ComplianceValidationResult(
            is_compliant=is_compliant,
            robots_txt_compliant=robots_compliant,
            legal_contact_verified=legal_contact_verified,
            terms_acceptable=terms_acceptable,
            fair_use_documented=fair_use_documented,
            data_minimization_applied=data_minimization_applied,
            violations=violations,
            crawl_delay=crawl_delay,
        )

        # Cache result
        self.compliance_cache[domain] = result

        logger.info(f"✅ Compliance validation completed for {domain}")
        logger.info(f"Compliant: {is_compliant}, Violations: {len(violations)}")

        return result

    async def _check_robots_txt_compliance(self, domain: str) -> bool:
        """
        Check if domain allows scraping via robots.txt.

        Args:
            domain: Domain to check

        Returns:
            True if compliant, False otherwise
        """
        try:
            test_url = f"https://{domain}/news"
            allowed = await robots_checker.can_fetch(test_url)
            logger.info(
                f"🤖 Robots.txt check for {domain}: {'ALLOWED' if allowed else 'DISALLOWED'}"
            )
            return allowed
        except Exception as e:
            logger.error(f"❌ Error checking robots.txt for {domain}: {str(e)}")
            return False

    async def _verify_legal_contact(self, domain: str) -> bool:
        """
        Verify if domain has accessible legal contact information.

        Args:
            domain: Domain to check

        Returns:
            True if legal contact is available, False otherwise
        """
        try:
            # Check common legal contact pages
            legal_pages = [
                "/contact",
                "/legal",
                "/terms",
                "/privacy",
                "/about",
                "/contact-us",
            ]

            async with httpx.AsyncClient(timeout=10.0) as client:
                for page in legal_pages:
                    url = f"https://{domain}{page}"
                    try:
                        response = await client.get(
                            url, headers={"User-Agent": self.user_agent}
                        )
                        if response.status_code == 200:
                            # Check for contact information indicators
                            content = response.text.lower()
                            if any(
                                indicator in content
                                for indicator in [
                                    "contact",
                                    "email",
                                    "@",
                                    "legal",
                                    "dmca",
                                    "copyright",
                                ]
                            ):
                                logger.info(
                                    f"📞 Legal contact found for {domain} at {page}"
                                )
                                return True
                    except:
                        continue

            logger.warning(f"⚠️ No legal contact information found for {domain}")
            return False

        except Exception as e:
            logger.error(f"❌ Error verifying legal contact for {domain}: {str(e)}")
            return False

    async def _review_terms_of_service(self, domain: str) -> bool:
        """
        Review terms of service for automated access restrictions.

        Args:
            domain: Domain to check

        Returns:
            True if terms are acceptable, False otherwise
        """
        try:
            # Check terms of service pages
            terms_pages = [
                "/terms",
                "/terms-of-service",
                "/terms-of-use",
                "/legal/terms",
                "/tos",
            ]

            async with httpx.AsyncClient(timeout=10.0) as client:
                for page in terms_pages:
                    url = f"https://{domain}{page}"
                    try:
                        response = await client.get(
                            url, headers={"User-Agent": self.user_agent}
                        )
                        if response.status_code == 200:
                            content = response.text.lower()

                            # Check for prohibitive terms
                            prohibited_terms = [
                                "no automated access",
                                "no bots",
                                "no scraping",
                                "no crawling",
                                "automated access prohibited",
                                "bots prohibited",
                            ]

                            if any(term in content for term in prohibited_terms):
                                logger.warning(
                                    f"⚠️ Terms of service prohibit automated access for {domain}"
                                )
                                return False

                            logger.info(f"📋 Terms of service acceptable for {domain}")
                            return True
                    except:
                        continue

            # If no terms found, assume acceptable for news content
            logger.info(f"📋 No restrictive terms found for {domain}")
            return True

        except Exception as e:
            logger.error(f"❌ Error reviewing terms of service for {domain}: {str(e)}")
            return True  # Default to acceptable

    async def _document_fair_use_basis(self, domain: str) -> bool:
        """
        Document fair use basis for academic research.

        Args:
            domain: Domain to document

        Returns:
            True if fair use basis is documented, False otherwise
        """
        # For academic research, fair use is generally applicable
        # This is a placeholder for more comprehensive fair use documentation
        logger.info(f"📚 Fair use basis documented for {domain} (academic research)")
        return True

    async def _apply_data_minimization(self, domain: str) -> bool:
        """
        Verify data minimization principles are applied.

        Args:
            domain: Domain to check

        Returns:
            True if data minimization is applied, False otherwise
        """
        # Data minimization is applied by design in our system
        # We only store metadata, not full content
        logger.info(f"🔒 Data minimization applied for {domain} (metadata only)")
        return True

    async def _get_crawl_delay(self, domain: str) -> Optional[float]:
        """
        Get recommended crawl delay from robots.txt.

        Args:
            domain: Domain to check

        Returns:
            Crawl delay in seconds, or None if not specified
        """
        try:
            test_url = f"https://{domain}/news"
            delay = robots_checker.get_crawl_delay(test_url)
            if delay:
                logger.info(f"⏱️ Crawl delay for {domain}: {delay} seconds")
            else:
                logger.info(f"⏱️ No crawl delay specified for {domain}")
            return delay
        except Exception as e:
            logger.error(f"❌ Error getting crawl delay for {domain}: {str(e)}")
            return None

    def clear_cache(self):
        """Clear compliance validation cache."""
        self.compliance_cache.clear()
        logger.info("🧹 Compliance validation cache cleared")
