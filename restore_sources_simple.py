#!/usr/bin/env python3
"""
Script to restore backed-up sources using the legacy API endpoint.
This validates the complete manual source creation workflow.
"""

import json
import requests
import sys
from datetime import datetime

API_BASE = "http://localhost:8000"

def restore_source(source_data):
    """Restore a single source using the legacy API"""
    
    # Prepare source data for API (remove id and timestamps)
    api_data = {
        "name": source_data["name"],
        "base_url": source_data["base_url"],
        "language": source_data["language"],
        "country": source_data["country"],
        "extractor_class": source_data["extractor_class"] or "",
        "is_active": source_data["is_active"],
        "validation_status": "pending"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/v1/sources", json=api_data)
        if response.status_code == 201:
            created_source = response.json()
            print(f"✅ Created: {source_data['name']} (ID: {created_source['id']})")
            return created_source
        elif response.status_code == 200:
            created_source = response.json()
            print(f"✅ Created: {source_data['name']} (ID: {created_source['id']})")
            return created_source
        else:
            print(f"❌ Failed to create {source_data['name']}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating {source_data['name']}: {e}")
        return None

def main():
    print("🔄 Starting source restoration process...")
    
    # Load backed-up sources
    try:
        with open("sources_backup.json", "r") as f:
            sources = json.load(f)
        print(f"📄 Loaded {len(sources)} sources from backup")
    except Exception as e:
        print(f"❌ Error loading backup file: {e}")
        sys.exit(1)
    
    # Test API connectivity
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("🔐 API connectivity confirmed")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ API connection error: {e}")
        sys.exit(1)
    
    # Check current sources count
    try:
        response = requests.get(f"{API_BASE}/api/v1/sources")
        if response.status_code == 200:
            current_sources = response.json()
            print(f"📊 Current sources in database: {len(current_sources)}")
        else:
            print(f"❌ Could not fetch current sources: {response.status_code}")
    except Exception as e:
        print(f"❌ Error fetching current sources: {e}")
    
    # Restore each source
    created_sources = []
    failed_sources = []
    
    for source in sources:
        result = restore_source(source)
        if result:
            created_sources.append(result)
        else:
            failed_sources.append(source["name"])
    
    # Summary
    print(f"\n📊 RESTORATION SUMMARY")
    print(f"✅ Successfully created: {len(created_sources)} sources")
    print(f"❌ Failed: {len(failed_sources)} sources")
    
    if failed_sources:
        print(f"\n🔴 Failed sources: {', '.join(failed_sources)}")
    
    # Verify total count
    try:
        response = requests.get(f"{API_BASE}/api/v1/sources")
        if response.status_code == 200:
            total_sources = len(response.json())
            print(f"📈 Total sources in database after restoration: {total_sources}")
        else:
            print(f"❌ Could not verify total count: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verifying count: {e}")
    
    print(f"\n🎯 Fresh database test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()