#!/usr/bin/env python3
"""
Automated scraper generation script for PreventIA News Analytics.
Generates scrapers for new domains with compliance-first approach.
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

# Setup project environment (replaces manual sys.path manipulation)
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import setup_script_environment

setup_script_environment()

from services.scraper.automation.scraper_generator import ScraperGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def generate_scraper_for_domain(
    domain: str, output_dir: str = None, config: dict = None
):
    """
    Generate a scraper for a specific domain.

    Args:
        domain: Target domain
        output_dir: Directory to save generated scraper
        config: Optional configuration for the scraper
    """
    logger.info(f"🚀 Starting scraper generation for: {domain}")

    if config is None:
        config = {}

    # Initialize scraper generator
    generator = ScraperGenerator()

    try:
        # Generate scraper
        result = await generator.generate_scraper_for_domain(domain, config)

        # Print results
        print(f"\n📊 Generation Results for {domain}:")
        print(f"   ✅ Status: {result.deployment_status}")
        print(f"   🏷️ Template Used: {result.template_used}")
        print(
            f"   🛡️ Compliance: {'✅ Passed' if result.compliance_result.is_compliant else '❌ Failed'}"
        )

        if not result.compliance_result.is_compliant:
            print(
                f"   ⚠️ Violations: {', '.join(result.compliance_result.violations[:3])}"
            )

        print(f"   📈 Complexity Score: {result.site_structure.complexity_score:.2f}")
        print(f"   🏗️ CMS Type: {result.site_structure.cms_type}")

        # Save scraper if generation was successful
        if result.scraper_code and output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            domain_safe = domain.replace(".", "_").replace("-", "_")
            scraper_filename = f"{domain_safe}_scraper.py"
            scraper_path = output_path / scraper_filename

            with open(scraper_path, "w", encoding="utf-8") as f:
                f.write(result.scraper_code)

            print(f"   💾 Scraper saved: {scraper_path}")

        # Save detailed results as JSON
        if output_dir:
            results_path = Path(output_dir) / f"{domain_safe}_results.json"
            with open(results_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "domain": result.domain,
                        "deployment_status": result.deployment_status,
                        "template_used": result.template_used,
                        "compliance_passed": result.compliance_result.is_compliant,
                        "compliance_violations": result.compliance_result.violations,
                        "site_structure": {
                            "cms_type": result.site_structure.cms_type,
                            "complexity_score": result.site_structure.complexity_score,
                            "requires_playwright": result.site_structure.requires_playwright,
                        },
                        "generation_timestamp": result.generation_timestamp.isoformat(),
                    },
                    indent=2,
                )

            print(f"   📋 Results saved: {results_path}")

        return result

    except Exception as e:
        logger.error(f"❌ Error generating scraper for {domain}: {str(e)}")
        print(f"\n❌ Generation failed for {domain}: {str(e)}")
        return None


async def generate_scrapers_batch(
    domains: list, output_dir: str = None, config: dict = None
):
    """
    Generate scrapers for multiple domains.

    Args:
        domains: List of domains to process
        output_dir: Directory to save generated scrapers
        config: Optional configuration for the scrapers
    """
    logger.info(f"🚀 Starting batch generation for {len(domains)} domains")

    generator = ScraperGenerator()

    try:
        results = await generator.generate_scrapers_for_multiple_domains(domains)

        # Print summary
        print(f"\n📊 Batch Generation Summary:")
        print(f"   📈 Total Domains: {len(domains)}")
        print(
            f"   ✅ Successful: {len([r for r in results if r.deployment_status == 'ready_for_deployment'])}"
        )
        print(
            f"   ⚠️ Needs Review: {len([r for r in results if r.deployment_status == 'needs_manual_review'])}"
        )
        print(
            f"   ❌ Failed: {len([r for r in results if 'failed' in r.deployment_status])}"
        )

        # Detailed results
        print(f"\n📋 Detailed Results:")
        for result in results:
            status_icon = (
                "✅"
                if result.deployment_status == "ready_for_deployment"
                else "⚠️" if "review" in result.deployment_status else "❌"
            )
            print(
                f"   {status_icon} {result.domain}: {result.deployment_status} ({result.template_used})"
            )

        # Save batch results
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            # Save individual scrapers
            for result in results:
                if result.scraper_code:
                    domain_safe = result.domain.replace(".", "_").replace("-", "_")
                    scraper_path = output_path / f"{domain_safe}_scraper.py"

                    with open(scraper_path, "w", encoding="utf-8") as f:
                        f.write(result.scraper_code)

            # Save batch summary
            summary_path = output_path / "batch_generation_summary.json"
            with open(summary_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "total_domains": len(domains),
                        "successful": len(
                            [
                                r
                                for r in results
                                if r.deployment_status == "ready_for_deployment"
                            ]
                        ),
                        "needs_review": len(
                            [
                                r
                                for r in results
                                if r.deployment_status == "needs_manual_review"
                            ]
                        ),
                        "failed": len(
                            [r for r in results if "failed" in r.deployment_status]
                        ),
                        "generation_stats": generator.get_generation_stats(),
                        "results": [
                            {
                                "domain": r.domain,
                                "deployment_status": r.deployment_status,
                                "template_used": r.template_used,
                                "compliance_passed": r.compliance_result.is_compliant,
                            }
                            for r in results
                        ],
                    },
                    indent=2,
                )

            print(f"   📋 Batch summary saved: {summary_path}")

        return results

    except Exception as e:
        logger.error(f"❌ Error in batch generation: {str(e)}")
        print(f"\n❌ Batch generation failed: {str(e)}")
        return []


def main():
    """Main entry point for the scraper generation script."""
    parser = argparse.ArgumentParser(
        description="Generate scrapers automatically for news sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate scraper for single domain
  python scripts/generate_scraper.py example.com

  # Generate with custom output directory
  python scripts/generate_scraper.py example.com --output-dir generated_scrapers/

  # Generate with custom configuration
  python scripts/generate_scraper.py example.com --config '{"language": "es", "country": "Spain"}'

  # Batch generation from file
  python scripts/generate_scraper.py --batch domains.txt

  # Test medical site generation
  python scripts/generate_scraper.py medical-news-site.com --config '{"max_articles": 10, "crawl_delay": 3}'
        """,
    )

    # Main arguments
    parser.add_argument(
        "domain", nargs="?", help="Domain to generate scraper for (e.g., example.com)"
    )

    # Options
    parser.add_argument(
        "--output-dir",
        default="generated_scrapers",
        help="Directory to save generated scrapers (default: generated_scrapers/)",
    )

    parser.add_argument("--config", help="JSON configuration for scraper generation")

    parser.add_argument(
        "--batch", help="File containing list of domains (one per line)"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze site structure without generating scraper",
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Parse config
    config = {}
    if args.config:
        try:
            config = json.loads(args.config)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON config: {e}")
            return 1

    # Determine domains to process
    domains = []

    if args.batch:
        # Batch mode
        try:
            with open(args.batch, "r") as f:
                domains = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]
        except FileNotFoundError:
            print(f"❌ Batch file not found: {args.batch}")
            return 1
    elif args.domain:
        # Single domain mode
        domains = [args.domain]
    else:
        print("❌ Either specify a domain or use --batch with a file")
        parser.print_help()
        return 1

    # Validate domains
    if not domains:
        print("❌ No domains to process")
        return 1

    print(f"🎯 Processing {len(domains)} domain(s)")
    print(f"📂 Output directory: {args.output_dir}")

    if args.dry_run:
        print("🔍 DRY RUN MODE: Analysis only, no scraper generation")

    # Run generation
    try:
        if len(domains) == 1:
            asyncio.run(
                generate_scraper_for_domain(domains[0], args.output_dir, config)
            )
        else:
            asyncio.run(generate_scrapers_batch(domains, args.output_dir, config))

        print(f"\n✅ Scraper generation completed successfully!")
        return 0

    except KeyboardInterrupt:
        print(f"\n⚠️ Generation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Generation failed: {str(e)}")
        logger.exception("Detailed error:")
        return 1


if __name__ == "__main__":
    exit(main())
