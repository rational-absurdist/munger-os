"""
model.py — Decision-quality scoring engine for Munger OS.

This does not pretend to produce objective truth. It produces a structured
pre-mortem score: how well a decision has been examined using Munger-style
mental models.
"""

from __future__ import annotations

from typing import Dict, List

from data import DECISION_CRITERIA, BIAS_TAXONOMY


def calculate_decision_score(criteria_checked: Dict[str, bool], confidence: int, downside: int) -> Dict[str, object]:
    """Return score, grade, and interpretation for a decision entry."""
    raw_score = 0
    max_score = sum(item["weight"] for item in DECISION_CRITERIA)

    missing: List[str] = []
    for item in DECISION_CRITERIA:
        if criteria_checked.get(item["key"], False):
            raw_score += item["weight"]
        else:
            missing.append(item["label"])

    score = round(100 * raw_score / max_score, 1)

    # Penalize high confidence paired with high downside and incomplete review.
    risk_warning = ""
    if confidence >= 80 and downside >= 70 and score < 80:
        score = max(score - 8, 0)
        risk_warning = "High confidence + high downside + incomplete review. This is where people usually get hurt."

    if score >= 85:
        grade = "Strong review"
        interpretation = "The decision has been reviewed through multiple lenses. Still not guaranteed, but the process is defensible."
    elif score >= 70:
        grade = "Adequate review"
        interpretation = "Reasonable process, but several predictable blind spots remain."
    elif score >= 50:
        grade = "Weak review"
        interpretation = "The decision may be right, but the reasoning process is underdeveloped. Slow down."
    else:
        grade = "Poor review"
        interpretation = "This is mostly impulse, narrative, or incomplete analysis. Do not confuse movement with judgment."

    return {
        "score": score,
        "grade": grade,
        "interpretation": interpretation,
        "missing": missing,
        "risk_warning": risk_warning,
    }


def detect_bias_flags(text: str) -> List[Dict[str, str]]:
    """Lightweight keyword-based bias detector. Simple by design and transparent."""
    text_lower = text.lower()
    flags = []

    rules = {
        "Confirmation bias": ["i know", "obvious", "clearly", "no doubt", "everyone knows"],
        "Availability bias": ["recently", "last time", "i just saw", "after what happened"],
        "Authority bias": ["expert said", "famous", "ceo", "professor", "authority"],
        "Social proof": ["everyone", "market says", "popular", "trending", "most people"],
        "Commitment bias": ["already invested", "too late", "can't quit", "sunk", "we started"],
        "Overconfidence": ["guaranteed", "can't lose", "sure thing", "100%", "certain"],
        "Incentive-caused bias": ["bonus", "commission", "promotion", "fee", "quota"],
        "Loss aversion": ["can't afford to lose", "recover", "make it back", "avoid losing"],
        "Narrative fallacy": ["destined", "meant to be", "story", "inevitable"],
        "Recency bias": ["right now", "these days", "current trend", "latest"],
    }

    for bias, keywords in rules.items():
        if any(k in text_lower for k in keywords):
            flags.append({"bias": bias, "description": BIAS_TAXONOMY[bias]})

    return flags
