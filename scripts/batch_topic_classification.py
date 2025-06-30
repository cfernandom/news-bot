#!/usr/bin/env python3
"""
Batch Topic Classification for Existing Articles
Processes all articles and adds medical topic categories
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.data.database.connection import DatabaseManager
from services.nlp.src.topic_classifier import MedicalTopic, get_topic_classifier

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def process_topic_classification(batch_size: int = 50):
    """Process all articles to add topic classification"""
    logger.info("🏷️  Starting batch topic classification for existing articles")

    db_manager = DatabaseManager()
    topic_classifier = get_topic_classifier()

    try:
        # Initialize database
        await db_manager.initialize()
        if not await db_manager.health_check():
            logger.error("❌ Database health check failed")
            return False

        # Add topic_category column if it doesn't exist
        await ensure_topic_column(db_manager)

        # Get total articles needing classification
        count_query = """
        SELECT COUNT(*) FROM articles
        WHERE topic_category IS NULL OR topic_category = ''
        """
        result = await db_manager.execute_sql_one(count_query)
        total_articles = result[0] if result else 0

        logger.info(f"📊 Found {total_articles} articles to classify")

        if total_articles == 0:
            logger.warning("⚠️  No articles found requiring topic classification")
            await show_topic_statistics(db_manager)
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
            WHERE topic_category IS NULL OR topic_category = ''
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
                    # Classify topic
                    result = topic_classifier.classify_article(title, summary, content)

                    # Update database
                    update_query = """
                    UPDATE articles
                    SET topic_category = $2,
                        topic_confidence = $3,
                        updated_at = NOW()
                    WHERE id = $1
                    """

                    await db_manager.execute_sql(
                        update_query,
                        article_id,
                        result.primary_topic.value,
                        result.confidence,
                    )

                    updated += 1
                    processed += 1

                    if processed % 10 == 0:
                        logger.info(
                            f"⚡ Processed {processed}/{total_articles} articles..."
                        )

                except Exception as e:
                    logger.error(f"❌ Error classifying article {article_id}: {e}")
                    errors += 1
                    processed += 1

        logger.info("📋 Topic classification completed!")
        logger.info(f"   Total processed: {processed}")
        logger.info(f"   Successfully updated: {updated}")
        logger.info(f"   Errors: {errors}")

        # Show topic distribution
        await show_topic_statistics(db_manager)

        logger.info("🎉 Batch topic classification completed successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Critical error in topic classification: {e}")
        return False

    finally:
        await db_manager.close()


async def ensure_topic_column(db_manager):
    """Ensure topic_category and topic_confidence columns exist"""
    try:
        # Check if columns exist
        check_query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'articles'
        AND column_name IN ('topic_category', 'topic_confidence')
        """

        existing_columns = await db_manager.execute_sql(check_query)
        existing_column_names = [row[0] for row in existing_columns]

        # Add topic_category column if missing
        if "topic_category" not in existing_column_names:
            logger.info("🔧 Adding topic_category column to articles table")
            await db_manager.execute_sql(
                """
                ALTER TABLE articles
                ADD COLUMN topic_category VARCHAR(50)
            """
            )

        # Add topic_confidence column if missing
        if "topic_confidence" not in existing_column_names:
            logger.info("🔧 Adding topic_confidence column to articles table")
            await db_manager.execute_sql(
                """
                ALTER TABLE articles
                ADD COLUMN topic_confidence DECIMAL(4,3)
            """
            )

        logger.info("✅ Topic classification columns ready")

    except Exception as e:
        logger.error(f"❌ Error ensuring topic columns: {e}")
        raise


async def show_topic_statistics(db_manager):
    """Display topic classification statistics"""
    stats_query = """
    SELECT
        topic_category,
        COUNT(*) as count,
        ROUND(AVG(topic_confidence), 3) as avg_confidence,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage
    FROM articles
    WHERE topic_category IS NOT NULL AND topic_category != ''
    GROUP BY topic_category
    ORDER BY count DESC
    """

    results = await db_manager.execute_sql(stats_query)

    logger.info("\n📊 Topic Classification Statistics:")
    logger.info("   " + "=" * 70)
    logger.info(
        f"   {'Topic':<15} {'Count':<8} {'Avg Confidence':<15} {'Percentage':<10}"
    )
    logger.info("   " + "-" * 70)

    for row in results:
        topic, count, avg_conf, percentage = row
        logger.info(
            f"   {topic:<15} {count:<8} {avg_conf or 0:<15} {percentage or 0:<10}%"
        )

    # Show examples for each topic
    logger.info("\n📰 Topic Examples:")
    logger.info("   " + "=" * 70)

    for topic in ["treatment", "research", "diagnosis", "surgery"]:
        example_query = """
        SELECT title
        FROM articles
        WHERE topic_category = $1
        ORDER BY topic_confidence DESC
        LIMIT 1
        """

        example = await db_manager.execute_sql_one(example_query, topic)
        if example:
            title = example[0][:60] + "..." if len(example[0]) > 60 else example[0]
            logger.info(f"   {topic.capitalize():<12}: {title}")


if __name__ == "__main__":
    logger.info("🎯 PreventIA Medical Topic Classification")
    logger.info("=" * 60)

    asyncio.run(process_topic_classification())
