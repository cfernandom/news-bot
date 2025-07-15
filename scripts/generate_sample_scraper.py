"""
Generate and save a sample scraper to demonstrate the automation system.
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


async def generate_and_save_scraper():
    """
    Generate a scraper for Medical News Today and save it.
    """
    print("🤖 Generating Sample Scraper for Medical News Today")
    print("=" * 60)

    domain = "www.medicalnewstoday.com"
    scraper_generator = ScraperGenerator()

    print(f"🔍 Analyzing and generating scraper for {domain}...")

    result = await scraper_generator.generate_scraper_for_domain(
        domain,
        {"language": "en", "country": "US", "max_articles": 25, "crawl_delay": 3},
    )

    print(f"✅ Generation completed!")
    print(f"   - Status: {result.deployment_status}")
    print(f"   - Template: {result.template_used}")
    print(f"   - Compliant: {result.compliance_result.is_compliant}")
    print(f"   - Code size: {len(result.scraper_code)} characters")

    # Save the generated scraper
    filename = f"generated_scraper_{domain.replace('.', '_')}.py"
    project_root = Path(__file__).parent.parent
    filepath = os.path.join(project_root, "scripts", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(result.scraper_code)

    print(f"💾 Scraper saved to: {filepath}")

    # Show analysis details
    print(f"\n📊 Site Analysis Details:")
    print(f"   - CMS Type: {result.site_structure.cms_type}")
    print(f"   - Complexity: {result.site_structure.complexity_score}")
    print(f"   - JavaScript Heavy: {result.site_structure.javascript_heavy}")
    print(f"   - Requires Playwright: {result.site_structure.requires_playwright}")
    print(f"   - Article Patterns: {len(result.site_structure.article_patterns)}")
    print(f"   - Detected Selectors: {len(result.site_structure.detected_selectors)}")

    # Show compliance details
    print(f"\n🛡️ Compliance Details:")
    comp = result.compliance_result
    print(f"   - Robots.txt: {comp.robots_txt_compliant}")
    print(f"   - Legal Contact: {comp.legal_contact_verified}")
    print(f"   - Terms Acceptable: {comp.terms_acceptable}")
    print(f"   - Fair Use: {comp.fair_use_documented}")
    print(f"   - Data Minimization: {comp.data_minimization_applied}")
    print(f"   - Crawl Delay: {comp.crawl_delay}s")

    # Show test results
    if result.test_results:
        print(f"\n🧪 Test Results:")
        tests = result.test_results
        print(f"   - Success Rate: {tests.get('success_rate', 0):.1%}")
        print(f"   - Compliance: {'✅' if tests.get('compliance_passed') else '❌'}")
        print(
            f"   - Functionality: {'✅' if tests.get('functionality_passed') else '❌'}"
        )
        print(f"   - Performance: {'✅' if tests.get('performance_passed') else '❌'}")
        print(
            f"   - Data Quality: {'✅' if tests.get('data_quality_passed') else '❌'}"
        )
        print(
            f"   - Error Handling: {'✅' if tests.get('error_handling_passed') else '❌'}"
        )

    print(
        f"\n🎯 Ready for deployment: {'✅ YES' if result.deployment_status == 'ready_for_deployment' else '❌ NO'}"
    )
    print("=" * 60)

    return filepath


if __name__ == "__main__":
    filepath = asyncio.run(generate_and_save_scraper())
    print(f"\n📄 Generated scraper file: {os.path.basename(filepath)}")
    print("🚀 You can now use this scraper in production!")
