"""
data.py — Reference data for Munger OS.

This module is the single source of truth for the app's mental models,
daily prompts, decision-quality criteria, and bias taxonomy.

The app is inspired by Charlie Munger's multidisciplinary approach, but it
uses original explanations and paraphrased principles rather than quote dumps.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class MentalModel:
    name: str
    category: str
    principle: str
    explanation: str
    question: str
    action: str
    decision_use: str


MENTAL_MODELS: List[MentalModel] = [
    MentalModel(
        name="Inversion",
        category="Decision Architecture",
        principle="Solve the problem backward.",
        explanation="Instead of asking how to succeed, identify what would reliably cause failure, then avoid those conditions.",
        question="What would make this fail?",
        action="List three ways this could go wrong and remove one today.",
        decision_use="Best for strategy, risk review, and avoiding self-inflicted damage.",
    ),
    MentalModel(
        name="Circle of Competence",
        category="Self-Knowledge",
        principle="Know the boundary of what you understand.",
        explanation="The advantage is not knowing everything. The advantage is knowing where your knowledge stops.",
        question="Where am I pretending to know more than I do?",
        action="Mark one assumption that needs outside expertise or more evidence.",
        decision_use="Best for investments, career moves, technical decisions, and delegation.",
    ),
    MentalModel(
        name="Incentives",
        category="Human Behavior",
        principle="Behavior follows incentives more often than intentions.",
        explanation="People and institutions usually respond to rewards, penalties, status, fear, and convenience.",
        question="What incentives are driving each party?",
        action="Identify one incentive that is misaligned with the desired outcome.",
        decision_use="Best for management, negotiations, organizations, contracts, and policy.",
    ),
    MentalModel(
        name="Opportunity Cost",
        category="Economics",
        principle="Every yes is a no to something else.",
        explanation="The true cost of a choice is the best alternative you gave up: time, attention, money, reputation, or optionality.",
        question="What am I giving up by choosing this?",
        action="Name the best alternative and decide whether this still wins.",
        decision_use="Best for prioritization, project selection, and personal finance.",
    ),
    MentalModel(
        name="Margin of Safety",
        category="Risk Management",
        principle="Leave room for error.",
        explanation="Good systems survive bad assumptions, delays, volatility, and ordinary human imperfection.",
        question="Where is the buffer too thin?",
        action="Add a time, money, review, redundancy, or fallback buffer.",
        decision_use="Best for planning, investing, engineering, operations, and health.",
    ),
    MentalModel(
        name="Second-Order Thinking",
        category="Systems Thinking",
        principle="Ask what happens after the first consequence.",
        explanation="The immediate effect is usually obvious. The delayed effect is where judgment begins.",
        question="What happens next, and then what?",
        action="Write one likely second-order consequence before acting.",
        decision_use="Best for policy, leadership, pricing, incentives, and life planning.",
    ),
    MentalModel(
        name="Probabilistic Thinking",
        category="Uncertainty",
        principle="Think in odds, not certainties.",
        explanation="Good judgment does not require certainty. It requires calibrated confidence and willingness to update.",
        question="What is the probability I am wrong?",
        action="Assign a confidence percentage and identify what would change it.",
        decision_use="Best for forecasting, investments, strategy, and uncertain outcomes.",
    ),
    MentalModel(
        name="Compounding",
        category="Long-Term Thinking",
        principle="Small advantages become decisive when repeated.",
        explanation="Knowledge, habits, capital, trust, reputation, and health compound when protected from interruption.",
        question="What behavior compounds if repeated?",
        action="Do one small action that benefits your future self.",
        decision_use="Best for learning, fitness, investing, and reputation.",
    ),
    MentalModel(
        name="Avoiding Stupidity",
        category="Practical Wisdom",
        principle="Avoid obvious mistakes before seeking brilliance.",
        explanation="Many good outcomes come from not doing dumb things: overleveraging, overcommitting, reacting emotionally, or ignoring incentives.",
        question="What is the dumbest preventable mistake here?",
        action="Build one guardrail against that mistake.",
        decision_use="Best for almost everything.",
    ),
    MentalModel(
        name="Lollapalooza Effect",
        category="Psychology",
        principle="Multiple forces can combine into extreme behavior.",
        explanation="Incentives, social proof, authority, scarcity, envy, and fear can reinforce each other and produce irrational outcomes.",
        question="Which forces are combining here?",
        action="List the psychological forces acting in the same direction.",
        decision_use="Best for bubbles, crowd behavior, marketing, politics, and organizational dysfunction.",
    ),
    MentalModel(
        name="Disconfirming Evidence",
        category="Epistemic Discipline",
        principle="Know what would prove you wrong.",
        explanation="A belief that cannot be tested or challenged becomes ideology, not judgment.",
        question="What evidence would change my mind?",
        action="Write one observable fact that would weaken your current view.",
        decision_use="Best for strategic planning, research, hiring, and investment theses.",
    ),
    MentalModel(
        name="Checklist Discipline",
        category="Execution",
        principle="Use checklists where errors are costly and predictable.",
        explanation="The goal is not bureaucracy. The goal is preventing known errors when attention fails.",
        question="What step should not be trusted to memory?",
        action="Turn one repeated risk into a checklist item.",
        decision_use="Best for operations, QA, finance, travel, health, and project delivery.",
    ),
]


BIAS_TAXONOMY: Dict[str, str] = {
    "Confirmation bias": "Searching for evidence that protects the current belief.",
    "Availability bias": "Overweighting vivid, recent, or emotionally memorable examples.",
    "Authority bias": "Treating status as evidence.",
    "Social proof": "Assuming the crowd has already done the thinking.",
    "Commitment bias": "Defending a past decision because identity or ego is attached.",
    "Overconfidence": "Mistaking intensity of belief for quality of evidence.",
    "Incentive-caused bias": "Reasoning bends toward what benefits the reasoner.",
    "Loss aversion": "Overweighting the pain of loss relative to equivalent gain.",
    "Narrative fallacy": "A clean story replacing messy reality.",
    "Recency bias": "Treating the recent past as the most likely future.",
}


DECISION_CRITERIA = [
    {"key": "inversion", "label": "Inverted failure modes", "weight": 12},
    {"key": "circle", "label": "Checked circle of competence", "weight": 12},
    {"key": "incentives", "label": "Identified incentives", "weight": 12},
    {"key": "opportunity", "label": "Considered opportunity cost", "weight": 12},
    {"key": "margin", "label": "Included margin of safety", "weight": 12},
    {"key": "second_order", "label": "Considered second-order effects", "weight": 12},
    {"key": "probability", "label": "Assigned probabilities", "weight": 10},
    {"key": "disconfirming", "label": "Defined disconfirming evidence", "weight": 10},
    {"key": "checklist", "label": "Used a checklist / review process", "weight": 8},
]


DAILY_THEMES = [
    "Avoid one obvious stupidity before chasing one brilliant move.",
    "Invert the day: what would make it a waste?",
    "Respect incentives. They are the hidden architecture of behavior.",
    "Stay inside the circle, or label the excursion as speculation.",
    "Leave room for error. Reality does not care about your spreadsheet.",
    "Trade certainty for calibrated probability.",
    "Protect what compounds: health, knowledge, trust, capital, reputation.",
]
