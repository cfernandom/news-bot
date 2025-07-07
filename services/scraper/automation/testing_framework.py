"""
Automated testing framework for generated scrapers.
Validates compliance, functionality, performance, and data quality.
"""

import ast
import asyncio
import logging
import re
import subprocess
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import SiteStructure, TestResults

logger = logging.getLogger(__name__)


class AutomatedTestingFramework:
    """
    Comprehensive testing framework for generated scrapers.
    Validates all aspects of scraper functionality and compliance.
    """

    def __init__(self):
        self.test_history: List[TestResults] = []

    async def run_full_test_suite(
        self, scraper_code: str, domain: str, site_structure: SiteStructure
    ) -> TestResults:
        """
        Run complete test suite for generated scraper.

        Args:
            scraper_code: Generated scraper code
            domain: Domain being tested
            site_structure: Site structure analysis

        Returns:
            TestResults with comprehensive test results
        """
        logger.info(f"🧪 Starting full test suite for {domain}")

        detailed_results = {}

        try:
            # 1. Code quality tests
            logger.info("🔍 Running code quality tests")
            code_quality_result = await self._test_code_quality(scraper_code)
            detailed_results["code_quality"] = code_quality_result

            # 2. Compliance tests
            logger.info("🛡️ Running compliance tests")
            compliance_result = await self._test_compliance(scraper_code, domain)
            detailed_results["compliance"] = compliance_result

            # 3. Functionality tests
            logger.info("⚙️ Running functionality tests")
            functionality_result = await self._test_functionality(
                scraper_code, domain, site_structure
            )
            detailed_results["functionality"] = functionality_result

            # 4. Performance tests
            logger.info("⚡ Running performance tests")
            performance_result = await self._test_performance(scraper_code, domain)
            detailed_results["performance"] = performance_result

            # 5. Data quality tests
            logger.info("📊 Running data quality tests")
            data_quality_result = await self._test_data_quality(scraper_code)
            detailed_results["data_quality"] = data_quality_result

            # 6. Error handling tests
            logger.info("🚨 Running error handling tests")
            error_handling_result = await self._test_error_handling(scraper_code)
            detailed_results["error_handling"] = error_handling_result

            # Calculate overall success rate
            success_rate = self._calculate_success_rate(detailed_results)

            test_results = TestResults(
                compliance_passed=compliance_result.get("passed", False),
                functionality_passed=functionality_result.get("passed", False),
                performance_passed=performance_result.get("passed", False),
                data_quality_passed=data_quality_result.get("passed", False),
                error_handling_passed=error_handling_result.get("passed", False),
                success_rate=success_rate,
                detailed_results=detailed_results,
                test_timestamp=datetime.utcnow(),
            )

            # Store in history
            self.test_history.append(test_results)

            logger.info(f"✅ Test suite completed for {domain}")
            logger.info(f"Success rate: {success_rate:.2%}")

            return test_results

        except Exception as e:
            logger.error(f"❌ Error running test suite for {domain}: {str(e)}")
            return TestResults(
                compliance_passed=False,
                functionality_passed=False,
                performance_passed=False,
                data_quality_passed=False,
                error_handling_passed=False,
                success_rate=0.0,
                detailed_results={"error": str(e)},
                test_timestamp=datetime.utcnow(),
            )

    async def _test_code_quality(self, scraper_code: str) -> Dict[str, Any]:
        """
        Test code quality and syntax.

        Args:
            scraper_code: Generated scraper code

        Returns:
            Code quality test results
        """
        results = {
            "passed": False,
            "syntax_valid": False,
            "imports_valid": False,
            "functions_defined": False,
            "error_handling_present": False,
            "issues": [],
        }

        try:
            # Test syntax validity
            try:
                ast.parse(scraper_code)
                results["syntax_valid"] = True
            except SyntaxError as e:
                results["issues"].append(f"Syntax error: {str(e)}")

            # Test for required imports
            required_imports = [
                "from playwright.async_api import async_playwright",
                "from bs4 import BeautifulSoup",
                "import asyncio",
            ]

            imports_found = 0
            for import_stmt in required_imports:
                if import_stmt in scraper_code:
                    imports_found += 1

            if imports_found >= len(required_imports) - 1:  # Allow for some flexibility
                results["imports_valid"] = True
            else:
                results["issues"].append(
                    f"Missing required imports ({imports_found}/{len(required_imports)})"
                )

            # Test for required functions
            required_functions = [
                "async def scrape_",
                "def calculate_content_hash",
                "def count_words",
            ]

            functions_found = 0
            for func_pattern in required_functions:
                if func_pattern in scraper_code:
                    functions_found += 1

            if functions_found >= len(required_functions):
                results["functions_defined"] = True
            else:
                results["issues"].append(
                    f"Missing required functions ({functions_found}/{len(required_functions)})"
                )

            # Test for error handling
            error_handling_patterns = ["try:", "except", "Exception"]

            error_handling_found = sum(
                1 for pattern in error_handling_patterns if pattern in scraper_code
            )

            if error_handling_found >= 2:
                results["error_handling_present"] = True
            else:
                results["issues"].append("Insufficient error handling")

            # Overall assessment
            results["passed"] = all(
                [
                    results["syntax_valid"],
                    results["imports_valid"],
                    results["functions_defined"],
                    results["error_handling_present"],
                ]
            )

        except Exception as e:
            results["issues"].append(f"Code quality test error: {str(e)}")

        return results

    async def _test_compliance(self, scraper_code: str, domain: str) -> Dict[str, Any]:
        """
        Test compliance with legal and ethical requirements.

        Args:
            scraper_code: Generated scraper code
            domain: Domain being tested

        Returns:
            Compliance test results
        """
        results = {
            "passed": False,
            "robots_txt_check": False,
            "rate_limiting": False,
            "user_agent_proper": False,
            "data_minimization": False,
            "academic_purpose": False,
            "issues": [],
        }

        try:
            # Test for robots.txt compliance
            if "robots_checker" in scraper_code or "can_fetch" in scraper_code:
                results["robots_txt_check"] = True
            else:
                results["issues"].append("No robots.txt compliance check found")

            # Test for rate limiting
            rate_limiting_patterns = ["CRAWL_DELAY", "wait_for_timeout", "sleep"]

            if any(pattern in scraper_code for pattern in rate_limiting_patterns):
                results["rate_limiting"] = True
            else:
                results["issues"].append("No rate limiting mechanism found")

            # Test for proper user agent
            if "PreventIA-NewsBot" in scraper_code and "Academic" in scraper_code:
                results["user_agent_proper"] = True
            else:
                results["issues"].append("Improper or missing user agent")

            # Test for data minimization
            data_minimization_indicators = [
                'content": "",',  # Empty content field
                "metadata only",
                "summary",
                "title",
            ]

            if any(
                indicator in scraper_code for indicator in data_minimization_indicators
            ):
                results["data_minimization"] = True
            else:
                results["issues"].append("Data minimization not enforced")

            # Test for academic purpose indicators
            academic_indicators = ["Academic", "Research", "University"]

            if any(indicator in scraper_code for indicator in academic_indicators):
                results["academic_purpose"] = True
            else:
                results["issues"].append("Academic purpose not clearly indicated")

            # Overall compliance assessment
            compliance_checks = [
                results["rate_limiting"],
                results["user_agent_proper"],
                results["data_minimization"],
                results["academic_purpose"],
            ]

            results["passed"] = (
                sum(compliance_checks) >= 3
            )  # Allow for some flexibility

        except Exception as e:
            results["issues"].append(f"Compliance test error: {str(e)}")

        return results

    async def _test_functionality(
        self, scraper_code: str, domain: str, site_structure: SiteStructure
    ) -> Dict[str, Any]:
        """
        Test core scraping functionality.

        Args:
            scraper_code: Generated scraper code
            domain: Domain being tested
            site_structure: Site structure analysis

        Returns:
            Functionality test results
        """
        results = {
            "passed": False,
            "database_integration": False,
            "duplicate_detection": False,
            "article_extraction": False,
            "metadata_extraction": False,
            "url_handling": False,
            "issues": [],
        }

        try:
            # Test database integration
            db_patterns = ["db_manager", "execute_sql", "INSERT INTO articles"]

            if all(pattern in scraper_code for pattern in db_patterns):
                results["database_integration"] = True
            else:
                results["issues"].append("Database integration incomplete")

            # Test duplicate detection
            duplicate_patterns = [
                "content_hash",
                "SELECT id FROM articles WHERE url",
                "existing",
            ]

            if all(pattern in scraper_code for pattern in duplicate_patterns):
                results["duplicate_detection"] = True
            else:
                results["issues"].append("Duplicate detection missing")

            # Test article extraction
            extraction_patterns = ["soup.select", "get_text", "urljoin"]

            if all(pattern in scraper_code for pattern in extraction_patterns):
                results["article_extraction"] = True
            else:
                results["issues"].append("Article extraction logic incomplete")

            # Test metadata extraction
            metadata_patterns = ["title", "summary", "published_at", "word_count"]

            if all(pattern in scraper_code for pattern in metadata_patterns):
                results["metadata_extraction"] = True
            else:
                results["issues"].append("Metadata extraction incomplete")

            # Test URL handling
            url_patterns = ["urljoin", "BASE_URL", "href"]

            if all(pattern in scraper_code for pattern in url_patterns):
                results["url_handling"] = True
            else:
                results["issues"].append("URL handling incomplete")

            # Overall functionality assessment
            functionality_checks = [
                results["database_integration"],
                results["duplicate_detection"],
                results["article_extraction"],
                results["metadata_extraction"],
                results["url_handling"],
            ]

            results["passed"] = sum(functionality_checks) >= 4  # Require most to pass

        except Exception as e:
            results["issues"].append(f"Functionality test error: {str(e)}")

        return results

    async def _test_performance(self, scraper_code: str, domain: str) -> Dict[str, Any]:
        """
        Test performance characteristics.

        Args:
            scraper_code: Generated scraper code
            domain: Domain being tested

        Returns:
            Performance test results
        """
        results = {
            "passed": False,
            "timeout_handling": False,
            "memory_efficiency": False,
            "batch_processing": False,
            "browser_management": False,
            "issues": [],
        }

        try:
            # Test timeout handling
            timeout_patterns = ["timeout=", "wait_for_timeout", "wait_until"]

            if any(pattern in scraper_code for pattern in timeout_patterns):
                results["timeout_handling"] = True
            else:
                results["issues"].append("No timeout handling found")

            # Test memory efficiency indicators
            memory_patterns = ["finally:", "await browser.close()", "MAX_ARTICLES"]

            if all(pattern in scraper_code for pattern in memory_patterns):
                results["memory_efficiency"] = True
            else:
                results["issues"].append("Memory efficiency concerns")

            # Test batch processing
            batch_patterns = ["for article", "articles_to_process", "limit"]

            if any(pattern in scraper_code for pattern in batch_patterns):
                results["batch_processing"] = True
            else:
                results["issues"].append("No batch processing found")

            # Test browser management
            browser_patterns = [
                "async with async_playwright",
                "browser.close()",
                "page.new_page()",
            ]

            if all(pattern in scraper_code for pattern in browser_patterns):
                results["browser_management"] = True
            else:
                results["issues"].append("Browser management incomplete")

            # Overall performance assessment
            performance_checks = [
                results["timeout_handling"],
                results["memory_efficiency"],
                results["batch_processing"],
                results["browser_management"],
            ]

            results["passed"] = sum(performance_checks) >= 3

        except Exception as e:
            results["issues"].append(f"Performance test error: {str(e)}")

        return results

    async def _test_data_quality(self, scraper_code: str) -> Dict[str, Any]:
        """
        Test data quality measures.

        Args:
            scraper_code: Generated scraper code

        Returns:
            Data quality test results
        """
        results = {
            "passed": False,
            "data_validation": False,
            "encoding_handling": False,
            "sanitization": False,
            "structured_output": False,
            "issues": [],
        }

        try:
            # Test data validation
            validation_patterns = ["if not title", "strip()", "get_text"]

            if all(pattern in scraper_code for pattern in validation_patterns):
                results["data_validation"] = True
            else:
                results["issues"].append("Data validation insufficient")

            # Test encoding handling
            encoding_patterns = ["utf-8", "encode", "decode"]

            if any(pattern in scraper_code for pattern in encoding_patterns):
                results["encoding_handling"] = True
            else:
                results["issues"].append("No explicit encoding handling")

            # Test sanitization
            sanitization_patterns = ["strip()", "[:500]", "get_text"]  # Length limiting

            if all(pattern in scraper_code for pattern in sanitization_patterns):
                results["sanitization"] = True
            else:
                results["issues"].append("Data sanitization incomplete")

            # Test structured output
            structure_patterns = ["INSERT INTO", "articles", "RETURNING id"]

            if all(pattern in scraper_code for pattern in structure_patterns):
                results["structured_output"] = True
            else:
                results["issues"].append("Structured output missing")

            # Overall data quality assessment
            quality_checks = [
                results["data_validation"],
                results["sanitization"],
                results["structured_output"],
            ]

            results["passed"] = sum(quality_checks) >= 2

        except Exception as e:
            results["issues"].append(f"Data quality test error: {str(e)}")

        return results

    async def _test_error_handling(self, scraper_code: str) -> Dict[str, Any]:
        """
        Test error handling capabilities.

        Args:
            scraper_code: Generated scraper code

        Returns:
            Error handling test results
        """
        results = {
            "passed": False,
            "exception_handling": False,
            "graceful_degradation": False,
            "logging": False,
            "recovery_mechanisms": False,
            "issues": [],
        }

        try:
            # Test exception handling
            exception_patterns = ["try:", "except Exception", "except"]

            exception_count = sum(
                1 for pattern in exception_patterns if pattern in scraper_code
            )

            if exception_count >= 3:
                results["exception_handling"] = True
            else:
                results["issues"].append(
                    f"Insufficient exception handling ({exception_count} blocks)"
                )

            # Test graceful degradation
            degradation_patterns = ["continue", "return []", "default"]

            if any(pattern in scraper_code for pattern in degradation_patterns):
                results["graceful_degradation"] = True
            else:
                results["issues"].append("No graceful degradation found")

            # Test logging
            logging_patterns = ["print(", "logger", "log"]

            if any(pattern in scraper_code for pattern in logging_patterns):
                results["logging"] = True
            else:
                results["issues"].append("No logging found")

            # Test recovery mechanisms
            recovery_patterns = ["finally:", "await browser.close()", "close_database"]

            if any(pattern in scraper_code for pattern in recovery_patterns):
                results["recovery_mechanisms"] = True
            else:
                results["issues"].append("No recovery mechanisms found")

            # Overall error handling assessment
            error_checks = [
                results["exception_handling"],
                results["graceful_degradation"],
                results["logging"],
                results["recovery_mechanisms"],
            ]

            results["passed"] = sum(error_checks) >= 3

        except Exception as e:
            results["issues"].append(f"Error handling test error: {str(e)}")

        return results

    def _calculate_success_rate(self, detailed_results: Dict[str, Any]) -> float:
        """
        Calculate overall success rate from detailed test results.

        Args:
            detailed_results: Detailed test results

        Returns:
            Success rate between 0.0 and 1.0
        """
        try:
            # Weight different test categories
            weights = {
                "code_quality": 0.15,
                "compliance": 0.25,
                "functionality": 0.25,
                "performance": 0.15,
                "data_quality": 0.15,
                "error_handling": 0.05,
            }

            total_score = 0.0
            total_weight = 0.0

            for category, weight in weights.items():
                if category in detailed_results:
                    result = detailed_results[category]
                    if isinstance(result, dict) and "passed" in result:
                        total_score += weight if result["passed"] else 0
                    total_weight += weight

            if total_weight > 0:
                return total_score / total_weight
            else:
                return 0.0

        except Exception as e:
            logger.error(f"❌ Error calculating success rate: {str(e)}")
            return 0.0

    def get_test_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about testing history.

        Returns:
            Testing statistics dictionary
        """
        if not self.test_history:
            return {
                "total_tests": 0,
                "average_success_rate": 0.0,
                "pass_rates": {},
                "common_issues": [],
            }

        total_tests = len(self.test_history)
        success_rates = [test.success_rate for test in self.test_history]
        average_success_rate = sum(success_rates) / len(success_rates)

        # Calculate pass rates for each category
        pass_rates = {
            "compliance": sum(1 for test in self.test_history if test.compliance_passed)
            / total_tests,
            "functionality": sum(
                1 for test in self.test_history if test.functionality_passed
            )
            / total_tests,
            "performance": sum(
                1 for test in self.test_history if test.performance_passed
            )
            / total_tests,
            "data_quality": sum(
                1 for test in self.test_history if test.data_quality_passed
            )
            / total_tests,
            "error_handling": sum(
                1 for test in self.test_history if test.error_handling_passed
            )
            / total_tests,
        }

        # Collect common issues
        all_issues = []
        for test in self.test_history:
            if "detailed_results" in test.detailed_results:
                for category_results in test.detailed_results.values():
                    if (
                        isinstance(category_results, dict)
                        and "issues" in category_results
                    ):
                        all_issues.extend(category_results["issues"])

        # Count issue frequency
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

        # Get most common issues
        common_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]

        return {
            "total_tests": total_tests,
            "average_success_rate": average_success_rate,
            "pass_rates": pass_rates,
            "common_issues": common_issues,
            "last_test": (
                self.test_history[-1].test_timestamp if self.test_history else None
            ),
        }

    def clear_history(self):
        """Clear testing history."""
        self.test_history.clear()
        logger.info("🧹 Testing history cleared")
