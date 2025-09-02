# ANISA API Reference (Index)

This section will house the REST API documentation for ANISA.

Planned:
- Authentication & headers
- Cultural analysis endpoints
- Trade query endpoints
- Telemetry and status

For now, see `src/api.py` for the current FastAPI routes.


## PANX Integration (Preview)

- GET `/api/v1/tool/describe`
  - Returns a tool descriptor for PANX to discover ANISA functions:
  - Functions exposed: `query`, `analyze`, `event_assess`

- POST `/api/v1/panx/analyze`
  - Request: `{ text, language?, region_hint? }`
  - Response: `{ authenticity_score, detected_region, detected_variant, compliance_notes[], recommendations[] }`

- POST `/api/v1/panx/event/assess`
  - Request: `{ event_type, region, trade_context, evidence? }`
  - Response: `{ recommended_validators[], minimum_consensus, cultural_risks[], compliance_notes[], region, variant }`

