#!/usr/bin/env python3
"""
ANISA API Startup Script
Simple script to start the ANISA API server.
"""

import uvicorn
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    print("🚀 Starting ANISA API Server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Alternative docs at: http://localhost:8000/redoc")
    print("🌐 API base URL: http://localhost:8000")
    print("=" * 60)
    
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
