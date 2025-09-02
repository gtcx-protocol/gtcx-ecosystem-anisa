# ANISA User Guide

## Overview
ANISA provides cultural intelligence for the GTCX ecosystem. It enriches trade flows with cultural context, authenticity scoring, and compliance notes.

## Base URL
- Example: `https://anisa.yourdomain` (replace with your deployment)

## Health
```
GET /health
```

## PANX Tool Describe
```
GET /api/v1/tool/describe
Headers: X-API-Key: <ANISA_API_KEY>
```

## PANX Analyze
```
POST /api/v1/panx/analyze
Headers: X-API-Key: <ANISA_API_KEY>
Body:
{
  "text": "local customs require community consultation",
  "language": "en",
  "region_hint": "west_africa"
}
```

## PANX Event Assess
```
POST /api/v1/panx/event/assess
Headers: X-API-Key: <ANISA_API_KEY>
Body:
{
  "event_type": "export_permit_issued",
  "region": "west_africa",
  "trade_context": "compliance",
  "evidence": {"permit_document": "hash:abc123"}
}
```

## Notes
- Obtain the ANISA API key from your deployment operator.
- Responses include authenticity and cultural/compliance notes suited for PANX/Cortex enrichment.
