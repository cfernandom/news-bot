#!/usr/bin/env python3
"""
Integration Test Runner for PreventIA News Analytics
Comprehensive test execution and reporting for end-to-end validation
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest


class IntegrationTestRunner:
    """Comprehensive integration test runner"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_root = Path(__file__).parent
        self.results = {}
        self.start_time = None
        self.end_time = None

    def setup_environment(self):
        """Setup test environment and dependencies"""
        print("🔧 Setting up test environment...")

        # Ensure we're in the correct directory
        os.chdir(self.project_root)

        # Set test database URL
        test_db_url = os.getenv(
            "TEST_DATABASE_URL",
            "postgresql://preventia:preventia123@localhost:5433/preventia_test",
        )
        os.environ["DATABASE_URL"] = test_db_url
        os.environ["TEST_DATABASE_URL"] = test_db_url

        # Set JWT secret for testing
        os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-integration-testing"

        # Add project root to Python path
        if str(self.project_root) not in sys.path:
            sys.path.insert(0, str(self.project_root))

        print(f"✅ Environment configured")
        print(f"   Project root: {self.project_root}")
        print(f"   Test database: {test_db_url}")

    def check_dependencies(self) -> bool:
        """Check that all required dependencies are available"""
        print("🔍 Checking dependencies...")

        required_modules = [
            "pytest",
            "pytest_asyncio",
            "fastapi",
            "sqlalchemy",
            "asyncpg",
            "services.api.main",
            "services.data.database.connection",
            "services.nlp.src.sentiment",
        ]

        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError as e:
                missing_modules.append((module, str(e)))

        if missing_modules:
            print("❌ Missing dependencies:")
            for module, error in missing_modules:
                print(f"   - {module}: {error}")
            return False

        print("✅ All dependencies available")
        return True

    def check_database_connection(self) -> bool:
        """Check database connectivity"""
        print("🗄️  Checking database connection...")

        try:
            # Test database connection

            from services.data.database.connection import db_manager

            async def test_db():
                try:
                    await db_manager.initialize()
                    health = await db_manager.health_check()
                    await db_manager.close()
                    return health
                except Exception as e:
                    print(f"   Database error: {e}")
                    return False

            is_healthy = asyncio.run(test_db())

            if is_healthy:
                print("✅ Database connection successful")
                return True
            else:
                print("❌ Database connection failed")
                return False

        except Exception as e:
            print(f"❌ Database check error: {e}")
            return False

    def run_test_suite(self, test_type: str, verbose: bool = False) -> Dict[str, Any]:
        """Run specific test suite"""
        print(f"🧪 Running {test_type} tests...")

        # Define test configurations
        test_configs = {
            "system": {
                "file": "integration/test_system_integration.py",
                "markers": "integration and e2e",
                "timeout": 300,
            },
            "cli": {
                "file": "integration/test_cli_integration.py",
                "markers": "integration and e2e",
                "timeout": 180,
            },
            "auth": {
                "file": "integration/test_auth_integration.py",
                "markers": "integration",
                "timeout": 120,
            },
            "pipeline": {
                "file": "integration/test_data_pipeline_integration.py",
                "markers": "integration and e2e",
                "timeout": 240,
            },
            "validation": {
                "file": "integration/test_end_to_end_validation.py",
                "markers": "e2e and integration",
                "timeout": 600,
            },
            "all": {"file": "integration/", "markers": "integration", "timeout": 900},
        }

        if test_type not in test_configs:
            raise ValueError(f"Unknown test type: {test_type}")

        config = test_configs[test_type]
        test_file = self.test_root / config["file"]

        # Build pytest command
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(test_file),
            "-v" if verbose else "-q",
            "--tb=short",
            "--disable-warnings",
            "--durations=10",
            f"--timeout={config['timeout']}",
            f"-m",
            config["markers"],
            "--junit-xml=test-results.xml",
            "--json-report",
            "--json-report-file=test-report.json",
        ]

        # Run tests
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                cwd=self.test_root,
                capture_output=True,
                text=True,
                timeout=config["timeout"] + 60,  # Extra buffer
            )

            duration = time.time() - start_time

            # Parse results
            test_result = {
                "test_type": test_type,
                "returncode": result.returncode,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }

            # Try to parse JSON report if available
            json_report_path = self.test_root / "test-report.json"
            if json_report_path.exists():
                try:
                    with open(json_report_path, "r") as f:
                        json_report = json.load(f)
                        test_result["detailed_results"] = json_report
                except Exception as e:
                    print(f"   Warning: Could not parse JSON report: {e}")

            # Print results
            if test_result["success"]:
                print(f"✅ {test_type} tests passed ({duration:.1f}s)")
            else:
                print(f"❌ {test_type} tests failed ({duration:.1f}s)")
                if verbose:
                    print("STDOUT:", result.stdout[-1000:])  # Last 1000 chars
                    print("STDERR:", result.stderr[-1000:])

            return test_result

        except subprocess.TimeoutExpired:
            print(f"⏰ {test_type} tests timed out after {config['timeout']}s")
            return {
                "test_type": test_type,
                "returncode": -1,
                "duration": config["timeout"],
                "stdout": "",
                "stderr": "Test timed out",
                "success": False,
            }

        except Exception as e:
            print(f"💥 {test_type} tests crashed: {e}")
            return {
                "test_type": test_type,
                "returncode": -1,
                "duration": time.time() - start_time,
                "stdout": "",
                "stderr": str(e),
                "success": False,
            }

    def run_performance_benchmarks(self) -> Dict[str, Any]:
        """Run performance benchmarks"""
        print("🏃 Running performance benchmarks...")

        try:
            from fastapi.testclient import TestClient

            from services.api.main import app

            client = TestClient(app)
            benchmarks = {}

            # API response time benchmarks
            endpoints = [
                ("/health", "Health Check"),
                ("/api/v1/articles/", "Articles List"),
                ("/api/v1/analytics/sentiment", "Sentiment Analytics"),
                ("/docs", "API Documentation"),
            ]

            for endpoint, name in endpoints:
                times = []
                for _ in range(10):  # 10 requests per endpoint
                    start = time.time()
                    try:
                        response = client.get(endpoint)
                        duration = time.time() - start
                        if response.status_code == 200:
                            times.append(duration)
                    except Exception:
                        pass

                if times:
                    benchmarks[name] = {
                        "avg_time": sum(times) / len(times),
                        "min_time": min(times),
                        "max_time": max(times),
                        "requests": len(times),
                    }

            print("✅ Performance benchmarks completed")
            return {"benchmarks": benchmarks, "success": True}

        except Exception as e:
            print(f"❌ Performance benchmarks failed: {e}")
            return {"error": str(e), "success": False}

    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate comprehensive test report"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "duration": (
                self.end_time - self.start_time
                if self.start_time and self.end_time
                else 0
            ),
            "results": self.results,
            "summary": self._generate_summary(),
        }

        # Generate markdown report
        report_md = self._generate_markdown_report(report_data)

        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(report_md)
            print(f"📄 Report saved to: {output_path}")

        return report_md

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r.get("success", False))
        failed_tests = total_tests - passed_tests

        total_duration = sum(r.get("duration", 0) for r in self.results.values())

        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_duration,
        }

    def _generate_markdown_report(self, report_data: Dict[str, Any]) -> str:
        """Generate markdown test report"""
        summary = report_data["summary"]

        report = f"""# PreventIA Integration Test Report

## Summary
- **Timestamp**: {report_data["timestamp"]}
- **Total Duration**: {report_data["duration"]:.1f}s
- **Test Suites**: {summary["total_tests"]}
- **Passed**: {summary["passed"]} ✅
- **Failed**: {summary["failed"]} ❌
- **Pass Rate**: {summary["pass_rate"]:.1f}%

## Test Results

"""

        for test_type, result in report_data["results"].items():
            status = "✅ PASSED" if result.get("success") else "❌ FAILED"
            duration = result.get("duration", 0)

            report += f"""### {test_type.title()} Tests
- **Status**: {status}
- **Duration**: {duration:.1f}s
- **Return Code**: {result.get("returncode", "N/A")}

"""

            if not result.get("success") and result.get("stderr"):
                report += f"""**Error Output**:
```
{result["stderr"][-500:]}
```

"""

        # Add performance benchmarks if available
        if "performance" in report_data["results"]:
            perf_data = report_data["results"]["performance"]
            if "benchmarks" in perf_data:
                report += "## Performance Benchmarks\n\n"
                for name, metrics in perf_data["benchmarks"].items():
                    report += f"""### {name}
- **Average**: {metrics["avg_time"]:.3f}s
- **Min**: {metrics["min_time"]:.3f}s
- **Max**: {metrics["max_time"]:.3f}s
- **Requests**: {metrics["requests"]}

"""

        report += f"""## Recommendations

"""

        if summary["failed"] > 0:
            report += "- ❌ Address failing tests before deployment\n"
        if summary["pass_rate"] < 90:
            report += "- ⚠️ Improve test pass rate to at least 90%\n"
        if summary["total_duration"] > 600:
            report += "- 🐌 Consider optimizing slow tests\n"
        if summary["pass_rate"] >= 95:
            report += "- ✅ Excellent test coverage and pass rate\n"

        return report

    def run_full_suite(self, test_types: List[str], verbose: bool = False) -> bool:
        """Run full integration test suite"""
        self.start_time = time.time()

        print("🚀 Starting PreventIA Integration Test Suite")
        print("=" * 60)

        # Setup and checks
        self.setup_environment()

        if not self.check_dependencies():
            print("💥 Dependency check failed")
            return False

        if not self.check_database_connection():
            print("💥 Database connection failed")
            return False

        print("✅ Pre-flight checks passed")
        print("-" * 60)

        # Run test suites
        all_passed = True
        for test_type in test_types:
            result = self.run_test_suite(test_type, verbose)
            self.results[test_type] = result
            if not result["success"]:
                all_passed = False

        # Run performance benchmarks
        if "performance" not in test_types:
            perf_result = self.run_performance_benchmarks()
            self.results["performance"] = perf_result

        self.end_time = time.time()

        print("-" * 60)
        print("📊 Test Suite Summary:")
        summary = self._generate_summary()
        print(f"   Total: {summary['total_tests']} suites")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Pass Rate: {summary['pass_rate']:.1f}%")
        print(f"   Duration: {self.end_time - self.start_time:.1f}s")

        return all_passed


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="PreventIA Integration Test Runner")
    parser.add_argument(
        "tests",
        nargs="*",
        default=["all"],
        choices=["system", "cli", "auth", "pipeline", "validation", "all"],
        help="Test suites to run",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--report", "-r", type=str, help="Generate report file (e.g., test-report.md)"
    )
    parser.add_argument(
        "--no-performance", action="store_true", help="Skip performance benchmarks"
    )

    args = parser.parse_args()

    # Resolve test types
    if "all" in args.tests:
        test_types = ["system", "cli", "auth", "pipeline", "validation"]
    else:
        test_types = args.tests

    # Run tests
    runner = IntegrationTestRunner()
    success = runner.run_full_suite(test_types, args.verbose)

    # Generate report
    if args.report:
        runner.generate_report(args.report)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
