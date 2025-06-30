#!/usr/bin/env python3
"""
Framework de Testing Estandarizado para Scrapers Migrados
Provee base común para tests de scrapers con validaciones estándar
"""

import asyncio
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from dotenv import load_dotenv

# Setup
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
load_dotenv()

from services.data.database.connection import close_database, db_manager, init_database


class ScraperTestFramework(ABC):
    """
    Base class para testing estandarizado de scrapers migrados
    """

    def __init__(
        self, scraper_name: str, scraper_function: Callable, expected_source_name: str
    ):
        self.scraper_name = scraper_name
        self.scraper_function = scraper_function
        self.expected_source_name = expected_source_name
        self.test_results: Dict[str, Any] = {}

    async def run_full_test_suite(self) -> Dict[str, Any]:
        """Ejecuta suite completo de tests estandarizados"""
        print(f"🧪 TESTING FRAMEWORK - {self.scraper_name}")
        print("=" * 60)

        try:
            await init_database()

            # Tests obligatorios
            await self._test_database_connection()
            await self._test_source_exists()
            await self._test_scraper_execution()
            await self._test_data_quality()
            await self._test_performance()

            # Test específico del scraper (implementado por subclase)
            await self.test_scraper_specific()

            # Resumen final
            self._generate_test_report()

        except Exception as e:
            print(f"❌ Critical test failure: {e}")
            self.test_results["critical_error"] = str(e)
        finally:
            await close_database()

        return self.test_results

    async def _test_database_connection(self):
        """Test 1: Conexión a base de datos"""
        print("📊 Test 1: Database Connection")
        try:
            version = await db_manager.execute_sql_scalar("SELECT version()")
            self.test_results["db_connection"] = {
                "status": "success",
                "version": version[:50] + "..." if len(version) > 50 else version,
            }
            print("   ✅ Database connection successful")
        except Exception as e:
            self.test_results["db_connection"] = {"status": "error", "error": str(e)}
            print(f"   ❌ Database connection failed: {e}")
            raise

    async def _test_source_exists(self):
        """Test 2: Verificar que la fuente existe en news_sources"""
        print("📊 Test 2: Source Verification")
        try:
            query = "SELECT id, name, base_url FROM news_sources WHERE name ILIKE $1 LIMIT 1"
            source = await db_manager.execute_sql_one(
                query, f"%{self.expected_source_name}%"
            )

            if source:
                self.source_id = source["id"]
                self.test_results["source_verification"] = {
                    "status": "success",
                    "source_id": source["id"],
                    "source_name": source["name"],
                    "base_url": source["base_url"],
                }
                print(f"   ✅ Source found: {source['name']} (ID: {source['id']})")
            else:
                self.test_results["source_verification"] = {
                    "status": "error",
                    "error": f"Source '{self.expected_source_name}' not found",
                }
                print(f"   ❌ Source '{self.expected_source_name}' not found")
                raise Exception(f"Source not found: {self.expected_source_name}")

        except Exception as e:
            if "source_verification" not in self.test_results:
                self.test_results["source_verification"] = {
                    "status": "error",
                    "error": str(e),
                }
            raise

    async def _test_scraper_execution(self):
        """Test 3: Ejecución del scraper"""
        print("📊 Test 3: Scraper Execution")
        try:
            start_time = datetime.now()

            # Contar artículos antes
            pre_count_query = (
                "SELECT COUNT(*) as count FROM articles WHERE source_id = $1"
            )
            pre_count = await db_manager.execute_sql_one(
                pre_count_query, self.source_id
            )

            # Ejecutar scraper
            article_ids = await self.scraper_function()

            # Contar artículos después
            post_count = await db_manager.execute_sql_one(
                pre_count_query, self.source_id
            )

            execution_time = (datetime.now() - start_time).total_seconds()
            articles_added = post_count["count"] - pre_count["count"]

            self.test_results["scraper_execution"] = {
                "status": "success",
                "execution_time_seconds": execution_time,
                "articles_before": pre_count["count"],
                "articles_after": post_count["count"],
                "articles_added": articles_added,
                "article_ids_returned": len(article_ids) if article_ids else 0,
                "article_ids_sample": article_ids[:5] if article_ids else [],
            }

            print(f"   ✅ Scraper executed successfully")
            print(f"   ⏱️  Execution time: {execution_time:.2f}s")
            print(f"   📊 Articles added: {articles_added}")
            print(f"   🆔 IDs returned: {len(article_ids) if article_ids else 0}")

        except Exception as e:
            self.test_results["scraper_execution"] = {
                "status": "error",
                "error": str(e),
            }
            print(f"   ❌ Scraper execution failed: {e}")
            raise

    async def _test_data_quality(self):
        """Test 4: Calidad de datos insertados"""
        print("📊 Test 4: Data Quality")
        try:
            # Query para verificar calidad de datos
            quality_query = """
                SELECT
                    COUNT(*) as total_articles,
                    COUNT(CASE WHEN title IS NOT NULL AND title != '' THEN 1 END) as with_title,
                    COUNT(CASE WHEN url IS NOT NULL AND url != '' THEN 1 END) as with_url,
                    COUNT(CASE WHEN published_at IS NOT NULL THEN 1 END) as with_date,
                    COUNT(CASE WHEN content_hash IS NOT NULL THEN 1 END) as with_hash,
                    COUNT(CASE WHEN word_count IS NOT NULL AND word_count > 0 THEN 1 END) as with_word_count,
                    COUNT(CASE WHEN language IS NOT NULL THEN 1 END) as with_language,
                    COUNT(CASE WHEN country IS NOT NULL THEN 1 END) as with_country,
                    COUNT(DISTINCT url) as unique_urls
                FROM articles
                WHERE source_id = $1
            """

            quality = await db_manager.execute_sql_one(quality_query, self.source_id)

            # Calcular porcentajes
            total = quality["total_articles"]
            quality_metrics = {}

            if total > 0:
                quality_metrics = {
                    "title_completeness": (quality["with_title"] / total) * 100,
                    "url_completeness": (quality["with_url"] / total) * 100,
                    "date_completeness": (quality["with_date"] / total) * 100,
                    "hash_completeness": (quality["with_hash"] / total) * 100,
                    "word_count_completeness": (quality["with_word_count"] / total)
                    * 100,
                    "language_completeness": (quality["with_language"] / total) * 100,
                    "country_completeness": (quality["with_country"] / total) * 100,
                    "url_uniqueness": (quality["unique_urls"] / total) * 100
                    if total > 0
                    else 100,
                }

            self.test_results["data_quality"] = {
                "status": "success",
                "total_articles": total,
                "metrics": quality_metrics,
                "raw_counts": dict(quality),
            }

            print(f"   ✅ Data quality analysis completed")
            print(f"   📊 Total articles: {total}")
            if total > 0:
                print(
                    f"   📝 Title completeness: {quality_metrics['title_completeness']:.1f}%"
                )
                print(f"   🔗 URL uniqueness: {quality_metrics['url_uniqueness']:.1f}%")
                print(
                    f"   📅 Date completeness: {quality_metrics['date_completeness']:.1f}%"
                )
                print(
                    f"   🔑 Metadata completeness: {quality_metrics['hash_completeness']:.1f}%"
                )

        except Exception as e:
            self.test_results["data_quality"] = {"status": "error", "error": str(e)}
            print(f"   ❌ Data quality test failed: {e}")

    async def _test_performance(self):
        """Test 5: Métricas de performance"""
        print("📊 Test 5: Performance Metrics")
        try:
            if (
                "scraper_execution" in self.test_results
                and self.test_results["scraper_execution"]["status"] == "success"
            ):
                exec_data = self.test_results["scraper_execution"]

                articles_added = exec_data["articles_added"]
                execution_time = exec_data["execution_time_seconds"]

                performance_metrics = {
                    "articles_per_second": articles_added / execution_time
                    if execution_time > 0
                    else 0,
                    "seconds_per_article": execution_time / articles_added
                    if articles_added > 0
                    else 0,
                    "execution_efficiency": "excellent"
                    if execution_time < 60
                    else "good"
                    if execution_time < 120
                    else "needs_optimization",
                }

                self.test_results["performance"] = {
                    "status": "success",
                    "metrics": performance_metrics,
                }

                print(f"   ✅ Performance analysis completed")
                print(
                    f"   ⚡ Articles per second: {performance_metrics['articles_per_second']:.2f}"
                )
                print(
                    f"   ⏱️  Seconds per article: {performance_metrics['seconds_per_article']:.2f}"
                )
                print(f"   🎯 Efficiency: {performance_metrics['execution_efficiency']}")
            else:
                self.test_results["performance"] = {
                    "status": "skipped",
                    "reason": "Scraper execution failed",
                }
                print("   ⚠️  Performance test skipped (scraper execution failed)")

        except Exception as e:
            self.test_results["performance"] = {"status": "error", "error": str(e)}
            print(f"   ❌ Performance test failed: {e}")

    @abstractmethod
    async def test_scraper_specific(self):
        """Test específico del scraper - debe ser implementado por subclase"""
        pass

    def _generate_test_report(self):
        """Genera reporte final de tests"""
        print("\n🎯 TEST REPORT SUMMARY")
        print("=" * 40)

        total_tests = 0
        passed_tests = 0

        for test_name, result in self.test_results.items():
            if isinstance(result, dict) and "status" in result:
                total_tests += 1
                if result["status"] == "success":
                    passed_tests += 1
                    print(f"   ✅ {test_name}: PASSED")
                elif result["status"] == "skipped":
                    print(f"   ⚠️  {test_name}: SKIPPED")
                else:
                    print(f"   ❌ {test_name}: FAILED")

        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        print(f"\n📊 Overall Results:")
        print(f"   Tests passed: {passed_tests}/{total_tests}")
        print(f"   Success rate: {success_rate:.1f}%")

        if success_rate >= 80:
            print(f"   🎉 Status: EXCELLENT")
        elif success_rate >= 60:
            print(f"   ✅ Status: GOOD")
        else:
            print(f"   ⚠️  Status: NEEDS IMPROVEMENT")

        self.test_results["overall"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "status": "excellent"
            if success_rate >= 80
            else "good"
            if success_rate >= 60
            else "needs_improvement",
        }


