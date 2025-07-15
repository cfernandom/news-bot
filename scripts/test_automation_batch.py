"""
Batch test script for automated scraper generation system.
Tests multiple domains without interactive input.
"""

import asyncio
import os
import sys
from pathlib import Path

# Setup project environment (replaces manual sys.path manipulation)
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import setup_script_environment

setup_script_environment()
from datetime import datetime

from services.scraper.automation import ScraperGenerator


async def test_multiple_domains():
    """
    Test automation system with multiple domains.
    """
    print("🚀 PreventIA Automated Scraper Generation - Batch Test")
    print("=" * 60)

    # Test domains with different characteristics
    test_domains = [
        "www.medicalnewstoday.com",  # WordPress medical site
        "www.healthline.com",  # Large health site
        "www.news-medical.net",  # Known working domain
        "www.sciencedaily.com",  # Science news
    ]

    print(f"📋 Testing {len(test_domains)} domains")
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    scraper_generator = ScraperGenerator()
    results = []

    for i, domain in enumerate(test_domains, 1):
        print(f"\n{i}. 🔍 Testing {domain}")
        print("-" * 40)

        try:
            start_time = datetime.now()
            result = await scraper_generator.generate_scraper_for_domain(
                domain,
                {
                    "language": "en",
                    "country": "US",
                    "max_articles": 15,
                    "crawl_delay": 2,
                },
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            results.append(
                {
                    "domain": domain,
                    "result": result,
                    "duration": duration,
                    "success": True,
                }
            )

            # Status icons
            status_icons = {
                "ready_for_deployment": "✅",
                "needs_manual_review": "⚠️",
                "compliance_failed": "❌",
                "generation_failed": "❌",
                "testing_failed": "⚠️",
            }

            icon = status_icons.get(result.deployment_status, "❓")

            print(f"   {icon} Status: {result.deployment_status}")
            print(f"   📋 Template: {result.template_used}")
            print(f"   🛡️ Compliant: {result.compliance_result.is_compliant}")
            print(f"   📊 CMS Type: {result.site_structure.cms_type}")
            print(f"   ⚡ Duration: {duration:.1f}s")
            print(f"   📄 Code Size: {len(result.scraper_code)} chars")

            if result.test_results:
                success_rate = result.test_results.get("success_rate", 0)
                print(f"   🧪 Test Score: {success_rate:.1%}")

            # Show compliance details if failed
            if not result.compliance_result.is_compliant:
                violations = result.compliance_result.violations
                print(f"   ⚠️ Violations: {violations}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append(
                {
                    "domain": domain,
                    "result": None,
                    "duration": 0,
                    "success": False,
                    "error": str(e),
                }
            )

    # Final Statistics
    print(f"\n📊 BATCH TEST RESULTS")
    print("=" * 40)

    stats = scraper_generator.get_generation_stats()
    successful = len([r for r in results if r["success"]])
    deployment_ready = len(
        [
            r
            for r in results
            if r["success"] and r["result"].deployment_status == "ready_for_deployment"
        ]
    )

    print(f"📈 Overall Statistics:")
    print(f"   - Total Domains: {len(test_domains)}")
    print(
        f"   - Successful: {successful}/{len(test_domains)} ({successful/len(test_domains):.1%})"
    )
    print(
        f"   - Deployment Ready: {deployment_ready}/{len(test_domains)} ({deployment_ready/len(test_domains):.1%})"
    )
    print(f"   - Compliance Rate: {stats['compliance_rate']:.1%}")
    print(f"   - Average Success: {stats['success_rate']:.1%}")

    print(f"\n📋 Template Usage:")
    for template, count in stats["templates_used"].items():
        print(f"   - {template}: {count}")

    print(f"\n⏱️ Performance:")
    total_duration = sum(r["duration"] for r in results if r["success"])
    avg_duration = total_duration / successful if successful > 0 else 0
    print(f"   - Total Time: {total_duration:.1f}s")
    print(f"   - Average per Domain: {avg_duration:.1f}s")

    # Detailed Results Table
    print(f"\n📝 DETAILED RESULTS")
    print("-" * 80)
    print(
        f"{'Domain':<25} {'Status':<20} {'Template':<15} {'Compliant':<10} {'Duration'}"
    )
    print("-" * 80)

    for r in results:
        if r["success"]:
            result = r["result"]
            domain = r["domain"][:24]
            status = result.deployment_status[:19]
            template = result.template_used[:14]
            compliant = "✅" if result.compliance_result.is_compliant else "❌"
            duration = f"{r['duration']:.1f}s"

            print(
                f"{domain:<25} {status:<20} {template:<15} {compliant:<10} {duration}"
            )
        else:
            domain = r["domain"][:24]
            print(f"{domain:<25} {'ERROR':<20} {'-':<15} {'-':<10} {'-'}")

    print("-" * 80)
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return results


async def test_code_generation_only():
    """
    Quick test focusing only on code generation without full analysis.
    """
    print("\n🚀 Quick Code Generation Test")
    print("=" * 40)

    # Simple test with minimal structure
    from services.scraper.automation import ScraperTemplateEngine
    from services.scraper.automation.models import SiteStructure

    template_engine = ScraperTemplateEngine()

    # Test different CMS types
    cms_types = ["wordpress", "drupal", "custom_medical", "generic"]

    for cms_type in cms_types:
        print(f"\n📋 Testing {cms_type} template")

        test_structure = SiteStructure(
            domain=f"example-{cms_type}.com",
            cms_type=cms_type,
            navigation={},
            article_patterns={
                "article_list_url": f"https://example-{cms_type}.com/news"
            },
            content_structure={},
            complexity_score=0.5,
            detected_selectors={
                "article_links": [".post-title a"],
                "title_selectors": ["h1.title"],
                "content_selectors": [".content"],
                "date_selectors": [".date"],
            },
        )

        try:
            code = await template_engine.generate_scraper(test_structure)
            lines = len(code.split("\n"))
            print(f"   ✅ Generated: {lines} lines, {len(code)} characters")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")


if __name__ == "__main__":
    print("🧪 PreventIA Automated Scraper Generation - Batch Testing")
    print("🔬 Testing multiple domains and templates")
    print()

    # Run batch test
    results = asyncio.run(test_multiple_domains())

    # Run quick template test
    asyncio.run(test_code_generation_only())

    print("\n✅ All tests completed!")

    # Summary
    successful = len([r for r in results if r["success"]])
    ready = len(
        [
            r
            for r in results
            if r["success"] and r["result"].deployment_status == "ready_for_deployment"
        ]
    )

    if ready > 0:
        print(f"🎉 {ready} scrapers are ready for deployment!")
    if successful > ready:
        print(f"⚠️ {successful - ready} scrapers need manual review")

    failed = len(results) - successful
    if failed > 0:
        print(f"❌ {failed} scrapers failed generation")
