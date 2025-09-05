# Deploy ANISA on GCP VM (quick)

## VM
- Ubuntu 22.04, e2-medium; allow HTTP/HTTPS.
- Install Python 3.11+, git.

## Setup
```bash
sudo apt-get update -y && sudo apt-get install -y python3-pip git python3-venv
cd /opt && sudo mkdir -p anisa && sudo chown $USER:$USER anisa
cd /opt/anisa
git clone https://github.com/gtcx-protocol/gtcx-ecosystem-anisa.git .
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-training.txt || true
pip install -r requirements.txt || true
```

## Run API (example)
```bash
export PYTHONPATH=src
export ANISA_API_KEY=<your-key>
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

## Verify
```bash
curl -s -H "X-API-Key: $ANISA_API_KEY" http://<VM_IP>:8000/api/v1/tool/describe
```