# Ejemplo de implementación específica
class BreastCancerOrgTest(ScraperTestFramework):
    """Test específico para Breast Cancer Org scraper"""

    def __init__(self):
        from services.scraper.src.extractors.www_breastcancer_org_postgres import (
            scrape_breastcancer_org_to_postgres,
        )

        super().__init__(
            scraper_name="Breast Cancer Org",
            scraper_function=scrape_breastcancer_org_to_postgres,
            expected_source_name="Breast Cancer Org",
        )

    async def test_scraper_specific(self):
        """Tests específicos para Breast Cancer Org"""
        print("📊 Test Específico: Breast Cancer Org")
        try:
            # Verificar estructura específica de URLs
            url_pattern_query = """
                SELECT COUNT(*) as count
                FROM articles
                WHERE source_id = $1
                AND url LIKE '%breastcancer.org/research-news/%'
            """

            url_check = await db_manager.execute_sql_one(
                url_pattern_query, self.source_id
            )

            self.test_results["specific_breast_cancer_org"] = {
                "status": "success",
                "url_pattern_matches": url_check["count"],
                "expected_url_pattern": "breastcancer.org/research-news/",
            }

            print(
                f"   ✅ URL pattern validation: {url_check['count']} articles match expected pattern"
            )

        except Exception as e:
            self.test_results["specific_breast_cancer_org"] = {
                "status": "error",
                "error": str(e),
            }
            print(f"   ❌ Specific test failed: {e}")


# Test runner
async def run_scraper_test(test_class):
    """Helper para ejecutar un test específico"""
    test_instance = test_class()
    return await test_instance.run_full_test_suite()


if __name__ == "__main__":
    # Ejemplo de uso
    async def main():
        results = await run_scraper_test(BreastCancerOrgTest)
        print(f"\n🔍 Detailed results available in results dict")

    asyncio.run(main())
