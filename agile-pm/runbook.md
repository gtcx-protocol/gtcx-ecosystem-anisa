# ANISA Runbook (Operations)

## Start / Stop
```bash
# API via uvicorn (example)
PYTHONPATH=src ANISA_API_KEY=<key> uvicorn src.api:app --host 0.0.0.0 --port 8000
```

## Logs & Health
- Health: `GET /health` (if enabled) or hit any known endpoint with `X-API-Key`.

## Rotate API Key
- Update deployment env `ANISA_API_KEY` and restart the process.

## Troubleshooting
- Import errors: ensure `PYTHONPATH=src` and correct absolute imports.
- 401 responses: verify `X-API-Key` header value.

