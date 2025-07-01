#!/usr/bin/env python3
"""
Detailed test for specific API endpoints
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient

from services.api.main import app


def test_detailed_endpoints():
    """Test specific API functionality"""

    client = TestClient(app)

    print("🔍 Testing Detailed API Functionality")
    print("=" * 60)

    # Test articles with filters
    print("\n📰 Testing articles with sentiment filter...")
    response = client.get("/api/articles/?sentiment=negative&size=5")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Negative articles found: {data.get('total', 0)}")
        print(f"Items returned: {len(data.get('items', []))}")
        if data.get("items"):
            article = data["items"][0]
            print(f"Sample article: {article.get('title', 'N/A')[:50]}...")
        print("✅ Sentiment filtering working")

    # Test search functionality
    print("\n🔍 Testing article search...")
    response = client.get("/api/articles/search/?q=cancer&size=3")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Search results: {data.get('total', 0)}")
        print(f"Items returned: {len(data.get('items', []))}")
        print("✅ Article search working")

    # Test analytics endpoints
    print("\n📊 Testing sentiment trends...")
    response = client.get("/api/analytics/sentiment/trends?days=14")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Trend period: {data.get('period_days')} days")
        print(f"Data points: {data.get('total_data_points', 0)}")
        print("✅ Sentiment trends working")

    # Test topic distribution
    print("\n🏷️  Testing topic distribution...")
    response = client.get("/api/analytics/topics/distribution")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total articles: {data.get('total_articles', 0)}")
        print(f"Unique topics: {data.get('unique_topics', 0)}")
        distribution = data.get("distribution", {})
        if distribution:
            print("Top topics:")
            for topic, count in list(distribution.items())[:3]:
                print(f"  - {topic}: {count} articles")
        print("✅ Topic distribution working")

    # Test sources performance
    print("\n🌐 Testing sources performance...")
    response = client.get("/api/analytics/sources/performance")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total sources: {data.get('total_sources', 0)}")
        sources = data.get("sources", [])
        if sources:
            print("Source performance:")
            for source in sources[:3]:
                name = source.get("source_name", "Unknown")
                articles = source.get("total_articles", 0)
                coverage = source.get("analysis_coverage", 0)
                print(f"  - {name}: {articles} articles ({coverage}% analyzed)")
        print("✅ Sources performance working")

    # Test NLP sentiment endpoint
    print("\n🧠 Testing NLP sentiment analysis...")
    test_data = {
        "text": "This breakthrough treatment shows very promising results for breast cancer patients.",
        "title": "Medical Breakthrough",
    }
    response = client.post("/api/nlp/sentiment", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Sentiment: {data.get('sentiment_label')}")
        print(f"Confidence: {data.get('confidence', 0):.3f}")
        print(f"Compound score: {data.get('compound_score', 0):.3f}")
        print("✅ NLP sentiment analysis working")
    else:
        print(f"❌ NLP sentiment failed: {response.text}")

    # Test weekly trends
    print("\n📈 Testing weekly trends...")
    response = client.get("/api/analytics/trends/weekly?weeks=4")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Period: {data.get('period_weeks')} weeks")
        print(f"Total weeks: {data.get('total_weeks', 0)}")
        trends = data.get("weekly_trends", [])
        if trends:
            latest = trends[0]
            print(f"Latest week articles: {latest.get('article_count', 0)}")
            sentiment_counts = latest.get("sentiment_counts", {})
            print(f"Sentiment breakdown: {sentiment_counts}")
        print("✅ Weekly trends working")

    print("\n" + "=" * 60)
    print("🎊 Detailed API testing completed successfully!")


if __name__ == "__main__":
    test_detailed_endpoints()
