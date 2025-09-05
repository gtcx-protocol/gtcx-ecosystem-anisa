# ANISA Changelog

## [0.1.0] - 2025-09-02
### Added
- GTCX-focused docs overhaul: `readme.md`, `docs/README.md`, `product_vision.md`, `user_journeys.md`, `gtcx_integration.md`, training docs, and project structure doc.
- GTCX models and API endpoints:
  - `GET /api/v1/tool/describe`
  - `POST /api/v1/panx/analyze`
  - `POST /api/v1/panx/event/assess`
- API key auth, response headers, and telemetry hooks.
- Training quick start (HF pipeline), `requirements-training.txt`, `scripts/quick_train.sh`.

### Changed
- Core services and models updated for GTCX trade contexts and compliance levels.

### Fixed
- Import issues, naming conflicts, and header handling in API responses.

[0.1.0]: https://github.com/gtcx-protocol/gtcx-ecosystem-anisa

