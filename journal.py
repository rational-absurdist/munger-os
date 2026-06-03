"""journal.py — CSV persistence layer for Munger OS."""

from __future__ import annotations

from datetime import datetime, date
from pathlib import Path
from typing import Dict

import pandas as pd

DATA_DIR = Path("data")
REFLECTIONS_FILE = DATA_DIR / "reflections.csv"
DECISIONS_FILE = DATA_DIR / "decisions.csv"
REVIEWS_FILE = DATA_DIR / "reviews.csv"


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def load_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    ensure_data_dir()
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=columns)


def save_reflection(model_name: str, theme: str, reflection: str, action: str) -> None:
    df = load_reflections()
    row = {
        "date": str(date.today()),
        "model": model_name,
        "theme": theme,
        "reflection": reflection,
        "action": action,
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
    }
    pd.concat([df, pd.DataFrame([row])], ignore_index=True).to_csv(REFLECTIONS_FILE, index=False)


def load_reflections() -> pd.DataFrame:
    return load_csv(REFLECTIONS_FILE, ["date", "model", "theme", "reflection", "action", "timestamp"])


def save_decision(row: Dict[str, object]) -> None:
    df = load_decisions()
    pd.concat([df, pd.DataFrame([row])], ignore_index=True).to_csv(DECISIONS_FILE, index=False)


def load_decisions() -> pd.DataFrame:
    return load_csv(
        DECISIONS_FILE,
        [
            "date", "decision", "domain", "primary_model", "expected_outcome", "risks",
            "opportunity_cost", "incentives", "disconfirming_evidence", "confidence",
            "downside", "score", "grade", "revisit_date", "timestamp",
        ],
    )


def save_review(row: Dict[str, object]) -> None:
    df = load_reviews()
    pd.concat([df, pd.DataFrame([row])], ignore_index=True).to_csv(REVIEWS_FILE, index=False)


def load_reviews() -> pd.DataFrame:
    return load_csv(REVIEWS_FILE, ["date", "decision", "actual_outcome", "lesson", "timestamp"])
