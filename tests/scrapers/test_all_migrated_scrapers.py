#!/usr/bin/env python3
"""
Test Suite Completo para Todos los Scrapers Migrados
Usa el framework estandarizado para validar todos los scrapers
"""

import asyncio
import sys
import os
from datetime import datetime
from test_scraper_framework import ScraperTestFramework, run_scraper_test

# Setup paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import database manager for specific tests
from services.data.database.connection import db_manager

# Import scrapers
from services.scraper.src.extractors.www_breastcancer_org_postgres import scrape_breastcancer_org_to_postgres
from services.scraper.src.extractors.www_webmd_com_postgres import scrape_webmd_to_postgres
from services.scraper.src.extractors.www_curetoday_com_postgres import scrape_curetoday_to_postgres
from services.scraper.src.extractors.www_news_medical_net_postgres import scrape_news_medical_to_postgres

class BreastCancerOrgTest(ScraperTestFramework):
    def __init__(self):
        super().__init__(
            scraper_name="Breast Cancer Org",
            scraper_function=scrape_breastcancer_org_to_postgres,
            expected_source_name="Breast Cancer Org"
        )
    
    async def test_scraper_specific(self):
        print("📊 Test Específico: Breast Cancer Org")
        try:
            # Verificar patrón de URLs específico
            url_pattern_query = """
                SELECT COUNT(*) as count 
                FROM articles 
                WHERE source_id = $1 
                AND url LIKE '%breastcancer.org/research-news/%'
            """
            url_check = await db_manager.execute_sql_one(url_pattern_query, self.source_id)
            
            self.test_results['specific_tests'] = {
                'status': 'success',
                'url_pattern_matches': url_check['count'],
                'expected_domain': 'breastcancer.org'
            }
            print(f"   ✅ URL pattern: {url_check['count']} articles match breastcancer.org pattern")
            
        except Exception as e:
            self.test_results['specific_tests'] = {'status': 'error', 'error': str(e)}
            print(f"   ❌ Specific test failed: {e}")

class WebMDTest(ScraperTestFramework):
    def __init__(self):
        super().__init__(
            scraper_name="WebMD",
            scraper_function=scrape_webmd_to_postgres,
            expected_source_name="WebMD"
        )
    
    async def test_scraper_specific(self):
        print("📊 Test Específico: WebMD")
        try:
            # Verificar parsing de fechas WebMD
            date_quality_query = """
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN published_at > '2020-01-01' THEN 1 END) as recent_dates
                FROM articles 
                WHERE source_id = $1
            """
            date_check = await db_manager.execute_sql_one(date_quality_query, self.source_id)
            
            self.test_results['specific_tests'] = {
                'status': 'success',
                'date_parsing_quality': (date_check['recent_dates'] / date_check['total']) * 100 if date_check['total'] > 0 else 0,
                'expected_domain': 'webmd.com'
            }
            print(f"   ✅ Date parsing: {date_check['recent_dates']}/{date_check['total']} articles have valid recent dates")
            
        except Exception as e:
            self.test_results['specific_tests'] = {'status': 'error', 'error': str(e)}
            print(f"   ❌ Specific test failed: {e}")

class CureTodayTest(ScraperTestFramework):
    def __init__(self):
        super().__init__(
            scraper_name="CureToday",
            scraper_function=scrape_curetoday_to_postgres,
            expected_source_name="CureToday"
        )
    
    async def test_scraper_specific(self):
        print("📊 Test Específico: CureToday")
        try:
            # Verificar estructura de contenido CureToday
            content_quality_query = """
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN summary IS NOT NULL AND LENGTH(summary) > 50 THEN 1 END) as with_quality_summary
                FROM articles 
                WHERE source_id = $1
            """
            content_check = await db_manager.execute_sql_one(content_quality_query, self.source_id)
            
            self.test_results['specific_tests'] = {
                'status': 'success',
                'summary_quality': (content_check['with_quality_summary'] / content_check['total']) * 100 if content_check['total'] > 0 else 0,
                'expected_domain': 'curetoday.com'
            }
            print(f"   ✅ Summary quality: {content_check['with_quality_summary']}/{content_check['total']} articles have quality summaries")
            
        except Exception as e:
            self.test_results['specific_tests'] = {'status': 'error', 'error': str(e)}
            print(f"   ❌ Specific test failed: {e}")

