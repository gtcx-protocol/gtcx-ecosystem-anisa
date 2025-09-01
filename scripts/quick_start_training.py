#!/usr/bin/env python3
import asyncio
import json
import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))


async def main() -> None:
    from training.data.data_collector import CulturalDataCollector
    from training.automl.huggingface_training import HFCulturalTrainer, HFConfig

    print("\n🚀 ANISA Quick-Start Training\n")

    # 1) Collect seed data
    collector = CulturalDataCollector()
    examples = collector.collect_initial_training_data()

    # Save for reproducibility
    out_path = collector.save_training_data(examples, filename="quick_start_data")
    print(f"Saved seed data to: {out_path}")

    # Prepare minimal list for trainer
    train_items = [
        {"text": e.text, "cultural_context": e.cultural_context} for e in examples
    ]

    # 2) Train a tiny HF model (CPU-friendly)
    cfg = HFConfig()
    trainer = HFCulturalTrainer(cfg)
    dataset = trainer.prepare_dataset(train_items)
    eval_res = trainer.train(dataset)
    print("\n📈 Evaluation:")
    for k, v in eval_res.items():
        print(f"  {k}: {v}")

    print(f"\n✅ Model artifacts in: {cfg.output_dir}")


if __name__ == "__main__":
    asyncio.run(main())


