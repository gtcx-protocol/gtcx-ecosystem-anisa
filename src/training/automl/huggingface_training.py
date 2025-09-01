#!/usr/bin/env python3
"""
ANISA Hugging Face Training (minimal quick-start)
"""

import logging
from dataclasses import dataclass
from typing import Dict, Any, List

try:
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        TrainingArguments,
        Trainer,
        DataCollatorWithPadding,
    )
    from datasets import Dataset, DatasetDict
    import evaluate
    import torch
    HF_AVAILABLE = True
except Exception:  # pragma: no cover
    HF_AVAILABLE = False


logger = logging.getLogger(__name__)


@dataclass
class HFConfig:
    model_name: str = "distilbert-base-uncased"  # lightweight for local quick start
    num_labels: int = 7
    max_length: int = 256
    learning_rate: float = 2e-5
    batch_size: int = 8
    num_epochs: int = 1  # keep very low for quick start
    output_dir: str = "./models/anisa-quick-start"


class HFCulturalTrainer:
    def __init__(self, config: HFConfig):
        if not HF_AVAILABLE:
            raise ImportError(
                "Transformers + Datasets not available. Install: pip install 'transformers==4.*' 'datasets==2.*' scikit-learn torch"
            )

        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.model_name,
            num_labels=config.num_labels,
        )

        self.label_map = {
            "ubuntu": 0,
            "guanxi": 1,
            "jugaad": 2,
            "jeitinho": 3,
            "wasta": 4,
            "individualism": 5,
            "collectivism": 6,
        }
        self.inv_label_map = {v: k for k, v in self.label_map.items()}

    def prepare_dataset(self, examples: List[Dict[str, Any]]) -> DatasetDict:
        # map labels
        data = [
            {
                "text": ex["text"],
                "label": self.label_map[ex["cultural_context"]],
            }
            for ex in examples
            if ex.get("text") and ex.get("cultural_context") in self.label_map
        ]

        full_ds = Dataset.from_list(data)
        split = full_ds.train_test_split(test_size=0.3, seed=42)

        def tokenize(batch):
            return self.tokenizer(
                batch["text"],
                truncation=True,
                padding=True,
                max_length=self.config.max_length,
            )

        train_ds = split["train"].map(tokenize, batched=True)
        val_ds = split["test"].map(tokenize, batched=True)

        return DatasetDict(train=train_ds, validation=val_ds)

    def _compute_metrics(self, eval_pred):
        logits, labels = eval_pred
        preds = logits.argmax(axis=-1)
        metric = evaluate.load("accuracy")
        return metric.compute(predictions=preds, references=labels)

    def train(self, dataset: DatasetDict) -> Dict[str, Any]:
        import torch
        from torch.utils.data import DataLoader
        from torch.optim import AdamW

        device = torch.device("cpu")
        self.model.to(device)

        # set torch format
        columns = ["input_ids", "attention_mask", "label"]
        train_ds = dataset["train"].remove_columns([c for c in dataset["train"].column_names if c not in columns])
        val_ds = dataset["validation"].remove_columns([c for c in dataset["validation"].column_names if c not in columns])
        train_ds.set_format(type="torch")
        val_ds.set_format(type="torch")

        collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        train_loader = DataLoader(train_ds, batch_size=self.config.batch_size, shuffle=True, collate_fn=collator)
        val_loader = DataLoader(val_ds, batch_size=self.config.batch_size, shuffle=False, collate_fn=collator)

        optimizer = AdamW(self.model.parameters(), lr=self.config.learning_rate)
        self.model.train()
        for _ in range(self.config.num_epochs):
            for batch in train_loader:
                batch = {k: v.to(device) for k, v in batch.items()}
                outputs = self.model(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"], labels=batch["labels"]) if "labels" in batch else self.model(**batch)
                loss = outputs.loss
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        # evaluation
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in val_loader:
                batch = {k: v.to(device) for k, v in batch.items()}
                outputs = self.model(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"], labels=batch["labels"]) if "labels" in batch else self.model(**batch)
                logits = outputs.logits
                preds = torch.argmax(logits, dim=-1)
                correct += (preds == batch["labels"]).sum().item()
                total += batch["labels"].numel()

        accuracy = (correct / total) if total > 0 else 0.0
        return {"accuracy": accuracy}


