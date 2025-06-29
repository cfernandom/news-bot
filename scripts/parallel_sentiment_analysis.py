#!/usr/bin/env python3
"""
Parallel Batch Sentiment Analysis for High-Performance Processing
Processes articles using concurrent workers for improved throughput
"""

import asyncio
import sys
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.data.database.connection import DatabaseManager
from services.nlp.src.sentiment import get_sentiment_analyzer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def process_articles_parallel(batch_size: int = 50, max_workers: int = 4):
    """Process articles with parallel workers for improved performance"""
    logger.info("🚀 Starting parallel sentiment analysis for existing articles")
    start_time = time.time()
    
    db_manager = DatabaseManager()
    sentiment_analyzer = get_sentiment_analyzer()
    
    try:
        # Initialize database
        await db_manager.initialize()
        if not await db_manager.health_check():
            logger.error("❌ Database health check failed")
            return False
        
        # Get total articles needing processing
        count_query = """
        SELECT COUNT(*) FROM articles 
        WHERE sentiment_score IS NULL OR sentiment_label IS NULL
        """
        result = await db_manager.execute_sql_one(count_query)
        total_articles = result[0] if result else 0
        
        logger.info(f"📊 Found {total_articles} articles to process")
        
        if total_articles == 0:
            logger.warning("⚠️  No articles found requiring sentiment analysis")
            return True
        
        # Process in parallel batches
        processed = 0
        updated = 0
        errors = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for offset in range(0, total_articles, batch_size):
                logger.info(f"📦 Processing parallel batch {offset//batch_size + 1}")
                
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
                
                # Process articles in parallel using thread pool
                futures = []
                for article_data in articles_data:
                    article_id = article_data[0]
                    title = article_data[1] or ""
                    summary = article_data[2] or ""
                    content = article_data[3] or ""
                    
                    # Submit to thread pool for parallel processing
                    future = executor.submit(
                        process_single_article,
                        sentiment_analyzer,
                        article_id,
                        title,
                        summary,
                        content
                    )
                    futures.append((future, article_id))
                
                # Collect results and update database
                batch_updates = []
                for future, article_id in futures:
                    try:
                        result = future.result(timeout=30)  # 30s timeout per article
                        if result:
                            batch_updates.append((article_id, result))
                            processed += 1
                            
                            if processed % 10 == 0:
                                logger.info(f"⚡ Processed {processed}/{total_articles} articles...")
                        
                    except Exception as e:
                        logger.error(f"❌ Error processing article {article_id}: {e}")
                        errors += 1
                
                # Batch update database
                if batch_updates:
                    await update_articles_batch(db_manager, batch_updates)
                    updated += len(batch_updates)
        
        # Calculate performance metrics
        end_time = time.time()
        total_time = end_time - start_time
        articles_per_second = processed / total_time if total_time > 0 else 0
        
        logger.info("📋 Parallel processing completed!")
        logger.info(f"   Total processed: {processed}")
        logger.info(f"   Successfully updated: {updated}")
        logger.info(f"   Errors: {errors}")
        logger.info(f"   Processing time: {total_time:.2f} seconds")
        logger.info(f"   Performance: {articles_per_second:.2f} articles/second")
        
        # Show updated statistics
        await show_sentiment_statistics(db_manager)
        
        logger.info("🎉 Parallel sentiment analysis completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Critical error in parallel processing: {e}")
        return False
        
    finally:
        await db_manager.close()

def process_single_article(analyzer, article_id, title, summary, content):
    """Process single article sentiment (thread-safe function)"""
    try:
        # Use summary if available, otherwise use content
        text_to_analyze = summary if summary.strip() else content
        
        if not text_to_analyze.strip():
            return None
        
        # Analyze sentiment
        result = analyzer.analyze_sentiment(text_to_analyze, title)
        
        return {
            'sentiment_score': result['scores']['compound'],
            'sentiment_label': result['sentiment_label'],
            'confidence': result['confidence']
        }
        
    except Exception as e:
        logger.error(f"Error analyzing article {article_id}: {e}")
        return None

async def update_articles_batch(db_manager, batch_updates):
    """Update multiple articles in a single transaction"""
    update_query = """
    UPDATE articles 
    SET sentiment_score = $2,
        sentiment_label = $3,
        confidence_score = $4,
        updated_at = NOW()
    WHERE id = $1
    """
    
    async with db_manager.get_connection() as conn:
        async with conn.transaction():
            for article_id, sentiment_data in batch_updates:
                await conn.execute(
                    update_query,
                    article_id,
                    sentiment_data['sentiment_score'],
                    sentiment_data['sentiment_label'],
                    sentiment_data['confidence']
                )

async def show_sentiment_statistics(db_manager):
    """Display updated sentiment analysis statistics"""
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
    
    results = await db_manager.execute_sql(stats_query)
    
    logger.info("\n📊 Sentiment Analysis Statistics:")
    logger.info("   ==================================================")
    for row in results:
        label, count, avg_score, min_score, max_score = row
        logger.info(f"   {label:>8}: {count:>3} articles (avg: {avg_score:>6}, range: {min_score} to {max_score})")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Parallel Sentiment Analysis')
    parser.add_argument('--batch-size', type=int, default=50, help='Batch size for processing')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    
    args = parser.parse_args()
    
    logger.info("🎯 PreventIA Parallel Sentiment Analysis")
    logger.info("=" * 60)
    logger.info(f"⚙️  Configuration: {args.workers} workers, batch size {args.batch_size}")
    
    asyncio.run(process_articles_parallel(args.batch_size, args.workers))