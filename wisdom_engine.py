"""wisdom_engine.py — Daily model selection and prompt generation."""

from __future__ import annotations

from datetime import date
import random

from data import MENTAL_MODELS, DAILY_THEMES, MentalModel


def get_daily_model() -> MentalModel:
    seed = int(date.today().strftime("%Y%m%d"))
    rng = random.Random(seed)
    return rng.choice(MENTAL_MODELS)


def get_daily_theme() -> str:
    seed = int(date.today().strftime("%Y%m%d")) + 17
    rng = random.Random(seed)
    return rng.choice(DAILY_THEMES)


def generate_inversion_prompt(decision: str) -> str:
    clean = decision.strip() or "this decision"
    return f"Assume '{clean}' fails badly. What were the three most likely causes?"
