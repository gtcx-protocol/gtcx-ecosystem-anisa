# ANISA — v1 Build Plan and Phase 2 Expansion

## v1 (delivered in this milestone)
- GTCX-focused models and endpoints: `/api/v1/tool/describe`, `/api/v1/panx/analyze`, `/api/v1/panx/event/assess`
- API key authentication, response headers, and basic telemetry hooks
- Training quick start (HF pipeline) and docs overhaul aligned to GTCX

## Definition of Done (v1)
- Endpoints documented and callable by PANX mock
- Cultural context models cover regions, variants, trade contexts, compliance levels
- Demos and README updated; basic telemetry emitted

---

## Phase 2 (Q1 2026) Expansion

### Security & Reliability
- API key scopes and rotation; per-route rate limits
- Idempotency for PANX calls; standardized error classes and codes
- Retry/backoff with circuit breaker for outbound integrations

### Contracts & Validation
- Versioned request/response models with contract headers
- JSON Schemas generated and published; compatibility test suite
- OpenAPI refined with examples and error schemas

### Cultural Intelligence Engine
- Expand cultural markers and compliance factors per region/variant
- Plug-in strategy for cultural evaluators; confidence calibration
- Community-verified inputs: hooks for lightweight attestations

### Integrations
- Harden PANX tool descriptor and analysis endpoints
- Add Veritas telemetry sinks; standardized event shapes
- Prepare Cortex-friendly enrichment outputs

### Training & Data
- Data pipeline for curated cultural datasets (quality gates)
- Active learning loop: sample selection, human-in-the-loop labeling
- Model packaging and versioning; inference performance budget

### Ops & Delivery
- Docker Compose for ANISA + mocks; healthchecks and envs
- CI smoke: start API, run contract tests, publish artifacts
- Observability: structured logs, metrics, trace stubs

---

## References
- GTCX Integration: `docs/gtcx_integration.md`
- Training: `docs/training_quick_start.md`, `docs/ai_training_framework.md`
- Product Vision: `docs/product_vision.md`
