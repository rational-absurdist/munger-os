"""
model.py — Decision-quality scoring engine for Munger OS v2.

Produces a structured pre-mortem score: how well a decision has been examined
using Munger-style mental models. Not truth — process quality.
"""

from __future__ import annotations

from typing import Dict, List

from data import DECISION_CRITERIA, BIAS_TAXONOMY


def calculate_decision_score(
    criteria_checked: Dict[str, bool],
    confidence: int,
    downside: int,
    reversibility: int = 50,
    magnitude: int = 50,
) -> Dict[str, object]:
    """Return score, grade, and interpretation for a decision entry.

    reversibility: 0 = permanent, 100 = fully reversible in 6 months.
    magnitude:     0 = minor, 100 = career or life-defining.
    """
    raw_score = 0
    max_score = sum(item["weight"] for item in DECISION_CRITERIA)

    missing: List[str] = []
    for item in DECISION_CRITERIA:
        if criteria_checked.get(item["key"], False):
            raw_score += item["weight"]
        else:
            missing.append(item["label"])

    score = round(100 * raw_score / max_score, 1)
    risk_warning = ""

    # High-magnitude, irreversible decisions require a higher bar.
    if magnitude >= 70 and reversibility <= 30 and score < 85:
        score = max(score - 12, 0)
        risk_warning = (
            "High-magnitude + irreversible + incomplete review. "
            "This is where permanent mistakes are made. Do not proceed."
        )
    elif confidence >= 80 and downside >= 70 and score < 80:
        score = max(score - 8, 0)
        risk_warning = (
            "High confidence + high downside + incomplete review. "
            "This is where people usually get hurt."
        )
    elif magnitude >= 70 and score < 70:
        risk_warning = (
            "High-magnitude decision with a weak review process. "
            "Raise the bar before committing."
        )

    if score >= 85:
        grade = "Strong review"
        interpretation = (
            "The decision has been reviewed through multiple lenses. "
            "Not guaranteed to be right, but the process is defensible."
        )
    elif score >= 70:
        grade = "Adequate review"
        interpretation = (
            "Reasonable process, but predictable blind spots remain. "
            "Push harder on the missing items before committing."
        )
    elif score >= 50:
        grade = "Weak review"
        interpretation = (
            "The decision may be right, but the reasoning process is underdeveloped. "
            "You are not ready to decide. Slow down."
        )
    else:
        grade = "Poor review"
        interpretation = (
            "This is mostly impulse, narrative, or incomplete analysis. "
            "Do not confuse movement with judgment. Stop and think."
        )

    return {
        "score": score,
        "grade": grade,
        "interpretation": interpretation,
        "missing": missing,
        "risk_warning": risk_warning,
    }


def detect_bias_flags(text: str) -> List[Dict[str, str]]:
    """Keyword-based bias detector. Simple, transparent, and intentionally limited."""
    text_lower = text.lower()
    flags = []

    rules = {
        "Confirmation bias":     ["i know", "obvious", "clearly", "no doubt", "everyone knows"],
        "Availability bias":     ["recently", "last time", "i just saw", "after what happened"],
        "Authority bias":        ["expert said", "famous", "ceo", "professor", "authority"],
        "Social proof":          ["everyone", "market says", "popular", "trending", "most people"],
        "Commitment bias":       ["already invested", "too late", "can't quit", "sunk", "we started"],
        "Overconfidence":        ["guaranteed", "can't lose", "sure thing", "100%", "certain"],
        "Incentive-caused bias": ["bonus", "commission", "promotion", "fee", "quota"],
        "Loss aversion":         ["can't afford to lose", "recover", "make it back", "avoid losing"],
        "Narrative fallacy":     ["destined", "meant to be", "story", "inevitable"],
        "Recency bias":          ["right now", "these days", "current trend", "latest"],
        "Deprival superreaction":["can't give up", "worked too hard", "already mine", "taken away", "walk away from"],
        "Envy and jealousy":     ["not fair", "why do they", "they don't deserve", "why not me", "better than me without"],
        "Contrast miscognition": ["compared to the last", "not as bad as", "at least it's better than", "previous was worse"],
        "Liking/disliking bias": ["trust them completely", "they would never", "great person so", "they're the worst"],
        "Twaddle tendency":      ["basically good", "kind of makes sense", "essentially just", "sort of obvious"],
    }

    for bias, keywords in rules.items():
        if any(k in text_lower for k in keywords):
            flags.append({"bias": bias, "description": BIAS_TAXONOMY[bias]})

    return flags
