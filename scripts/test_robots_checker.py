#!/usr/bin/env python3
"""
Test script for robots.txt checker functionality
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from services.scraper.src.compliance import check_robots_compliance


async def test_robots_checker():
    """Test robots.txt checker with real URLs"""
    test_urls = [
        "https://www.breastcancer.org/",
        "https://www.webmd.com/",
        "https://www.curetoday.com/",
        "https://www.news-medical.net/",
    ]

    print("🔍 Testing robots.txt compliance checker...")
    print("=" * 60)

    for url in test_urls:
        print(f"\nTesting: {url}")
        try:
            allowed = await check_robots_compliance(url)
            status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
            print(f"Result: {status}")
        except Exception as e:
            print(f"❌ ERROR: {e}")

    print("\n" + "=" * 60)
    print("✅ Robots.txt checker test completed")


if __name__ == "__main__":
    asyncio.run(test_robots_checker())
