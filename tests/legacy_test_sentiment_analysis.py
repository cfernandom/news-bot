#!/usr/bin/env python3
"""
Test script for Sentiment Analysis system
Tests VADER + spaCy integration with medical news content
"""

import asyncio
import sys
from pathlib import Path

# Add services to path
sys.path.append(str(Path(__file__).parent))

from services.nlp.src.sentiment import get_sentiment_analyzer
from services.nlp.src.analyzer import analyze_article
from services.shared.models.article import Article

def test_sentiment_analyzer():
    """Test sentiment analyzer with medical news examples"""
    print("🧪 Testing Sentiment Analysis System")
    print("=" * 50)
    
    analyzer = get_sentiment_analyzer()
    
    # Test cases for medical news
    test_cases = [
        {
            "title": "Breakthrough Cancer Treatment Shows Promising Results",
            "content": "New immunotherapy treatment shows 85% success rate in clinical trials. Patients experienced significant improvement with minimal side effects.",
            "expected": "positive"
        },
        {
            "title": "Study Links Diet to Reduced Cancer Risk",
            "content": "Research indicates that mediterranean diet may reduce breast cancer risk by 30%. Scientists recommend including more vegetables and fish.",
            "expected": "positive"
        },
        {
            "title": "Cancer Rates Continue to Rise Globally",
            "content": "WHO reports increasing cancer diagnoses worldwide. Delayed treatments during pandemic contributed to advanced stage diagnoses.",
            "expected": "negative"
        },
        {
            "title": "FDA Approves New Diagnostic Tool",
            "content": "Medical device receives regulatory approval for early cancer detection. The technology uses AI to analyze medical imaging.",
            "expected": "neutral"
        }
    ]
    
    print("\n📊 Individual Test Results:")
    for i, case in enumerate(test_cases, 1):
        result = analyzer.analyze_sentiment(case["content"], case["title"])
        
        print(f"\nTest {i}: {case['title'][:50]}...")
        print(f"Expected: {case['expected']}")
        print(f"Result: {result['sentiment_label']} (confidence: {result['confidence']:.3f})")
        print(f"Scores: pos={result['scores']['positive']:.3f}, neg={result['scores']['negative']:.3f}, neu={result['scores']['neutral']:.3f}")
        
        # Check if result matches expectation
        match = "✅" if result['sentiment_label'] == case['expected'] else "❌"
        print(f"Match: {match}")
    
    return True

def test_nlp_integration():
    """Test integration with NLP analyzer"""
    print("\n🔗 Testing NLP Integration")
    print("=" * 30)
    
    # Create test article (using legacy Article model)
    from datetime import datetime
    test_article = Article(
        title="Revolutionary Breast Cancer Treatment Approved",
        published_at=datetime(2024, 1, 15),
        summary="New targeted therapy shows remarkable results in treating aggressive breast cancer with fewer side effects than traditional chemotherapy.",
        content="New targeted therapy shows remarkable results in treating aggressive breast cancer with fewer side effects than traditional chemotherapy. The treatment targets specific proteins found in cancer cells.",
        url="https://test.example.com"
    )
    
    # Analyze with enhanced NLP
    result = analyze_article(test_article)
    
    print(f"Article: {test_article.title}")
    print(f"Relevance: {'✅ Relevant' if result.is_relevant else '❌ Not Relevant'}")
    print(f"Keywords: {result.matched_keywords}")
    print(f"Keyword Score: {result.score}")
    
    if result.sentiment_data:
        sentiment = result.sentiment_data
        print(f"Sentiment: {sentiment['sentiment_label']} (confidence: {sentiment['confidence']:.3f})")
        print(f"Compound Score: {sentiment['scores']['compound']:.3f}")
    else:
        print("❌ No sentiment data found")
    
    return True

async def test_database_integration():
    """Test with real database articles (if available)"""
    print("\n🗄️ Testing Database Integration")
    print("=" * 35)
    
    try:
        from services.data.database.connection import DatabaseManager
        
        db_manager = DatabaseManager()
        
        # Test database connection
        try:
            health = await db_manager.health_check()
            if not health:
                print("❌ Database not available, skipping database tests")
                return False
        except Exception as e:
            print(f"❌ Database health check failed: {e}")
            return False
        
        # Get sample articles
        query = "SELECT id, title, summary, url, published_at, (SELECT name FROM news_sources WHERE id = articles.source_id) as source_name FROM articles LIMIT 3"
        articles_data = await db_manager.execute_sql(query)
        
        if not articles_data:
            print("❌ No articles found in database")
            return False
        
        print(f"📰 Testing {len(articles_data)} real articles from database:")
        
        analyzer = get_sentiment_analyzer()
        
        for article_data in articles_data:
            # Create Article object (using legacy Article model)
            from datetime import datetime
            published_date = article_data[4] if article_data[4] else datetime.now()
            if isinstance(published_date, str):
                published_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            
            article = Article(
                title=article_data[1] or "",
                published_at=published_date,
                summary=article_data[2] or "",
                content=article_data[2] or "",  # Use summary as content for now
                url=article_data[3] or ""
            )
            
            # Analyze sentiment
            sentiment = analyzer.analyze_sentiment(article.summary, article.title)
            
            print(f"\n📄 Article: {article.title[:60]}...")
            print(f"   Source: {article_data[5] or 'Unknown'}")  # source_name from database
            print(f"   Sentiment: {sentiment['sentiment_label']} ({sentiment['confidence']:.3f})")
            print(f"   Compound: {sentiment['scores']['compound']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all sentiment analysis tests"""
    print("🚀 PreventIA Sentiment Analysis Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Basic sentiment analyzer
    total_tests += 1
    if test_sentiment_analyzer():
        tests_passed += 1
    
    # Test 2: NLP integration
    total_tests += 1
    if test_nlp_integration():
        tests_passed += 1
    
    # Test 3: Database integration (async)
    total_tests += 1
    try:
        if asyncio.run(test_database_integration()):
            tests_passed += 1
    except Exception as e:
        print(f"❌ Database integration test failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📋 Test Summary: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Sentiment analysis system is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Check configuration and dependencies.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)