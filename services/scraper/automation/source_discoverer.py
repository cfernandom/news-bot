"""
Source discovery and evaluation system for automated scraper generation.
Discovers new medical news sources and evaluates their suitability for scraping.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup

from .compliance_validator import ComplianceValidator
from .models import (
    ComplianceValidationResult,
    SourceEvaluationResult,
    SourceQualityMetrics,
)
from .structure_analyzer import SiteStructureAnalyzer

logger = logging.getLogger(__name__)


class SourceDiscoverer:
    """
    Discovers and evaluates new medical news sources for potential scraping.
    Focuses on breast cancer and medical content with compliance-first approach.
    """

    def __init__(self):
        self.compliance_validator = ComplianceValidator()
        self.structure_analyzer = SiteStructureAnalyzer()
        self.discovery_history: List[SourceEvaluationResult] = []

        # Medical content keywords for relevance scoring
        self.medical_keywords = {
            "breast_cancer": ["breast cancer", "mammography", "mastectomy", "oncology"],
            "medical_general": [
                "health",
                "medical",
                "medicine",
                "treatment",
                "diagnosis",
            ],
            "research": ["clinical trial", "research", "study", "publication"],
            "news": ["news", "article", "report", "breaking", "update"],
        }

        # Common medical news site patterns
        self.medical_site_patterns = [
            "health",
            "medical",
            "medicine",
            "cancer",
            "oncology",
            "news",
            "research",
            "clinical",
            "hospital",
            "clinic",
        ]

    async def discover_sources_from_search(
        self, search_terms: List[str], max_sources: int = 10
    ) -> List[SourceEvaluationResult]:
        """
        Discover sources using search terms (simulated - would integrate with search APIs).

        Args:
            search_terms: Terms to search for
            max_sources: Maximum number of sources to evaluate

        Returns:
            List of evaluated sources
        """
        logger.info(f"🔍 Starting source discovery with terms: {search_terms}")

        # Simulate search results (in production, would use search APIs)
        potential_sources = await self._simulate_search_results(search_terms)

        # Evaluate each discovered source
        evaluated_sources = []
        for domain in potential_sources[:max_sources]:
            try:
                evaluation = await self.evaluate_source(domain)
                evaluated_sources.append(evaluation)
                logger.info(f"✅ Evaluated {domain}: {evaluation.overall_score:.2f}")
            except Exception as e:
                logger.error(f"❌ Error evaluating {domain}: {str(e)}")
                continue

        # Sort by overall score
        evaluated_sources.sort(key=lambda x: x.overall_score, reverse=True)

        logger.info(
            f"📊 Discovery completed: {len(evaluated_sources)} sources evaluated"
        )
        return evaluated_sources

    async def _simulate_search_results(self, search_terms: List[str]) -> List[str]:
        """Simulate search results for demonstration (replace with actual search API)."""
        # Example medical news domains (would be dynamically discovered)
        example_domains = [
            "healthline.com",
            "medicalnewstoday.com",
            "webmd.com",
            "mayoclinic.org",
            "cancer.gov",
            "breastcancer.org",
            "cancerresearchuk.org",
            "mdanderson.org",
            "mskcc.org",
            "dana-farber.org",
        ]

        # Filter based on search terms (basic simulation)
        relevant_domains = []
        for domain in example_domains:
            for term in search_terms:
                if any(keyword in domain.lower() for keyword in term.lower().split()):
                    relevant_domains.append(domain)
                    break

        return relevant_domains if relevant_domains else example_domains[:5]

    async def evaluate_source(self, domain: str) -> SourceEvaluationResult:
        """
        Comprehensive evaluation of a potential source.

        Args:
            domain: Domain to evaluate

        Returns:
            SourceEvaluationResult with detailed metrics
        """
        logger.info(f"🔍 Evaluating source: {domain}")

        try:
            # 1. Basic compliance check
            compliance_result = await self.compliance_validator.validate_source(domain)

            # 2. Content analysis
            content_metrics = await self._analyze_content_quality(domain)

            # 3. Technical analysis
            technical_metrics = await self._analyze_technical_quality(domain)

            # 4. Medical relevance scoring
            relevance_score = await self._calculate_medical_relevance(domain)

            # 5. Overall scoring
            overall_score = self._calculate_overall_score(
                compliance_result, content_metrics, technical_metrics, relevance_score
            )

            # 6. Generate recommendation
            recommendation = self._generate_recommendation(
                overall_score, compliance_result
            )

            result = SourceEvaluationResult(
                domain=domain,
                compliance_result=compliance_result,
                content_quality=content_metrics,
                technical_quality=technical_metrics,
                medical_relevance=relevance_score,
                overall_score=overall_score,
                recommendation=recommendation,
                evaluation_timestamp=datetime.utcnow(),
            )

            self.discovery_history.append(result)
            return result

        except Exception as e:
            logger.error(f"❌ Error during source evaluation for {domain}: {str(e)}")
            # Return failed evaluation
            return SourceEvaluationResult(
                domain=domain,
                compliance_result=ComplianceValidationResult(
                    is_compliant=False,
                    robots_txt_compliant=False,
                    legal_contact_verified=False,
                    terms_acceptable=False,
                    fair_use_documented=False,
                    data_minimization_applied=False,
                    violations=[f"Evaluation error: {str(e)}"],
                ),
                content_quality=SourceQualityMetrics(
                    content_freshness=0.0,
                    content_volume=0.0,
                    content_structure=0.0,
                    update_frequency=0.0,
                ),
                technical_quality=SourceQualityMetrics(
                    page_load_speed=0.0,
                    mobile_compatibility=0.0,
                    accessibility=0.0,
                    technical_reliability=0.0,
                ),
                medical_relevance=0.0,
                overall_score=0.0,
                recommendation="evaluation_failed",
                evaluation_timestamp=datetime.utcnow(),
            )

    async def _analyze_content_quality(self, domain: str) -> SourceQualityMetrics:
        """Analyze content quality metrics."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://{domain}", timeout=10) as response:
                    if response.status != 200:
                        return SourceQualityMetrics(0.0, 0.0, 0.0, 0.0)

                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")

                    # Content freshness (check for recent dates)
                    freshness = self._analyze_content_freshness(soup)

                    # Content volume (number of articles/posts)
                    volume = self._analyze_content_volume(soup)

                    # Content structure (proper HTML structure)
                    structure = self._analyze_content_structure(soup)

                    # Update frequency (estimate based on content dates)
                    frequency = self._estimate_update_frequency(soup)

                    return SourceQualityMetrics(
                        content_freshness=freshness,
                        content_volume=volume,
                        content_structure=structure,
                        update_frequency=frequency,
                    )
        except Exception as e:
            logger.error(f"Error analyzing content quality for {domain}: {str(e)}")
            return SourceQualityMetrics(0.0, 0.0, 0.0, 0.0)

    async def _analyze_technical_quality(self, domain: str) -> SourceQualityMetrics:
        """Analyze technical quality metrics."""
        try:
            # Use structure analyzer for technical analysis
            site_structure = await self.structure_analyzer.analyze_site(domain)

            # Convert structure analysis to quality metrics
            load_speed = 0.8 if site_structure.requires_playwright else 0.9
            mobile_compat = 0.8  # Assume good mobile compatibility
            accessibility = 0.7  # Moderate accessibility
            reliability = min(1.0, site_structure.complexity_score / 10.0)

            return SourceQualityMetrics(
                page_load_speed=load_speed,
                mobile_compatibility=mobile_compat,
                accessibility=accessibility,
                technical_reliability=reliability,
            )
        except Exception as e:
            logger.error(f"Error analyzing technical quality for {domain}: {str(e)}")
            return SourceQualityMetrics(0.0, 0.0, 0.0, 0.0)

    async def _calculate_medical_relevance(self, domain: str) -> float:
        """Calculate medical relevance score based on content and domain."""
        try:
            # Domain-based scoring
            domain_score = 0.0
            for pattern in self.medical_site_patterns:
                if pattern in domain.lower():
                    domain_score += 0.1

            # Content-based scoring (sample homepage)
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://{domain}", timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        content_score = self._score_medical_content(html)
                    else:
                        content_score = 0.0

            return min(1.0, domain_score + content_score)
        except Exception as e:
            logger.error(f"Error calculating medical relevance for {domain}: {str(e)}")
            return 0.0

    def _score_medical_content(self, html: str) -> float:
        """Score content based on medical keyword presence."""
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text().lower()

        total_score = 0.0
        for category, keywords in self.medical_keywords.items():
            category_score = 0.0
            for keyword in keywords:
                if keyword in text:
                    category_score += 0.1
            total_score += min(0.2, category_score)  # Max 0.2 per category

        return min(1.0, total_score)

    def _analyze_content_freshness(self, soup: BeautifulSoup) -> float:
        """Analyze content freshness based on publication dates."""
        # Look for common date patterns
        date_selectors = [
            "time[datetime]",
            ".date",
            ".published",
            ".post-date",
            '[class*="date"]',
            '[class*="time"]',
        ]

        dates_found = 0
        recent_dates = 0

        for selector in date_selectors:
            elements = soup.select(selector)
            for element in elements:
                dates_found += 1
                # Simple heuristic: if element contains recent year, consider it fresh
                if any(str(year) in element.get_text() for year in [2023, 2024, 2025]):
                    recent_dates += 1

        return recent_dates / max(1, dates_found) if dates_found > 0 else 0.5

    def _analyze_content_volume(self, soup: BeautifulSoup) -> float:
        """Analyze content volume based on number of articles/posts."""
        # Look for common article patterns
        article_selectors = [
            "article",
            ".post",
            ".article",
            ".news-item",
            '[class*="post"]',
            '[class*="article"]',
        ]

        total_articles = 0
        for selector in article_selectors:
            total_articles += len(soup.select(selector))

        # Normalize to 0-1 scale (assume 20+ articles = high volume)
        return min(1.0, total_articles / 20.0)

    def _analyze_content_structure(self, soup: BeautifulSoup) -> float:
        """Analyze content structure quality."""
        score = 0.0

        # Check for proper HTML structure
        if soup.find("header"):
            score += 0.2
        if soup.find("main") or soup.find("article"):
            score += 0.3
        if soup.find("nav"):
            score += 0.2
        if soup.find("footer"):
            score += 0.2
        if soup.find("h1"):
            score += 0.1

        return min(1.0, score)

    def _estimate_update_frequency(self, soup: BeautifulSoup) -> float:
        """Estimate update frequency based on content analysis."""
        # Simple heuristic based on presence of recent content indicators
        recent_indicators = [
            "today",
            "yesterday",
            "hours ago",
            "minutes ago",
            "breaking",
            "update",
            "latest",
        ]

        text = soup.get_text().lower()
        score = 0.0

        for indicator in recent_indicators:
            if indicator in text:
                score += 0.1

        return min(1.0, score)

    def _calculate_overall_score(
        self,
        compliance: ComplianceValidationResult,
        content: SourceQualityMetrics,
        technical: SourceQualityMetrics,
        relevance: float,
    ) -> float:
        """Calculate overall source quality score."""
        # Weighted scoring
        weights = {
            "compliance": 0.4,  # Compliance is most important
            "content": 0.3,
            "technical": 0.2,
            "relevance": 0.1,
        }

        compliance_score = 1.0 if compliance.is_compliant else 0.0
        content_score = (
            content.content_freshness
            + content.content_volume
            + content.content_structure
            + content.update_frequency
        ) / 4.0

        technical_score = (
            technical.page_load_speed
            + technical.mobile_compatibility
            + technical.accessibility
            + technical.technical_reliability
        ) / 4.0

        overall = (
            weights["compliance"] * compliance_score
            + weights["content"] * content_score
            + weights["technical"] * technical_score
            + weights["relevance"] * relevance
        )

        return round(overall, 2)

    def _generate_recommendation(
        self, overall_score: float, compliance: ComplianceValidationResult
    ) -> str:
        """Generate recommendation based on evaluation results."""
        if not compliance.is_compliant:
            return "not_recommended_compliance"
        elif overall_score >= 0.8:
            return "highly_recommended"
        elif overall_score >= 0.6:
            return "recommended"
        elif overall_score >= 0.4:
            return "conditionally_recommended"
        else:
            return "not_recommended_quality"

    def get_discovery_stats(self) -> Dict:
        """Get statistics about source discovery history."""
        if not self.discovery_history:
            return {
                "total_evaluated": 0,
                "highly_recommended": 0,
                "recommended": 0,
                "not_recommended": 0,
                "average_score": 0.0,
            }

        total = len(self.discovery_history)
        highly_recommended = sum(
            1
            for s in self.discovery_history
            if s.recommendation == "highly_recommended"
        )
        recommended = sum(
            1 for s in self.discovery_history if s.recommendation == "recommended"
        )
        not_recommended = sum(
            1 for s in self.discovery_history if "not_recommended" in s.recommendation
        )

        average_score = sum(s.overall_score for s in self.discovery_history) / total

        return {
            "total_evaluated": total,
            "highly_recommended": highly_recommended,
            "recommended": recommended,
            "not_recommended": not_recommended,
            "average_score": round(average_score, 2),
            "last_discovery": (
                self.discovery_history[-1].evaluation_timestamp
                if self.discovery_history
                else None
            ),
        }

    def get_top_sources(self, limit: int = 5) -> List[SourceEvaluationResult]:
        """Get top-rated sources from discovery history."""
        sorted_sources = sorted(
            self.discovery_history, key=lambda x: x.overall_score, reverse=True
        )
        return sorted_sources[:limit]

    def clear_history(self):
        """Clear discovery history."""
        self.discovery_history.clear()
        logger.info("🧹 Discovery history cleared")
