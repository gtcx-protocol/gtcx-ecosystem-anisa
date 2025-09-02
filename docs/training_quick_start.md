# Training Quick Start

## Prerequisites
- Python 3.13
- macOS ARM64 supported (CPU is fine)

```
pip install -r requirements-training.txt
```

## Run
```
bash scripts/quick_train.sh
```
This will:
- Collect seed cultural examples
- Train a small DistilBERT classifier
- Print validation accuracy
- Save model to `./models/anisa-quick-start`

## Improve accuracy
- Add labeled examples in `src/training/data/data_collector.py`
- Re-run `bash scripts/quick_train.sh`

## Notes
- Dependencies pinned for Python 3.13 + macOS ARM compatibility
- No GPU required for seed set