class NewsMedicalTest(ScraperTestFramework):
    def __init__(self):
        super().__init__(
            scraper_name="News Medical",
            scraper_function=scrape_news_medical_to_postgres,
            expected_source_name="News Medical"
        )
    
    async def test_scraper_specific(self):
        print("📊 Test Específico: News Medical")
        try:
            # Verificar consistencia de datos News Medical
            consistency_query = """
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN country = 'International' THEN 1 END) as correct_country,
                    COUNT(CASE WHEN language = 'en' THEN 1 END) as correct_language
                FROM articles 
                WHERE source_id = $1
            """
            consistency_check = await db_manager.execute_sql_one(consistency_query, self.source_id)
            
            self.test_results['specific_tests'] = {
                'status': 'success',
                'metadata_consistency': {
                    'country_accuracy': (consistency_check['correct_country'] / consistency_check['total']) * 100 if consistency_check['total'] > 0 else 0,
                    'language_accuracy': (consistency_check['correct_language'] / consistency_check['total']) * 100 if consistency_check['total'] > 0 else 0
                },
                'expected_domain': 'news-medical.net'
            }
            print(f"   ✅ Metadata consistency: Country {consistency_check['correct_country']}/{consistency_check['total']}, Language {consistency_check['correct_language']}/{consistency_check['total']}")
            
        except Exception as e:
            self.test_results['specific_tests'] = {'status': 'error', 'error': str(e)}
            print(f"   ❌ Specific test failed: {e}")

async def run_comprehensive_test_suite():
    """Ejecuta suite completo de tests para todos los scrapers"""
    print("🧪 COMPREHENSIVE SCRAPER TEST SUITE")
    print("=" * 80)
    print(f"⏰ Started at: {datetime.now()}")
    print()
    
    test_classes = [
        BreastCancerOrgTest,
        WebMDTest, 
        CureTodayTest,
        NewsMedicalTest
    ]
    
    all_results = {}
    passed_scrapers = 0
    total_scrapers = len(test_classes)
    
    for test_class in test_classes:
        try:
            print(f"\n{'='*60}")
            results = await run_scraper_test(test_class)
            scraper_name = test_class().scraper_name.lower().replace(' ', '_')
            all_results[scraper_name] = results
            
            # Verificar si el scraper pasó los tests
            if 'overall' in results and results['overall']['success_rate'] >= 60:
                passed_scrapers += 1
                print(f"🎉 {test_class().scraper_name}: PASSED")
            else:
                print(f"⚠️  {test_class().scraper_name}: NEEDS ATTENTION")
                
        except Exception as e:
            print(f"❌ {test_class().scraper_name}: FAILED - {e}")
            all_results[test_class().scraper_name.lower().replace(' ', '_')] = {
                'error': str(e),
                'overall': {'success_rate': 0}
            }
    
    # Reporte final consolidado
    print(f"\n🎯 CONSOLIDATED TEST REPORT")
    print("=" * 50)
    print(f"⏰ Completed at: {datetime.now()}")
    print(f"📊 Scrapers tested: {total_scrapers}")
    print(f"✅ Scrapers passed: {passed_scrapers}")
    print(f"📈 Overall success rate: {(passed_scrapers/total_scrapers)*100:.1f}%")
    
    # Detalles por scraper
    print(f"\n📋 Detailed Results:")
    for scraper_name, results in all_results.items():
        if 'overall' in results:
            rate = results['overall']['success_rate']
            status = "✅" if rate >= 60 else "⚠️"
            print(f"   {status} {scraper_name}: {rate:.1f}% success rate")
        else:
            print(f"   ❌ {scraper_name}: Test failed to complete")
    
    # Recomendaciones
    if passed_scrapers == total_scrapers:
        print(f"\n🚀 RECOMMENDATION: All scrapers ready for production")
    elif passed_scrapers >= total_scrapers * 0.75:
        print(f"\n✅ RECOMMENDATION: Most scrapers ready, investigate failing ones")
    else:
        print(f"\n⚠️  RECOMMENDATION: Multiple scrapers need attention before proceeding")
    
    return all_results

if __name__ == "__main__":
    results = asyncio.run(run_comprehensive_test_suite())