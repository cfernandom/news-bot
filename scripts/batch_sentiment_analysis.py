#!/usr/bin/env python3
"""
Batch Sentiment Analysis for Existing Articles
Processes all articles in database and updates sentiment data
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.data.database.connection import DatabaseManager
from services.nlp.src.sentiment import get_sentiment_analyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def process_articles_batch(batch_size: int = 50):
    """Process all articles in batches to update sentiment data"""
    logger.info("🚀 Starting batch sentiment analysis for existing articles")

    db_manager = DatabaseManager()
    sentiment_analyzer = get_sentiment_analyzer()

    try:
        # Check database health
        if not await db_manager.health_check():
            logger.error("❌ Database is not available")
            return False

        # Get total article count
        count_query = "SELECT COUNT(*) FROM articles"
        total_count_result = await db_manager.execute_sql(count_query)
        total_articles = total_count_result[0][0] if total_count_result else 0

        logger.info(f"📊 Found {total_articles} articles to process")

        if total_articles == 0:
            logger.warning("⚠️  No articles found in database")
            return True

        # Process in batches
        processed = 0
        updated = 0
        errors = 0

        for offset in range(0, total_articles, batch_size):
            logger.info(
                f"📦 Processing batch {offset//batch_size + 1} (articles {offset+1}-{min(offset+batch_size, total_articles)})"
            )

            # Get batch of articles
            query = """
            SELECT id, title, summary, content
            FROM articles
            WHERE sentiment_score IS NULL OR sentiment_label IS NULL
            ORDER BY published_at DESC
            LIMIT $1 OFFSET $2
            """

            articles_data = await db_manager.execute_sql(query, batch_size, offset)

            if not articles_data:
                logger.info("✅ No more articles to process")
                break

            # Process each article in the batch
            for article_data in articles_data:
                article_id = article_data[0]
                title = article_data[1] or ""
                summary = article_data[2] or ""
                content = article_data[3] or ""

                try:
                    # Use summary if available, otherwise use content
                    text_to_analyze = summary if summary.strip() else content

                    if not text_to_analyze.strip():
                        logger.warning(
                            f"⚠️  Article {article_id} has no content to analyze"
                        )
                        processed += 1
                        continue

                    # Analyze sentiment
                    sentiment_result = sentiment_analyzer.analyze_sentiment(
                        text=text_to_analyze, title=title
                    )

                    # Update database with sentiment data
                    update_query = """
                    UPDATE articles
                    SET
                        sentiment_score = $1,
                        sentiment_label = $2,
                        processing_status = 'analyzed'
                    WHERE id = $3
                    """

                    await db_manager.execute_sql(
                        update_query,
                        sentiment_result["scores"]["compound"],
                        sentiment_result["sentiment_label"],
                        article_id,
                    )

                    updated += 1
                    processed += 1

                    if processed % 10 == 0:
                        logger.info(
                            f"⚡ Processed {processed}/{total_articles} articles..."
                        )

                except Exception as e:
                    logger.error(f"❌ Error processing article {article_id}: {e}")
                    errors += 1
                    processed += 1

        # Final summary
        logger.info("📋 Batch processing completed!")
        logger.info(f"   Total processed: {processed}")
        logger.info(f"   Successfully updated: {updated}")
        logger.info(f"   Errors: {errors}")

        # Show sentiment distribution
        await show_sentiment_stats(db_manager)

        return True

    except Exception as e:
        logger.error(f"❌ Batch processing failed: {e}")
        return False


async def show_sentiment_stats(db_manager: DatabaseManager):
    """Show sentiment analysis statistics"""
    logger.info("\n📊 Sentiment Analysis Statistics:")

    # Get sentiment distribution
    stats_query = """
    SELECT
        sentiment_label,
        COUNT(*) as count,
        ROUND(AVG(sentiment_score), 3) as avg_score,
        ROUND(MIN(sentiment_score), 3) as min_score,
        ROUND(MAX(sentiment_score), 3) as max_score
    FROM articles
    WHERE sentiment_label IS NOT NULL
    GROUP BY sentiment_label
    ORDER BY count DESC
    """

    stats_data = await db_manager.execute_sql(stats_query)

    if stats_data:
        print("\n   Sentiment Distribution:")
        print("   " + "=" * 50)
        for row in stats_data:
            label, count, avg_score, min_score, max_score = row
            print(
                f"   {label:>8}: {count:>3} articles (avg: {avg_score:>6}, range: {min_score} to {max_score})"
            )

    # Get recent examples
    examples_query = """
    SELECT title, sentiment_label, sentiment_score
    FROM articles
    WHERE sentiment_label IS NOT NULL
    ORDER BY published_at DESC
    LIMIT 5
    """

    examples_data = await db_manager.execute_sql(examples_query)

    if examples_data:
        print("\n   Recent Examples:")
        print("   " + "=" * 50)
        for title, label, score in examples_data:
            title_short = title[:40] + "..." if len(title) > 40 else title
            print(f"   {label:>8} ({score:>6}): {title_short}")


async def main():
    """Main function"""
    logger.info("🎯 PreventIA Batch Sentiment Analysis")
    logger.info("=" * 60)

    try:
        success = await process_articles_batch(batch_size=50)

        if success:
            logger.info("🎉 Batch sentiment analysis completed successfully!")
            return True
        else:
            logger.error("❌ Batch sentiment analysis failed")
            return False

    except KeyboardInterrupt:
        logger.warning("⚠️  Process interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
