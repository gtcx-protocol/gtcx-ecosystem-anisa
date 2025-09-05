#!/usr/bin/env python3
"""
ANISA Training Data Collector

Collects seed cultural training examples for quick-start fine-tuning.
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List


logger = logging.getLogger(__name__)


@dataclass
class CulturalTrainingExample:
    text: str
    cultural_context: str
    region: str
    trade_context: str
    source: str
    created_at: str


class CulturalDataCollector:
    def __init__(self, data_dir: str = "training_data"):
        self.data_dir = Path(data_dir)
        (self.data_dir / "raw").mkdir(parents=True, exist_ok=True)

    def collect_initial_training_data(self) -> List[CulturalTrainingExample]:
        now = datetime.utcnow().isoformat()
        examples: List[CulturalTrainingExample] = [
            # Ubuntu (West Africa)
            CulturalTrainingExample(
                text="We need to consult with the community before making any decisions about mining operations.",
                cultural_context="ubuntu",
                region="west_africa",
                trade_context="mining",
                source="seed_example",
                created_at=now,
            ),
            CulturalTrainingExample(
                text="Benefits should be shared with the entire community, not just a few individuals.",
                cultural_context="ubuntu",
                region="west_africa",
                trade_context="benefit_sharing",
                source="seed_example",
                created_at=now,
            ),
            # Guanxi (East Asia)
            CulturalTrainingExample(
                text="Let's build relationships first before discussing business terms.",
                cultural_context="guanxi",
                region="east_asia",
                trade_context="trade",
                source="seed_example",
                created_at=now,
            ),
            CulturalTrainingExample(
                text="Preserve face and maintain honor in all negotiations.",
                cultural_context="guanxi",
                region="east_asia",
                trade_context="negotiation",
                source="seed_example",
                created_at=now,
            ),
            # Jugaad (South Asia)
            CulturalTrainingExample(
                text="We can find a creative solution with limited resources.",
                cultural_context="jugaad",
                region="south_asia",
                trade_context="innovation",
                source="seed_example",
                created_at=now,
            ),
            # Jeitinho (Latin America)
            CulturalTrainingExample(
                text="We need to find a flexible way around this bureaucratic obstacle.",
                cultural_context="jeitinho",
                region="latin_america",
                trade_context="bureaucracy",
                source="seed_example",
                created_at=now,
            ),
            # Wasta (Middle East)
            CulturalTrainingExample(
                text="Use trusted relationships to facilitate approvals respectfully.",
                cultural_context="wasta",
                region="middle_east",
                trade_context="approval",
                source="seed_example",
                created_at=now,
            ),
            # Individualism (North America)
            CulturalTrainingExample(
                text="I'll take responsibility and proceed independently.",
                cultural_context="individualism",
                region="north_america",
                trade_context="decision_making",
                source="seed_example",
                created_at=now,
            ),
            # Collectivism (Europe)
            CulturalTrainingExample(
                text="We should reach group consensus before proceeding.",
                cultural_context="collectivism",
                region="europe",
                trade_context="decision_making",
                source="seed_example",
                created_at=now,
            ),
        ]
        return examples

    def save_training_data(self, examples: List[CulturalTrainingExample], filename: str = "initial_training_data") -> Path:
        out_path = self.data_dir / "raw" / f"{filename}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in examples], f, ensure_ascii=False, indent=2)
        logger.info("Saved %d examples to %s", len(examples), out_path)
        return out_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    collector = CulturalDataCollector()
    data = collector.collect_initial_training_data()
    collector.save_training_data(data)




