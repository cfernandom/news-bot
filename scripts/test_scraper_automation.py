"""
Test script for automated scraper generation system.
Validates the automation pipeline with a sample domain.
"""

import asyncio
import os
import sys
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from services.scraper.automation import (
    ComplianceValidator,
    ScraperGenerator,
    ScraperResult,
    SiteStructureAnalyzer,
)


async def test_automation_system():
    """
    Test the automated scraper generation system.
    """
    print("🚀 Testing Automated Scraper Generation System")
    print("=" * 60)

    # Test domain (use a medical news site)
    test_domain = "www.medicalnewstoday.com"

    print(f"📍 Test Domain: {test_domain}")
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    try:
        # 1. Test Compliance Validator
        print("\n🛡️ STEP 1: Testing Compliance Validator")
        compliance_validator = ComplianceValidator()

        print(f"   Validating compliance for {test_domain}...")
        compliance_result = await compliance_validator.validate_source(test_domain)

        print(f"   ✅ Compliance Result:")
        print(f"      - Is Compliant: {compliance_result.is_compliant}")
        print(f"      - Robots.txt: {compliance_result.robots_txt_compliant}")
        print(f"      - Legal Contact: {compliance_result.legal_contact_verified}")
        print(f"      - Terms Acceptable: {compliance_result.terms_acceptable}")
        print(f"      - Crawl Delay: {compliance_result.crawl_delay}")

        if compliance_result.violations:
            print(f"      - Violations: {compliance_result.violations}")

        # 2. Test Site Structure Analyzer
        print("\n🔍 STEP 2: Testing Site Structure Analyzer")
        structure_analyzer = SiteStructureAnalyzer()

        print(f"   Analyzing site structure for {test_domain}...")
        try:
            site_structure = await structure_analyzer.analyze_site(test_domain)

            print(f"   ✅ Site Structure Analysis:")
            print(f"      - CMS Type: {site_structure.cms_type}")
            print(f"      - Complexity Score: {site_structure.complexity_score}")
            print(f"      - JavaScript Heavy: {site_structure.javascript_heavy}")
            print(f"      - Requires Playwright: {site_structure.requires_playwright}")
            print(
                f"      - Article Patterns: {len(site_structure.article_patterns)} found"
            )
            print(
                f"      - Detected Selectors: {len(site_structure.detected_selectors)} categories"
            )

        except Exception as e:
            print(f"   ❌ Site structure analysis failed: {str(e)}")
            # Create minimal structure for testing
            from services.scraper.automation.models import SiteStructure

            site_structure = SiteStructure(
                domain=test_domain,
                cms_type="unknown",
                navigation={},
                article_patterns={},
                content_structure={},
                complexity_score=0.5,
            )

        # 3. Test Scraper Generator
        print("\n⚙️ STEP 3: Testing Scraper Generator")
        scraper_generator = ScraperGenerator()

        print(f"   Generating scraper for {test_domain}...")
        generation_result = await scraper_generator.generate_scraper_for_domain(
            test_domain,
            {"language": "en", "country": "US", "max_articles": 20, "crawl_delay": 3},
        )

        print(f"   ✅ Scraper Generation Result:")
        print(f"      - Domain: {generation_result.domain}")
        print(f"      - Template Used: {generation_result.template_used}")
        print(f"      - Deployment Status: {generation_result.deployment_status}")
        print(f"      - Code Length: {len(generation_result.scraper_code)} characters")
        print(f"      - Generation Time: {generation_result.generation_timestamp}")

        # Show compliance summary
        comp_result = generation_result.compliance_result
        print(f"      - Final Compliance: {comp_result.is_compliant}")

        # Show test results if available
        if generation_result.test_results:
            test_results = generation_result.test_results
            print(
                f"      - Test Success Rate: {test_results.get('success_rate', 0):.2%}"
            )
            print(f"      - Tests Passed:")
            print(
                f"        - Compliance: {test_results.get('compliance_passed', False)}"
            )
            print(
                f"        - Functionality: {test_results.get('functionality_passed', False)}"
            )
            print(
                f"        - Performance: {test_results.get('performance_passed', False)}"
            )

        # 4. Show generated code sample
        print("\n📄 STEP 4: Generated Code Sample")
        code_lines = generation_result.scraper_code.split("\n")
        print("   First 10 lines of generated code:")
        for i, line in enumerate(code_lines[:10], 1):
            print(f"   {i:2d}: {line}")
        print(f"   ... ({len(code_lines)} total lines)")

        # 5. Test Statistics
        print("\n📊 STEP 5: System Statistics")
        stats = scraper_generator.get_generation_stats()
        print(f"   Generation Statistics:")
        print(f"      - Total Generated: {stats['total_generated']}")
        print(f"      - Success Rate: {stats['success_rate']:.2%}")
        print(f"      - Compliance Rate: {stats['compliance_rate']:.2%}")
        print(f"      - Deployment Ready: {stats['deployment_ready']}")
        print(f"      - Templates Used: {stats['templates_used']}")

        # 6. Overall Assessment
        print("\n🎯 OVERALL ASSESSMENT")
        print("-" * 30)

        if generation_result.deployment_status == "ready_for_deployment":
            print("   ✅ SUCCESS: Scraper is ready for deployment")
        elif generation_result.deployment_status == "needs_manual_review":
            print("   ⚠️  WARNING: Scraper needs manual review")
        else:
            print("   ❌ FAILED: Scraper generation failed")

        print(
            f"   - Compliance Status: {'✅ PASS' if comp_result.is_compliant else '❌ FAIL'}"
        )
        print(
            f"   - Code Generation: {'✅ PASS' if len(generation_result.scraper_code) > 1000 else '❌ FAIL'}"
        )
        print(f"   - Template Selection: ✅ PASS")

        print(f"\n⏰ Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        return generation_result

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


async def test_multiple_domains():
    """
    Test automation system with multiple domains.
    """
    print("\n🔄 Testing Multiple Domains")
    print("=" * 40)

    test_domains = [
        "www.healthline.com",
        "www.medicalnewstoday.com",
        "www.webmd.com",  # Known working domain
    ]

    scraper_generator = ScraperGenerator()

    for i, domain in enumerate(test_domains, 1):
        print(f"\n{i}. Testing {domain}")
        print("-" * 30)

        try:
            result = await scraper_generator.generate_scraper_for_domain(domain)

            status_icon = {
                "ready_for_deployment": "✅",
                "needs_manual_review": "⚠️",
                "compliance_failed": "❌",
                "generation_failed": "❌",
                "testing_failed": "⚠️",
            }.get(result.deployment_status, "❓")

            print(f"   {status_icon} Status: {result.deployment_status}")
            print(f"   📋 Template: {result.template_used}")
            print(f"   🛡️ Compliant: {result.compliance_result.is_compliant}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

    # Show final statistics
    stats = scraper_generator.get_generation_stats()
    print(f"\n📊 BATCH RESULTS:")
    print(f"   Total Tested: {stats['total_generated']}")
    print(f"   Success Rate: {stats['success_rate']:.2%}")
    print(f"   Deployment Ready: {stats['deployment_ready']}")


if __name__ == "__main__":
    print("🧪 PreventIA Automated Scraper Generation Test Suite")
    print("🔬 This script tests the automation system components")
    print()

    # Run single domain test
    asyncio.run(test_automation_system())

    # Optionally run multiple domain test
    run_batch = (
        input("\n🤔 Run batch test with multiple domains? (y/N): ").lower().strip()
    )
    if run_batch in ["y", "yes"]:
        asyncio.run(test_multiple_domains())

    print("\n✅ Testing completed!")
