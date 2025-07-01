#!/usr/bin/env python3
"""
Testing Framework Verification Script
Verifies that all testing components are working correctly
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Execute a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent
        )
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ FAILED: {description}")
            print(f"Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ ERROR: {description} - {e}")
        return False


def main():
    """Run all verification tests"""
    print("🧪 PreventIA News Analytics - Testing Framework Verification")
    print("=" * 80)

    tests = [
        ("pytest --collect-only -q | wc -l", "Test Discovery (Count all tests)"),
        ("pytest -m unit --collect-only -q | wc -l", "Unit Tests Discovery"),
        (
            "pytest -m integration --collect-only -q | wc -l",
            "Integration Tests Discovery",
        ),
        ("pytest unit/test_api/test_models.py -v --tb=short", "API Models Unit Tests"),
        (
            "pytest unit/test_nlp/test_sentiment.py::TestSentimentAnalyzer::test_analyze_sentiment_positive_text -v",
            "NLP Sentiment Test",
        ),
        (
            "pytest unit/test_database/test_connection.py::TestDatabaseManager::test_init_with_database_url -v",
            "Database Connection Test",
        ),
        ("pytest --version", "Pytest Version Check"),
        (
            "python -c 'import pytest; import pytest_asyncio; import pytest_cov; print(\"All testing dependencies available\")'",
            "Dependencies Check",
        ),
    ]

    results = []
    for cmd, desc in tests:
        success = run_command(cmd, desc)
        results.append((desc, success))

    # Summary
    print(f"\n{'='*80}")
    print("📊 VERIFICATION SUMMARY")
    print(f"{'='*80}")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for desc, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:<10} {desc}")

    print(f"\n📈 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Testing framework is working correctly!")
        return 0
    else:
        print(f"\n⚠️  SOME TESTS FAILED - Please review the failed tests above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
