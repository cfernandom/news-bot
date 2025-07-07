"""
Test script for automation API endpoints.
Tests the FastAPI automation endpoints.
"""

import asyncio
import json
import sys
from datetime import datetime

import httpx


async def test_automation_api():
    """
    Test the automation API endpoints.
    """
    print("🧪 Testing PreventIA Automation API")
    print("=" * 50)

    base_url = "http://localhost:8000"

    async with httpx.AsyncClient(timeout=60.0) as client:

        # 1. Test health check
        print("\n🔍 1. Testing automation health check")
        try:
            response = await client.get(f"{base_url}/api/automation/health")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                health = response.json()
                print(f"   System: {health.get('automation_system')}")
                print(f"   Version: {health.get('version')}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Connection failed: {str(e)}")
            print("   Make sure FastAPI server is running: python -m services.api.main")
            return False

        # 2. Test available templates
        print("\n📋 2. Testing available templates")
        try:
            response = await client.get(f"{base_url}/api/automation/templates")
            if response.status_code == 200:
                templates = response.json()
                print(f"   Templates: {templates['available_templates']}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

        # 3. Test compliance validation
        print("\n🛡️ 3. Testing compliance validation")
        try:
            test_domain = "www.medicalnewstoday.com"
            response = await client.post(
                f"{base_url}/api/automation/validate-compliance",
                json={"domain": test_domain},
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                compliance = response.json()
                print(f"   Domain: {compliance['domain']}")
                print(f"   Compliant: {compliance['is_compliant']}")
                print(f"   Robots.txt: {compliance['robots_txt_compliant']}")
                print(f"   Legal Contact: {compliance['legal_contact_verified']}")
                if compliance["crawl_delay"]:
                    print(f"   Crawl Delay: {compliance['crawl_delay']}s")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

        # 4. Test domain analysis
        print("\n🔍 4. Testing domain analysis")
        try:
            test_domain = "www.medicalnewstoday.com"
            response = await client.post(
                f"{base_url}/api/automation/analyze-domain",
                json={"domain": test_domain},
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                analysis = response.json()
                print(f"   Domain: {analysis['domain']}")
                print(f"   CMS Type: {analysis['cms_type']}")
                print(f"   Complexity: {analysis['complexity_score']}")
                print(f"   JavaScript Heavy: {analysis['javascript_heavy']}")
                print(f"   Article Patterns: {analysis['article_patterns_count']}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

        # 5. Test scraper generation
        print("\n🤖 5. Testing scraper generation")
        try:
            test_domain = "www.medicalnewstoday.com"
            response = await client.post(
                f"{base_url}/api/automation/generate-scraper",
                json={
                    "domain": test_domain,
                    "language": "en",
                    "country": "US",
                    "max_articles": 20,
                    "crawl_delay": 3,
                },
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                generation = response.json()
                print(f"   Domain: {generation['domain']}")
                print(f"   Status: {generation['status']}")
                print(f"   Template: {generation['template_used']}")
                print(f"   Deployment Ready: {generation['deployment_ready']}")
                print(
                    f"   Code Preview Lines: {len(generation['code_preview'].split())}"
                )

                # Show test results if available
                if generation.get("test_results"):
                    tests = generation["test_results"]
                    success_rate = tests.get("success_rate", 0)
                    print(f"   Test Success Rate: {success_rate:.1%}")

            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

        # 6. Test automation statistics
        print("\n📊 6. Testing automation statistics")
        try:
            response = await client.get(f"{base_url}/api/automation/stats")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                stats = response.json()
                print(f"   Total Generated: {stats['total_generated']}")
                print(f"   Success Rate: {stats['success_rate']:.1%}")
                print(f"   Deployment Ready: {stats['deployment_ready']}")
                print(f"   Templates Used: {stats['templates_used']}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

        # 7. Test batch generation (small batch)
        print("\n🔄 7. Testing batch generation")
        try:
            test_domains = ["www.medicalnewstoday.com", "www.healthline.com"]
            response = await client.post(
                f"{base_url}/api/automation/batch-generate", json=test_domains
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                batch_results = response.json()
                print(f"   Batch Size: {len(batch_results)}")
                for result in batch_results:
                    domain = result["domain"]
                    status = result["status"]
                    ready = result["deployment_ready"]
                    print(f"   - {domain}: {status} {'✅' if ready else '❌'}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

        print(f"\n✅ API testing completed!")
        return True


async def test_api_performance():
    """
    Test API performance with timing.
    """
    print("\n⚡ Testing API Performance")
    print("=" * 30)

    base_url = "http://localhost:8000"
    test_domain = "www.medicalnewstoday.com"

    endpoints_to_test = [
        ("Health Check", "GET", "/api/automation/health", None),
        ("Templates", "GET", "/api/automation/templates", None),
        (
            "Compliance",
            "POST",
            "/api/automation/validate-compliance",
            {"domain": test_domain},
        ),
        ("Analysis", "POST", "/api/automation/analyze-domain", {"domain": test_domain}),
        (
            "Generation",
            "POST",
            "/api/automation/generate-scraper",
            {"domain": test_domain, "language": "en", "max_articles": 15},
        ),
    ]

    async with httpx.AsyncClient(timeout=120.0) as client:
        for name, method, endpoint, payload in endpoints_to_test:
            print(f"\n🔍 Testing {name}")

            start_time = datetime.now()
            try:
                if method == "GET":
                    response = await client.get(f"{base_url}{endpoint}")
                else:
                    response = await client.post(f"{base_url}{endpoint}", json=payload)

                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                print(f"   Status: {response.status_code}")
                print(f"   Duration: {duration:.2f}s")

                if response.status_code == 200:
                    response_size = len(response.content)
                    print(f"   Response Size: {response_size} bytes")
                else:
                    print(f"   Error: {response.text[:100]}...")

            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                print(f"   ❌ Error after {duration:.2f}s: {str(e)}")


if __name__ == "__main__":
    print("🧪 PreventIA Automation API Test Suite")
    print("🔬 Testing FastAPI automation endpoints")
    print("📡 Make sure API server is running on http://localhost:8000")
    print()

    # Run basic API tests
    success = asyncio.run(test_automation_api())

    if success:
        # Run performance tests
        run_perf = input("\n🤔 Run performance tests? (y/N): ").lower().strip()
        if run_perf in ["y", "yes"]:
            asyncio.run(test_api_performance())

    print("\n🎉 Testing completed!")
