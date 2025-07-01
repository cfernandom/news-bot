#!/usr/bin/env python3
"""
Quick test script for FastAPI endpoints
"""

import asyncio
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient

from services.api.main import app


def test_basic_endpoints():
    """Test basic API endpoints"""

    client = TestClient(app)

    print("🧪 Testing PreventIA News Analytics API")
    print("=" * 50)

    # Test root endpoint
    print("\n📍 Testing root endpoint...")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Message: {data.get('message')}")
        print(f"Version: {data.get('version')}")
        print("✅ Root endpoint working")
    else:
        print("❌ Root endpoint failed")
        print(f"Error: {response.text}")

    # Test health endpoint
    print("\n🏥 Testing health endpoint...")
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Health Status: {data.get('status')}")
        print(f"Database: {data.get('database')}")
        print(f"Articles Count: {data.get('articles_count')}")
        print("✅ Health endpoint working")
    else:
        print("❌ Health endpoint failed")
        print(f"Error: {response.text}")

    # Test articles endpoint
    print("\n📰 Testing articles endpoint...")
    response = client.get("/api/articles/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total articles: {data.get('total', 0)}")
        print(f"Items returned: {len(data.get('items', []))}")
        print(f"Current page: {data.get('page')}")
        print("✅ Articles endpoint working")
    else:
        print("❌ Articles endpoint failed")
        print(f"Error: {response.text}")

    # Test analytics dashboard
    print("\n📊 Testing analytics dashboard...")
    response = client.get("/api/analytics/dashboard")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total articles: {data.get('total_articles', 0)}")
        print(f"Recent articles: {data.get('recent_articles', 0)}")
        print(f"Analysis period: {data.get('analysis_period_days')} days")
        print("✅ Analytics dashboard working")
    else:
        print("❌ Analytics dashboard failed")
        print(f"Error: {response.text}")

    # Test NLP status
    print("\n🧠 Testing NLP analyzers status...")
    response = client.get("/api/nlp/analyzers/status")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"System Status: {data.get('system_status')}")
        sentiment_status = data.get("sentiment_analyzer", {}).get("status")
        topic_status = data.get("topic_classifier", {}).get("status")
        print(f"Sentiment Analyzer: {sentiment_status}")
        print(f"Topic Classifier: {topic_status}")
        print("✅ NLP analyzers working")
    else:
        print("❌ NLP analyzers failed")
        print(f"Error: {response.text}")

    print("\n" + "=" * 50)
    print("🎉 API testing completed!")


if __name__ == "__main__":
    test_basic_endpoints()
