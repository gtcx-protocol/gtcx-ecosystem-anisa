# ANISA Agent Integration Guide

## Purpose
Guidance for PANX and other services integrating with ANISA for cultural intelligence.

## Endpoints
- GET `/api/v1/tool/describe` — tool descriptor for PANX
- POST `/api/v1/panx/analyze` — text analysis with region/language hints
- POST `/api/v1/panx/event/assess` — event assessment returning cultural/compliance notes

## Auth
- Header: `X-API-Key: <ANISA_API_KEY>`

## Retries & Timeouts
- Use backoff on 5xx and network errors; treat 429 as soft-fail.

## Example (pseudo)
```python
headers = {"Content-Type": "application/json", "X-API-Key": ANISA_API_KEY}
req = {"event_type":"export_permit_issued","region":"west_africa","trade_context":"compliance","evidence":{}}
resp = http.post(f"{ANISA_BASE}/api/v1/panx/event/assess", json=req, headers=headers)
if resp.ok:
  data = resp.json()
  # fields: compliance_notes, cultural_risks, variant, region
```
