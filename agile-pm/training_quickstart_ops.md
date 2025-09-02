# ANISA Training Quickstart (Ops)

## Environment
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-training.txt
```

## One-command
```bash
bash scripts/quick_train.sh
```
Artifacts:
- Models: `./models/anisa-quick-start`
- Data: `training_data/raw/`

## Notes
- Seed data is minimal; add more in `src/training/data/data_collector.py`.
- Adjust epochs/batch sizes in `src/training/automl/huggingface_training.py`.
