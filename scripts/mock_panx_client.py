#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path
import requests

BASE = os.environ.get("ANISA_BASE_URL", "http://localhost:8000")
API_KEY = os.environ.get("ANISA_API_KEY", "test-key")

def get(url: str):
    r = requests.get(url, headers={"X-API-Key": API_KEY})
    r.raise_for_status()
    return r.json()

def post(url: str, payload: dict):
    r = requests.post(url, headers={"X-API-Key": API_KEY, "Content-Type": "application/json"}, data=json.dumps(payload))
    r.raise_for_status()
    return r.json()

def main():
    print("Describe tool:")
    print(json.dumps(get(f"{BASE}/api/v1/tool/describe"), indent=2))

    print("\nPANX analyze:")
    analyze = post(f"{BASE}/api/v1/panx/analyze", {"text": "Community first cooperation for mining approvals", "language": "en"})
    print(json.dumps(analyze, indent=2))

    print("\nPANX event assess:")
    sample_path = Path(__file__).resolve().parents[1] / "examples" / "panx" / "sample_event.json"
    with open(sample_path, "r", encoding="utf-8") as fh:
        evt = json.load(fh)
    assess = post(f"{BASE}/api/v1/panx/event/assess", evt)
    print(json.dumps(assess, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


