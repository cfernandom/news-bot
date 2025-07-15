#!/usr/bin/env python3
"""
Source discovery script for PreventIA News Analytics.
Discovers and evaluates new medical news sources for potential scraping.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path

# Setup project environment (replaces manual sys.path manipulation)
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import setup_script_environment

setup_script_environment()
from pathlib import Path

from services.scraper.automation.source_discoverer import SourceDiscoverer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def discover_sources(
    search_terms: list, max_sources: int = 10, output_dir: str = None
):
    """
    Discover and evaluate sources based on search terms.

    Args:
        search_terms: List of search terms
        max_sources: Maximum number of sources to evaluate
        output_dir: Directory to save results
    """
    logger.info(f"🔍 Starting source discovery with terms: {search_terms}")

    discoverer = SourceDiscoverer()

    try:
        # Discover sources
        results = await discoverer.discover_sources_from_search(
            search_terms, max_sources
        )

        # Print summary
        print(f"\n📊 Source Discovery Summary:")
        print(f"   📈 Total Sources Evaluated: {len(results)}")

        stats = discoverer.get_discovery_stats()
        print(f"   ✅ Highly Recommended: {stats['highly_recommended']}")
        print(f"   👍 Recommended: {stats['recommended']}")
        print(f"   ❌ Not Recommended: {stats['not_recommended']}")
        print(f"   📊 Average Score: {stats['average_score']:.2f}")

        # Detailed results
        print(f"\n📋 Detailed Results:")
        for result in results:
            status_icon = (
                "✅"
                if "highly" in result.recommendation
                else "👍" if result.recommendation == "recommended" else "❌"
            )
            compliance_icon = "🛡️" if result.compliance_result.is_compliant else "⚠️"
            print(f"   {status_icon} {result.domain}")
            print(
                f"      Score: {result.overall_score:.2f} | {compliance_icon} Compliance: {'Pass' if result.compliance_result.is_compliant else 'Fail'}"
            )
            print(
                f"      Medical Relevance: {result.medical_relevance:.2f} | Recommendation: {result.recommendation}"
            )

        # Save results if output directory specified
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            # Save detailed results
            results_data = []
            for result in results:
                results_data.append(
                    {
                        "domain": result.domain,
                        "overall_score": result.overall_score,
                        "medical_relevance": result.medical_relevance,
                        "recommendation": result.recommendation,
                        "compliance": {
                            "is_compliant": result.compliance_result.is_compliant,
                            "violations": result.compliance_result.violations,
                        },
                        "content_quality": {
                            "freshness": result.content_quality.content_freshness,
                            "volume": result.content_quality.content_volume,
                            "structure": result.content_quality.content_structure,
                            "frequency": result.content_quality.update_frequency,
                        },
                        "technical_quality": {
                            "load_speed": result.technical_quality.page_load_speed,
                            "mobile": result.technical_quality.mobile_compatibility,
                            "accessibility": result.technical_quality.accessibility,
                            "reliability": result.technical_quality.technical_reliability,
                        },
                        "evaluation_timestamp": result.evaluation_timestamp.isoformat(),
                    }
                )

            results_file = output_path / "discovery_results.json"
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "search_terms": search_terms,
                        "discovery_stats": stats,
                        "sources": results_data,
                    },
                    f,
                    indent=2,
                )

            print(f"   💾 Results saved: {results_file}")

            # Save top recommendations
            top_sources = discoverer.get_top_sources(5)
            if top_sources:
                top_file = output_path / "top_recommendations.json"
                with open(top_file, "w", encoding="utf-8") as f:
                    json.dump(
                        [
                            {
                                "domain": s.domain,
                                "score": s.overall_score,
                                "recommendation": s.recommendation,
                            }
                            for s in top_sources
                        ],
                        f,
                        indent=2,
                    )

                print(f"   🏆 Top recommendations saved: {top_file}")

        return results

    except Exception as e:
        logger.error(f"❌ Error during source discovery: {str(e)}")
        print(f"\n❌ Discovery failed: {str(e)}")
        return []


async def evaluate_single_source(domain: str, output_dir: str = None):
    """
    Evaluate a single source.

    Args:
        domain: Domain to evaluate
        output_dir: Directory to save results
    """
    logger.info(f"🔍 Evaluating single source: {domain}")

    discoverer = SourceDiscoverer()

    try:
        result = await discoverer.evaluate_source(domain)

        # Print detailed results
        print(f"\n📊 Evaluation Results for {domain}:")
        print(f"   📈 Overall Score: {result.overall_score:.2f}")
        print(
            f"   🛡️ Compliance: {'✅ Pass' if result.compliance_result.is_compliant else '❌ Fail'}"
        )
        print(f"   🏥 Medical Relevance: {result.medical_relevance:.2f}")
        print(f"   💡 Recommendation: {result.recommendation}")

        if not result.compliance_result.is_compliant:
            print(f"   ⚠️ Compliance Violations:")
            for violation in result.compliance_result.violations[:3]:
                print(f"      - {violation}")

        print(f"\n📋 Quality Breakdown:")
        print(f"   📝 Content Quality:")
        print(f"      Freshness: {result.content_quality.content_freshness:.2f}")
        print(f"      Volume: {result.content_quality.content_volume:.2f}")
        print(f"      Structure: {result.content_quality.content_structure:.2f}")
        print(f"      Update Frequency: {result.content_quality.update_frequency:.2f}")

        print(f"   🔧 Technical Quality:")
        print(f"      Load Speed: {result.technical_quality.page_load_speed:.2f}")
        print(
            f"      Mobile Compatibility: {result.technical_quality.mobile_compatibility:.2f}"
        )
        print(f"      Accessibility: {result.technical_quality.accessibility:.2f}")
        print(
            f"      Reliability: {result.technical_quality.technical_reliability:.2f}"
        )

        # Save results if output directory specified
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            domain_safe = domain.replace(".", "_").replace("-", "_")
            result_file = output_path / f"{domain_safe}_evaluation.json"

            with open(result_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "domain": result.domain,
                        "overall_score": result.overall_score,
                        "medical_relevance": result.medical_relevance,
                        "recommendation": result.recommendation,
                        "compliance": {
                            "is_compliant": result.compliance_result.is_compliant,
                            "robots_txt_compliant": result.compliance_result.robots_txt_compliant,
                            "legal_contact_verified": result.compliance_result.legal_contact_verified,
                            "terms_acceptable": result.compliance_result.terms_acceptable,
                            "violations": result.compliance_result.violations,
                        },
                        "content_quality": result.content_quality.dict(),
                        "technical_quality": result.technical_quality.dict(),
                        "evaluation_timestamp": result.evaluation_timestamp.isoformat(),
                    },
                    f,
                    indent=2,
                )

            print(f"   💾 Evaluation saved: {result_file}")

        return result

    except Exception as e:
        logger.error(f"❌ Error evaluating {domain}: {str(e)}")
        print(f"\n❌ Evaluation failed for {domain}: {str(e)}")
        return None


def main():
    """Main entry point for the source discovery script."""
    parser = argparse.ArgumentParser(
        description="Discover and evaluate medical news sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Discover sources for breast cancer news
  python scripts/discover_sources.py --search "breast cancer" "medical news"

  # Evaluate a single source
  python scripts/discover_sources.py --domain healthline.com

  # Discovery with custom output directory
  python scripts/discover_sources.py --search "oncology news" --output-dir source_evaluations/

  # Discover multiple sources with higher limit
  python scripts/discover_sources.py --search "cancer research" --max-sources 20
        """,
    )

    # Main mode selection
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--search", nargs="+", help="Search terms for source discovery")
    group.add_argument("--domain", help="Single domain to evaluate")

    # Options
    parser.add_argument(
        "--max-sources",
        type=int,
        default=10,
        help="Maximum number of sources to discover and evaluate (default: 10)",
    )

    parser.add_argument(
        "--output-dir",
        default="source_evaluations",
        help="Directory to save evaluation results (default: source_evaluations/)",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print(f"🎯 Source Discovery & Evaluation Tool")

    if args.search:
        print(f"🔍 Mode: Discovery with search terms: {args.search}")
        print(f"📊 Max sources: {args.max_sources}")
    else:
        print(f"🔍 Mode: Single source evaluation: {args.domain}")

    print(f"📂 Output directory: {args.output_dir}")

    # Run discovery or evaluation
    try:
        if args.search:
            asyncio.run(
                discover_sources(args.search, args.max_sources, args.output_dir)
            )
        else:
            asyncio.run(evaluate_single_source(args.domain, args.output_dir))

        print(f"\n✅ Operation completed successfully!")
        return 0

    except KeyboardInterrupt:
        print(f"\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Operation failed: {str(e)}")
        logger.exception("Detailed error:")
        return 1


if __name__ == "__main__":
    exit(main())
