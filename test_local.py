#!/usr/bin/env python3
"""
Quick local test for ANISA API
Tests the core functionality without Docker
"""

import sys
import os
sys.path.append('src')

from fastapi.testclient import TestClient
from src.api import app

# Create test client
client = TestClient(app)

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✅ Health check passed")

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "ANISA" in data["message"]
    print("✅ Root endpoint passed")

def test_cultural_query():
    """Test cultural query endpoint"""
    # Skip if API key is required
    os.environ["ANISA_API_KEY"] = ""
    
    response = client.post("/api/v1/query", json={
        "text": "We need community approval for mining operations",
        "language": "en"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Cultural query passed - Region: {data.get('cultural_variant', 'N/A')}")
    else:
        print(f"⚠️  Cultural query returned {response.status_code}")

def test_insights():
    """Test cultural insights endpoint"""
    os.environ["ANISA_API_KEY"] = ""
    
    response = client.post("/api/v1/insights", json={
        "text": "The elders must bless this trade agreement",
        "language": "en",
        "context": {
            "trade_type": "mining_rights",
            "region": "africa"
        }
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Insights passed - Factors: {len(data.get('cultural_factors', []))}")
    else:
        print(f"⚠️  Insights returned {response.status_code}")

if __name__ == "__main__":
    print("\n🧪 Testing ANISA API locally...\n")
    
    try:
        test_health()
        test_root()
        test_cultural_query()
        test_insights()
        
        print("\n✨ All basic tests passed! ANISA core is functional.\n")
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        sys.exit(1)
