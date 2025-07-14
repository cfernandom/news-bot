#!/usr/bin/env python3
"""
Script to restore backed-up sources to the fresh database using API endpoints.
This validates the complete manual source creation workflow.
"""

import json
import requests
import sys
from datetime import datetime

API_BASE = "http://localhost:8000"

def get_auth_token():
    """Get authentication token for API access"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/auth/login", json=login_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def restore_source(source_data, auth_token):
    """Restore a single source using the API"""
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    # Prepare source data for API (remove id and timestamps)
    api_data = {
        "name": source_data["name"],
        "base_url": source_data["base_url"],
        "language": source_data["language"],
        "country": source_data["country"],
        "extractor_class": source_data["extractor_class"] or "",
        "is_active": source_data["is_active"],
        "validation_status": "pending",  # Will be validated after creation
        "robots_txt_url": source_data.get("robots_txt_url"),
        "crawl_delay_seconds": source_data.get("crawl_delay_seconds", 2.0),
        "terms_of_service_url": source_data.get("terms_of_service_url"),
        "legal_contact_email": source_data.get("legal_contact_email"),
        "fair_use_basis": source_data.get("fair_use_basis"),
        "compliance_score": source_data.get("compliance_score", 0.0),
        "data_retention_days": 365,
        "max_articles_per_run": 50,
        "content_type": "metadata_only",
        "source_type": "news_site",
        "status": "active"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/sources", json=api_data, headers=headers)
        if response.status_code == 201:
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
    
    # Get authentication token
    auth_token = get_auth_token()
    if not auth_token:
        print("❌ Authentication failed. Cannot proceed.")
        sys.exit(1)
    
    print("🔐 Authentication successful")
    
    # Restore each source
    created_sources = []
    failed_sources = []
    
    for source in sources:
        result = restore_source(source, auth_token)
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
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{API_BASE}/api/sources", headers=headers)
        if response.status_code == 200:
            total_sources = len(response.json())
            print(f"📈 Total sources in database: {total_sources}")
        else:
            print(f"❌ Could not verify total count: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verifying count: {e}")
    
    print(f"\n🎯 Fresh database test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()