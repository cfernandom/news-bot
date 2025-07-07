"""
Optimized database queries for PreventIA News Analytics
High-performance queries for analytics dashboard with caching and indexing
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .connection import DatabaseManager


class OptimizedQueries:
    """
    Optimized database queries for analytics dashboard performance
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def get_analytics_summary(
        self, days: int = 30, use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive analytics summary with optimized single query
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        query = """
        WITH recent_articles AS (
            SELECT
                id,
                sentiment_label,
                topic_category,
                published_at,
                source_id,
                CASE
                    WHEN published_at >= $1 THEN 1
                    ELSE 0
                END as is_recent
            FROM articles
            WHERE processing_status = 'completed'
        ),
        sentiment_stats AS (
            SELECT
                sentiment_label,
                COUNT(*) as total_count,
                COUNT(*) FILTER (WHERE is_recent = 1) as recent_count,
                AVG(CASE WHEN sentiment_score IS NOT NULL THEN sentiment_score ELSE 0 END) as avg_score
            FROM recent_articles
            WHERE sentiment_label IS NOT NULL
            GROUP BY sentiment_label
        ),
        topic_stats AS (
            SELECT
                topic_category,
                COUNT(*) as total_count,
                COUNT(*) FILTER (WHERE is_recent = 1) as recent_count
            FROM recent_articles
            WHERE topic_category IS NOT NULL
            GROUP BY topic_category
        ),
        source_stats AS (
            SELECT
                s.name as source_name,
                COUNT(ra.id) as total_articles,
                COUNT(ra.id) FILTER (WHERE ra.is_recent = 1) as recent_articles
            FROM recent_articles ra
            JOIN news_sources s ON ra.source_id = s.id
            GROUP BY s.name
        ),
        daily_counts AS (
            SELECT
                DATE(published_at) as date,
                COUNT(*) as count
            FROM recent_articles
            WHERE published_at >= $1
            GROUP BY DATE(published_at)
            ORDER BY date
        )
        SELECT
            (SELECT COUNT(*) FROM recent_articles) as total_articles,
            (SELECT COUNT(*) FROM recent_articles WHERE is_recent = 1) as recent_articles,
            (SELECT json_agg(json_build_object('sentiment', sentiment_label, 'count', total_count, 'recent_count', recent_count, 'avg_score', avg_score)) FROM sentiment_stats) as sentiment_data,
            (SELECT json_agg(json_build_object('topic', topic_category, 'count', total_count, 'recent_count', recent_count)) FROM topic_stats) as topic_data,
            (SELECT json_agg(json_build_object('source', source_name, 'total', total_articles, 'recent', recent_articles)) FROM source_stats) as source_data,
            (SELECT json_agg(json_build_object('date', date, 'count', count)) FROM daily_counts) as daily_data
        """

        async with self.db_manager.get_connection() as conn:
            result = await conn.fetchrow(query, cutoff_date)

            return {
                "total_articles": result["total_articles"],
                "recent_articles": result["recent_articles"],
                "sentiment_distribution": result["sentiment_data"] or [],
                "topic_distribution": result["topic_data"] or [],
                "source_distribution": result["source_data"] or [],
                "daily_counts": result["daily_data"] or [],
                "analysis_period": days,
                "cutoff_date": cutoff_date.isoformat(),
            }

    async def get_sentiment_trends(
        self, days: int = 30, granularity: str = "daily"
    ) -> List[Dict[str, Any]]:
        """
        Get sentiment trends over time with configurable granularity
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        if granularity == "daily":
            date_trunc = "day"
        elif granularity == "weekly":
            date_trunc = "week"
        elif granularity == "monthly":
            date_trunc = "month"
        else:
            date_trunc = "day"

        query = f"""
        WITH sentiment_by_period AS (
            SELECT
                date_trunc('{date_trunc}', published_at) as period,
                sentiment_label,
                COUNT(*) as count,
                AVG(sentiment_score) as avg_score
            FROM articles
            WHERE published_at >= $1
                AND sentiment_label IS NOT NULL
                AND processing_status = 'completed'
            GROUP BY period, sentiment_label
        ),
        periods AS (
            SELECT generate_series(
                date_trunc('{date_trunc}', $1),
                date_trunc('{date_trunc}', NOW()),
                '1 {date_trunc}'::interval
            ) as period
        )
        SELECT
            p.period,
            COALESCE(
                json_agg(
                    json_build_object(
                        'sentiment', s.sentiment_label,
                        'count', s.count,
                        'avg_score', s.avg_score
                    )
                ) FILTER (WHERE s.sentiment_label IS NOT NULL),
                '[]'::json
            ) as sentiment_data
        FROM periods p
        LEFT JOIN sentiment_by_period s ON p.period = s.period
        GROUP BY p.period
        ORDER BY p.period
        """

        async with self.db_manager.get_connection() as conn:
            results = await conn.fetch(query, cutoff_date)

            return [
                {
                    "period": row["period"].isoformat(),
                    "sentiment_data": row["sentiment_data"],
                }
                for row in results
            ]

    async def get_geographic_distribution(self) -> List[Dict[str, Any]]:
        """
        Get geographic distribution of articles with optimized query
        """
        query = """
        WITH geographic_stats AS (
            SELECT
                COALESCE(geographic_focus, 'Unknown') as region,
                COUNT(*) as article_count,
                COUNT(DISTINCT source_id) as source_count,
                AVG(CASE WHEN sentiment_score IS NOT NULL THEN sentiment_score ELSE 0 END) as avg_sentiment,
                MAX(published_at) as latest_article
            FROM articles
            WHERE processing_status = 'completed'
            GROUP BY geographic_focus
        )
        SELECT
            region,
            article_count,
            source_count,
            avg_sentiment,
            latest_article,
            ROUND(
                (article_count * 100.0 / (SELECT SUM(article_count) FROM geographic_stats))::numeric,
                2
            ) as percentage
        FROM geographic_stats
        ORDER BY article_count DESC
        """

        async with self.db_manager.get_connection() as conn:
            results = await conn.fetch(query)

            return [
                {
                    "region": row["region"],
                    "article_count": row["article_count"],
                    "source_count": row["source_count"],
                    "avg_sentiment": (
                        float(row["avg_sentiment"]) if row["avg_sentiment"] else 0.0
                    ),
                    "latest_article": (
                        row["latest_article"].isoformat()
                        if row["latest_article"]
                        else None
                    ),
                    "percentage": (
                        float(row["percentage"]) if row["percentage"] else 0.0
                    ),
                }
                for row in results
            ]

    async def get_top_keywords(
        self, days: int = 30, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get top keywords with frequency and sentiment analysis
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        query = """
        WITH keyword_stats AS (
            SELECT
                ak.keyword,
                COUNT(*) as frequency,
                AVG(ak.relevance_score) as avg_relevance,
                AVG(a.sentiment_score) as avg_sentiment,
                array_agg(DISTINCT a.sentiment_label) as sentiment_labels,
                MAX(a.published_at) as latest_mention
            FROM article_keywords ak
            JOIN articles a ON ak.article_id = a.id
            WHERE a.published_at >= $1
                AND a.processing_status = 'completed'
            GROUP BY ak.keyword
        )
        SELECT
            keyword,
            frequency,
            avg_relevance,
            avg_sentiment,
            sentiment_labels,
            latest_mention,
            ROUND(
                (frequency * 100.0 / (SELECT SUM(frequency) FROM keyword_stats))::numeric,
                3
            ) as percentage
        FROM keyword_stats
        ORDER BY frequency DESC
        LIMIT $2
        """

        async with self.db_manager.get_connection() as conn:
            results = await conn.fetch(query, cutoff_date, limit)

            return [
                {
                    "keyword": row["keyword"],
                    "frequency": row["frequency"],
                    "avg_relevance": (
                        float(row["avg_relevance"]) if row["avg_relevance"] else 0.0
                    ),
                    "avg_sentiment": (
                        float(row["avg_sentiment"]) if row["avg_sentiment"] else 0.0
                    ),
                    "sentiment_labels": row["sentiment_labels"],
                    "latest_mention": (
                        row["latest_mention"].isoformat()
                        if row["latest_mention"]
                        else None
                    ),
                    "percentage": (
                        float(row["percentage"]) if row["percentage"] else 0.0
                    ),
                }
                for row in results
            ]

    async def get_source_performance(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get source performance metrics with optimized query
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        query = """
        WITH source_performance AS (
            SELECT
                s.name as source_name,
                s.url as source_url,
                COUNT(a.id) as total_articles,
                COUNT(a.id) FILTER (WHERE a.published_at >= $1) as recent_articles,
                AVG(a.sentiment_score) as avg_sentiment,
                COUNT(DISTINCT a.topic_category) as topic_diversity,
                MAX(a.published_at) as latest_article,
                MIN(a.published_at) as earliest_article,
                ROUND(
                    COUNT(a.id) * 1.0 / NULLIF(
                        EXTRACT(days FROM (MAX(a.published_at) - MIN(a.published_at))), 0
                    ), 2
                ) as articles_per_day
            FROM news_sources s
            LEFT JOIN articles a ON s.id = a.source_id
            WHERE a.processing_status = 'completed' OR a.processing_status IS NULL
            GROUP BY s.id, s.name, s.url
        )
        SELECT
            source_name,
            source_url,
            total_articles,
            recent_articles,
            avg_sentiment,
            topic_diversity,
            latest_article,
            earliest_article,
            articles_per_day,
            CASE
                WHEN recent_articles > 0 THEN 'active'
                WHEN latest_article > (NOW() - INTERVAL '7 days') THEN 'recent'
                ELSE 'inactive'
            END as activity_status
        FROM source_performance
        ORDER BY total_articles DESC
        """

        async with self.db_manager.get_connection() as conn:
            results = await conn.fetch(query, cutoff_date)

            return [
                {
                    "source_name": row["source_name"],
                    "source_url": row["source_url"],
                    "total_articles": row["total_articles"],
                    "recent_articles": row["recent_articles"],
                    "avg_sentiment": (
                        float(row["avg_sentiment"]) if row["avg_sentiment"] else 0.0
                    ),
                    "topic_diversity": row["topic_diversity"],
                    "latest_article": (
                        row["latest_article"].isoformat()
                        if row["latest_article"]
                        else None
                    ),
                    "earliest_article": (
                        row["earliest_article"].isoformat()
                        if row["earliest_article"]
                        else None
                    ),
                    "articles_per_day": (
                        float(row["articles_per_day"])
                        if row["articles_per_day"]
                        else 0.0
                    ),
                    "activity_status": row["activity_status"],
                }
                for row in results
            ]

    async def get_search_optimized(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
        sentiment_filter: Optional[str] = None,
        topic_filter: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Optimized search with full-text search and filters
        """
        conditions = ["processing_status = 'completed'"]
        params = []
        param_count = 0

        # Full-text search
        if query.strip():
            param_count += 1
            conditions.append(
                f"(title ILIKE ${param_count} OR content ILIKE ${param_count} OR summary ILIKE ${param_count})"
            )
            params.append(f"%{query}%")

        # Sentiment filter
        if sentiment_filter:
            param_count += 1
            conditions.append(f"sentiment_label = ${param_count}")
            params.append(sentiment_filter)

        # Topic filter
        if topic_filter:
            param_count += 1
            conditions.append(f"topic_category = ${param_count}")
            params.append(topic_filter)

        # Date filters
        if date_from:
            param_count += 1
            conditions.append(f"published_at >= ${param_count}")
            params.append(date_from)

        if date_to:
            param_count += 1
            conditions.append(f"published_at <= ${param_count}")
            params.append(date_to)

        where_clause = " AND ".join(conditions)

        # Count query
        count_query = f"""
        SELECT COUNT(*)
        FROM articles a
        JOIN news_sources s ON a.source_id = s.id
        WHERE {where_clause}
        """

        # Main query with pagination
        param_count += 1
        limit_param = param_count
        param_count += 1
        offset_param = param_count

        main_query = f"""
        SELECT
            a.id,
            a.title,
            a.summary,
            a.url,
            a.published_at,
            a.sentiment_label,
            a.sentiment_score,
            a.topic_category,
            s.name as source_name,
            s.url as source_url
        FROM articles a
        JOIN news_sources s ON a.source_id = s.id
        WHERE {where_clause}
        ORDER BY a.published_at DESC
        LIMIT ${limit_param} OFFSET ${offset_param}
        """

        params.extend([limit, offset])

        async with self.db_manager.get_connection() as conn:
            # Get total count
            count_result = await conn.fetchval(count_query, *params[:-2])

            # Get results
            results = await conn.fetch(main_query, *params)

            articles = [
                {
                    "id": row["id"],
                    "title": row["title"],
                    "summary": row["summary"],
                    "url": row["url"],
                    "published_at": row["published_at"].isoformat(),
                    "sentiment_label": row["sentiment_label"],
                    "sentiment_score": (
                        float(row["sentiment_score"])
                        if row["sentiment_score"]
                        else None
                    ),
                    "topic_category": row["topic_category"],
                    "source_name": row["source_name"],
                    "source_url": row["source_url"],
                }
                for row in results
            ]

            return articles, count_result

    async def create_database_indexes(self):
        """
        Create optimized indexes for analytics queries
        """
        indexes = [
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_published_at ON articles(published_at DESC)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_sentiment_label ON articles(sentiment_label)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_topic_category ON articles(topic_category)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_source_id ON articles(source_id)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_processing_status ON articles(processing_status)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_sentiment_score ON articles(sentiment_score)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_geographic_focus ON articles(geographic_focus)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_article_keywords_keyword ON article_keywords(keyword)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_article_keywords_relevance ON article_keywords(relevance_score DESC)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_fulltext ON articles USING gin(to_tsvector('english', title || ' ' || content || ' ' || summary))",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_composite_analytics ON articles(processing_status, published_at DESC, sentiment_label, topic_category)",
        ]

        async with self.db_manager.get_connection() as conn:
            for index_sql in indexes:
                try:
                    await conn.execute(index_sql)
                    print(f"Created index: {index_sql}")
                except Exception as e:
                    print(f"Index creation failed or already exists: {e}")

    async def analyze_database_statistics(self):
        """
        Update database statistics for query optimization
        """
        analyze_queries = [
            "ANALYZE articles",
            "ANALYZE news_sources",
            "ANALYZE article_keywords",
            "VACUUM ANALYZE articles",
            "VACUUM ANALYZE news_sources",
            "VACUUM ANALYZE article_keywords",
        ]

        async with self.db_manager.get_connection() as conn:
            for query in analyze_queries:
                try:
                    await conn.execute(query)
                    print(f"Executed: {query}")
                except Exception as e:
                    print(f"Query failed: {e}")


# Global instance
_optimized_queries: Optional[OptimizedQueries] = None


async def get_optimized_queries() -> OptimizedQueries:
    """Get singleton instance of optimized queries"""
    global _optimized_queries
    if _optimized_queries is None:
        from .connection import get_db_manager

        db_manager = await get_db_manager()
        _optimized_queries = OptimizedQueries(db_manager)
    return _optimized_queries
