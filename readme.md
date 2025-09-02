# ANISA: Authentic Native Intelligence Systematically Applied

Cultural Intelligence Engine for the GTCX Ecosystem

Updated: 2025-09-02

[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GTCX Ecosystem](https://img.shields.io/badge/GTCX-Ecosystem-green.svg)](https://github.com/gtcx-protocol-ecosystem)

---

## Executive summary
ANISA provides practical cultural intelligence for GTCX services. It exposes APIs that PANX uses to enrich event verification with accurate regional/variant context, authenticity signals, and compliance notes. We optimize for correctness, transparency, and safe defaults.

---

## GTCX integration (current)
- PANX tool surface: `GET /api/v1/tool/describe`
- PANX analyze: `POST /api/v1/panx/analyze`
- PANX assess event: `POST /api/v1/panx/event/assess`

Guides:
- `agile-pm/user_guide.md`
- `agile-pm/agent_guide.md`
- `agile-pm/runbook.md`
- `agile-pm/deploy_gcp_vm.md`
- `agile-pm/training_quickstart_ops.md`

---

## Architecture (high level)
```
ANISA Core
├─ Cultural Authentication (region, variant, trade context)
├─ Native Language Processing (insights, implications, notes)
└─ Intelligence Service (structured guidance for PANX/Cortex)
```

---

## Getting started
### Run API (local example)
```bash
pip install -r requirements.txt
PYTHONPATH=src ANISA_API_KEY=<key> uvicorn src.api:app --host 0.0.0.0 --port 8000
```

### Training quick start
```bash
pip install -r requirements-training.txt
bash scripts/quick_train.sh
```
Artifacts: `models/anisa-quick-start`; seed data in `training_data/raw/`.

---

## Documentation
- Product vision: `docs/product_vision.md`
- User journeys: `docs/user_journeys.md`
- GTCX integration: `docs/gtcx_integration.md`
- Agile-PM guides: see `agile-pm/`
- Changelog: `CHANGELOG.md`

---

## Roadmap (as of 2025‑09‑02)
- Delivered
  - PANX tool descriptor and assess/analyze endpoints
  - PANX/Cortex mock E2E with schemas and contract checks
  - VM deploy guides and runbooks
- In progress (Q3 2025)
  - Input/response schema hardening and versioned headers
  - Telemetry hooks and basic observability
- Planned (Q4 2025)
  - Region/variant coverage expansion with curated data
  - Packaging improvements and deployment profiles

Dates are targets, subject to change based on validation and data availability.

---

## License
MIT — see `LICENSE`.

## Support
- Issues: GitHub Issues (repo)
- Discussions: GitHub Discussions (repo)
- Email: anisa@gtcx.org