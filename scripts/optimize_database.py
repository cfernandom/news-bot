#!/usr/bin/env python3
"""
Database optimization script for PreventIA News Analytics
Creates indexes, updates statistics, and optimizes performance
"""

import asyncio
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.data.database.connection import DatabaseManager
from services.data.database.optimized_queries import OptimizedQueries


async def optimize_database():
    """
    Run complete database optimization
    """
    print("🔧 Starting database optimization...")
    print(f"📅 Started at: {datetime.now()}")

    # Initialize database manager
    db_manager = DatabaseManager()
    await db_manager.initialize()

    # Create optimized queries instance
    optimized_queries = OptimizedQueries(db_manager)

    try:
        # Step 1: Create optimized indexes
        print("\n📊 Creating database indexes...")
        await optimized_queries.create_database_indexes()

        # Step 2: Update statistics
        print("\n📈 Updating database statistics...")
        await optimized_queries.analyze_database_statistics()

        # Step 3: Test optimized queries
        print("\n🧪 Testing optimized queries...")

        # Test analytics summary
        start_time = datetime.now()
        summary = await optimized_queries.get_analytics_summary(days=30)
        analytics_time = (datetime.now() - start_time).total_seconds()
        print(f"  ✅ Analytics summary: {analytics_time:.2f}s")
        print(f"     Total articles: {summary['total_articles']}")
        print(f"     Recent articles: {summary['recent_articles']}")

        # Test sentiment trends
        start_time = datetime.now()
        trends = await optimized_queries.get_sentiment_trends(days=30)
        trends_time = (datetime.now() - start_time).total_seconds()
        print(f"  ✅ Sentiment trends: {trends_time:.2f}s")
        print(f"     Trend points: {len(trends)}")

        # Test geographic distribution
        start_time = datetime.now()
        geo_data = await optimized_queries.get_geographic_distribution()
        geo_time = (datetime.now() - start_time).total_seconds()
        print(f"  ✅ Geographic distribution: {geo_time:.2f}s")
        print(f"     Regions: {len(geo_data)}")

        # Test top keywords
        start_time = datetime.now()
        keywords = await optimized_queries.get_top_keywords(days=30, limit=20)
        keywords_time = (datetime.now() - start_time).total_seconds()
        print(f"  ✅ Top keywords: {keywords_time:.2f}s")
        print(f"     Keywords: {len(keywords)}")

        # Test source performance
        start_time = datetime.now()
        sources = await optimized_queries.get_source_performance(days=30)
        sources_time = (datetime.now() - start_time).total_seconds()
        print(f"  ✅ Source performance: {sources_time:.2f}s")
        print(f"     Sources: {len(sources)}")

        # Test search optimization
        start_time = datetime.now()
        search_results, total_count = await optimized_queries.get_search_optimized(
            query="breast cancer", limit=20, offset=0
        )
        search_time = (datetime.now() - start_time).total_seconds()
        print(f"  ✅ Optimized search: {search_time:.2f}s")
        print(f"     Results: {len(search_results)}/{total_count}")

        # Calculate total performance
        total_time = (
            analytics_time
            + trends_time
            + geo_time
            + keywords_time
            + sources_time
            + search_time
        )
        print(f"\n⚡ Total query time: {total_time:.2f}s")

        # Performance benchmarks
        print("\n📊 Performance Analysis:")
        if total_time < 10:
            print("  🟢 Excellent performance (<10s)")
        elif total_time < 20:
            print("  🟡 Good performance (10-20s)")
        else:
            print("  🔴 Performance needs improvement (>20s)")

        # Database statistics
        print("\n📋 Database Statistics:")
        async with db_manager.get_connection() as conn:
            # Table sizes
            table_stats = await conn.fetch(
                """
                SELECT
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            """
            )

            for row in table_stats:
                print(f"  📊 {row['tablename']}: {row['size']}")

            # Index usage
            index_stats = await conn.fetch(
                """
                SELECT
                    schemaname,
                    tablename,
                    indexname,
                    idx_scan,
                    idx_tup_read,
                    idx_tup_fetch
                FROM pg_stat_user_indexes
                WHERE schemaname = 'public'
                ORDER BY idx_scan DESC
                LIMIT 10
            """
            )

            print("\n🔍 Top Index Usage:")
            for row in index_stats:
                print(f"  📈 {row['indexname']}: {row['idx_scan']} scans")

    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        raise
    finally:
        # Cleanup
        if hasattr(db_manager, "_pool") and db_manager._pool:
            await db_manager._pool.close()

    print(f"\n✅ Database optimization completed at: {datetime.now()}")


async def check_database_health():
    """
    Check database health and performance metrics
    """
    print("🏥 Checking database health...")

    db_manager = DatabaseManager()
    await db_manager.initialize()

    try:
        async with db_manager.get_connection() as conn:
            # Connection test
            result = await conn.fetchval("SELECT 1")
            print(f"  ✅ Connection test: {result}")

            # Version check
            version = await conn.fetchval("SELECT version()")
            print(f"  📋 PostgreSQL version: {version.split()[1]}")

            # Database size
            db_size = await conn.fetchval(
                """
                SELECT pg_size_pretty(pg_database_size(current_database()))
            """
            )
            print(f"  💾 Database size: {db_size}")

            # Active connections
            connections = await conn.fetchval(
                """
                SELECT count(*) FROM pg_stat_activity
                WHERE state = 'active'
            """
            )
            print(f"  🔗 Active connections: {connections}")

            # Table record counts
            tables = ["articles", "news_sources", "article_keywords"]
            for table in tables:
                try:
                    count = await conn.fetchval(f"SELECT COUNT(*) FROM {table}")
                    print(f"  📊 {table}: {count:,} records")
                except Exception as e:
                    print(f"  ❌ {table}: Error - {e}")

            # Check for missing indexes
            missing_indexes = await conn.fetch(
                """
                SELECT
                    schemaname,
                    tablename,
                    seq_scan,
                    seq_tup_read,
                    idx_scan,
                    n_tup_ins + n_tup_upd + n_tup_del as writes
                FROM pg_stat_user_tables
                WHERE schemaname = 'public'
                  AND (seq_scan > 1000 OR seq_tup_read > 100000)
                ORDER BY seq_tup_read DESC
            """
            )

            if missing_indexes:
                print("\n⚠️  Tables with high sequential scans (may need indexes):")
                for row in missing_indexes:
                    print(
                        f"  📊 {row['tablename']}: {row['seq_scan']} scans, {row['seq_tup_read']} reads"
                    )

    except Exception as e:
        print(f"❌ Health check failed: {e}")
        raise
    finally:
        if hasattr(db_manager, "_pool") and db_manager._pool:
            await db_manager._pool.close()


async def main():
    """
    Main function to run database optimization
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Database optimization for PreventIA News Analytics"
    )
    parser.add_argument(
        "--health", action="store_true", help="Check database health only"
    )
    parser.add_argument("--optimize", action="store_true", help="Run full optimization")
    parser.add_argument(
        "--all", action="store_true", help="Run health check and optimization"
    )

    args = parser.parse_args()

    if args.health or args.all:
        await check_database_health()

    if args.optimize or args.all:
        await optimize_database()

    if not any([args.health, args.optimize, args.all]):
        print("No action specified. Use --health, --optimize, or --all")
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
