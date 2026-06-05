"""
data.py — Reference data for Munger OS v2.

Single source of truth for mental models, daily themes, decision criteria,
and the bias taxonomy. Expanded from v1 to reflect the full range of
Munger's multidisciplinary latticework.
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
        explanation="Instead of asking how to succeed, identify what would reliably cause failure, then avoid those conditions. Most people never invert. They spend all their energy planning for the best case while the worst case destroys them.",
        question="What would make this fail?",
        action="List three ways this could go wrong and remove one today.",
        decision_use="Best for strategy, risk review, and avoiding self-inflicted damage.",
    ),
    MentalModel(
        name="Circle of Competence",
        category="Self-Knowledge",
        principle="Know the boundary of what you understand.",
        explanation="The advantage is not knowing everything. The advantage is knowing where your knowledge stops. Most disasters happen at the edge of the circle where people don't realize they've left it.",
        question="Where am I pretending to know more than I do?",
        action="Mark one assumption that needs outside expertise or more evidence.",
        decision_use="Best for investments, career moves, technical decisions, and delegation.",
    ),
    MentalModel(
        name="Incentives",
        category="Human Behavior",
        principle="Behavior follows incentives more often than intentions.",
        explanation="People and institutions usually respond to rewards, penalties, status, fear, and convenience — not to stated values. Show me the incentive and I'll show you the outcome. The most reliable way to change behavior is to change incentives.",
        question="What incentives are driving each party?",
        action="Identify one incentive that is misaligned with the desired outcome.",
        decision_use="Best for management, negotiations, organizations, contracts, and policy.",
    ),
    MentalModel(
        name="Opportunity Cost",
        category="Economics",
        principle="Every yes is a no to something else.",
        explanation="The true cost of a choice is the best alternative you gave up: time, attention, money, reputation, or optionality. Most people calculate the sticker price and ignore the opportunity cost.",
        question="What am I giving up by choosing this?",
        action="Name the best alternative and decide whether this still wins.",
        decision_use="Best for prioritization, project selection, and personal finance.",
    ),
    MentalModel(
        name="Margin of Safety",
        category="Risk Management",
        principle="Leave room for error.",
        explanation="Good systems survive bad assumptions, delays, volatility, and ordinary human imperfection. The margin of safety is not pessimism — it is the acknowledgment that your model of reality is incomplete.",
        question="Where is the buffer too thin?",
        action="Add a time, money, review, redundancy, or fallback buffer.",
        decision_use="Best for planning, investing, engineering, operations, and health.",
    ),
    MentalModel(
        name="Second-Order Thinking",
        category="Systems Thinking",
        principle="Ask what happens after the first consequence.",
        explanation="The immediate effect is usually obvious. The delayed effect is where judgment begins. First-order thinking produces solutions that create new problems. Second-order thinking anticipates them.",
        question="What happens next, and then what?",
        action="Write one likely second-order consequence before acting.",
        decision_use="Best for policy, leadership, pricing, incentives, and life planning.",
    ),
    MentalModel(
        name="Probabilistic Thinking",
        category="Uncertainty",
        principle="Think in odds, not certainties.",
        explanation="Good judgment does not require certainty. It requires calibrated confidence and willingness to update when evidence changes. Certainty is usually a signal of ideology, not rigor.",
        question="What is the probability I am wrong?",
        action="Assign a confidence percentage and identify what would change it.",
        decision_use="Best for forecasting, investments, strategy, and uncertain outcomes.",
    ),
    MentalModel(
        name="Compounding",
        category="Long-Term Thinking",
        principle="Small advantages become decisive when repeated.",
        explanation="Knowledge, habits, capital, trust, reputation, and health compound when protected from interruption. The enemy of compounding is not slowness — it is the catastrophic loss that resets the clock.",
        question="What behavior compounds if repeated?",
        action="Do one small action that benefits your future self without risking compounding.",
        decision_use="Best for learning, fitness, investing, and reputation.",
    ),
    MentalModel(
        name="Avoiding Stupidity",
        category="Practical Wisdom",
        principle="Avoid obvious mistakes before seeking brilliance.",
        explanation="Many good outcomes come from not doing dumb things: overleveraging, overcommitting, reacting emotionally, ignoring incentives, or operating outside the circle of competence. You don't need to be brilliant — you need to be reliably not stupid.",
        question="What is the dumbest preventable mistake here?",
        action="Build one guardrail against that mistake before moving forward.",
        decision_use="Best for almost everything.",
    ),
    MentalModel(
        name="Lollapalooza Effect",
        category="Psychology",
        principle="Multiple forces can combine into extreme behavior.",
        explanation="Incentives, social proof, authority, scarcity, envy, and fear can reinforce each other and produce irrational outcomes that no single force would cause alone. This is the mechanism behind bubbles, cults, manias, and organizational dysfunction.",
        question="Which forces are combining here?",
        action="List the psychological forces acting in the same direction.",
        decision_use="Best for bubbles, crowd behavior, marketing, politics, and organizational dysfunction.",
    ),
    MentalModel(
        name="Disconfirming Evidence",
        category="Epistemic Discipline",
        principle="Know what would prove you wrong.",
        explanation="A belief that cannot be tested or challenged becomes ideology, not judgment. The most valuable question before committing is: what would have to be true for this to be wrong? Most people never ask it.",
        question="What evidence would change my mind?",
        action="Write one observable fact that would weaken your current view.",
        decision_use="Best for strategic planning, research, hiring, and investment theses.",
    ),
    MentalModel(
        name="Checklist Discipline",
        category="Execution",
        principle="Use checklists where errors are costly and predictable.",
        explanation="The goal is not bureaucracy. The goal is preventing known errors when attention fails. Surgeons, pilots, and investors who use checklists outperform those who trust memory. The checklist doesn't add intelligence — it subtracts preventable stupidity.",
        question="What step should not be trusted to memory?",
        action="Turn one repeated risk into a checklist item.",
        decision_use="Best for operations, QA, finance, travel, health, and project delivery.",
    ),
    MentalModel(
        name="Regression to the Mean",
        category="Statistics",
        principle="Extreme results tend to revert toward average over time.",
        explanation="Exceptional performance — good or bad — often contains a luck component that won't persist. Praising a manager after an outlier quarter and firing one after a bad year both attribute randomness to skill. Most extreme results are partly transient. Build your model on the base rate.",
        question="How much of this result is repeatable skill versus temporary luck?",
        action="Identify the base rate before drawing conclusions from the most recent data point.",
        decision_use="Best for hiring, performance reviews, investing, sports, and interpreting any extreme outcome.",
    ),
    MentalModel(
        name="Survivorship Bias",
        category="Epistemic Discipline",
        principle="You only see the winners. The losers are invisible.",
        explanation="Books are written by successful founders, not by the majority who failed. Strategies look brilliant in backtests because the failures never made it into the dataset. The graveyard of failed experiments contains the most important lessons — and you can't see it.",
        question="What am I not seeing because it failed and disappeared?",
        action="Deliberately seek failure cases before drawing lessons from success stories.",
        decision_use="Best for strategy, investing, hiring, product decisions, and learning from history.",
    ),
    MentalModel(
        name="Feedback Loops",
        category="Systems Thinking",
        principle="Outputs become inputs. Effects become causes.",
        explanation="Reinforcing loops amplify: wealth attracts capital, reputation attracts talent, skill attracts opportunity — and debt attracts more debt. Balancing loops regulate: price rises reduce demand, fatigue reduces effort. Identifying which loop dominates determines what interventions are useful.",
        question="Which feedback loops are active here, and do they reinforce or balance?",
        action="Map one feedback loop in this system before deciding to intervene.",
        decision_use="Best for organizations, markets, personal habits, and any complex adaptive system.",
    ),
    MentalModel(
        name="Comparative Advantage",
        category="Economics",
        principle="Do what you are relatively best at. Delegate or trade the rest.",
        explanation="Even if you are better at everything than everyone else, specialization and exchange increase total output. The opportunity cost of doing something yourself is often higher than it appears. The question is not whether you can do it, but whether doing it is the best use of limited time and attention.",
        question="Is this the highest-value use of my time relative to the available alternatives?",
        action="Identify one task to delegate or eliminate — even if you could do it yourself.",
        decision_use="Best for career decisions, delegation, team structure, and time allocation.",
    ),
    MentalModel(
        name="Occam's Razor",
        category="Epistemic Discipline",
        principle="Prefer the simpler explanation when evidence is equal.",
        explanation="Complexity is not a sign of rigor. A simpler model with the same predictive power is more robust — fewer hidden assumptions, fewer points of failure, easier to test and falsify. Most elaborate explanations are rationalizations. The simplest explanation consistent with the facts is the right place to start.",
        question="Is there a simpler explanation that fits the same evidence?",
        action="Remove one unnecessary assumption from the current analysis.",
        decision_use="Best for diagnosis, root cause analysis, strategy, and evaluating competing theories.",
    ),
    MentalModel(
        name="Deprival Superreaction",
        category="Psychology",
        principle="People react to loss far more intensely than to equivalent gain.",
        explanation="The pain of losing something you have — or almost have — triggers disproportionate behavior. This drives sunk cost fallacies, takeover premiums, bitter disputes over minor items, and irrational escalation. Munger considered this one of the most dangerous and least-recognized psychological tendencies in business and investing.",
        question="Am I fighting this hard because the stakes are high, or because losing feels intolerable?",
        action="Reframe the choice as if you did not already own the thing at risk. Would you still choose it?",
        decision_use="Best for negotiations, portfolio decisions, organizational disputes, and recognizing escalation traps.",
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
    "Deprival superreaction": "Disproportionate distress at losing something already possessed or nearly possessed — the engine of sunk cost fallacies and escalation.",
    "Envy and jealousy": "Distorting reasoning or taking harmful actions to match, undermine, or punish perceived rivals.",
    "Contrast miscognition": "Evaluating an option relative to what came immediately before it rather than on its own merits.",
    "Liking/disliking bias": "Distorting facts, beliefs, or actions to favor those you like — and oppose those you dislike — regardless of evidence.",
    "Twaddle tendency": "Filling silence and uncertainty with confident-sounding noise rather than admitting what is unknown.",
}


DECISION_CRITERIA = [
    {"key": "inversion",     "label": "Inverted failure modes",          "weight": 12},
    {"key": "circle",        "label": "Checked circle of competence",    "weight": 12},
    {"key": "incentives",    "label": "Identified incentives",           "weight": 12},
    {"key": "opportunity",   "label": "Considered opportunity cost",     "weight": 12},
    {"key": "margin",        "label": "Included margin of safety",       "weight": 12},
    {"key": "second_order",  "label": "Considered second-order effects", "weight": 12},
    {"key": "probability",   "label": "Assigned probabilities",          "weight": 10},
    {"key": "disconfirming", "label": "Defined disconfirming evidence",  "weight": 10},
    {"key": "checklist",     "label": "Used a checklist / review process", "weight": 8},
]


DAILY_THEMES = [
    "Avoid one obvious stupidity before chasing one brilliant move.",
    "Invert the day: what would make it a waste?",
    "Respect incentives. They are the hidden architecture of behavior.",
    "Stay inside the circle, or label the excursion as speculation.",
    "Leave room for error. Reality does not care about your spreadsheet.",
    "Trade certainty for calibrated probability.",
    "Protect what compounds: health, knowledge, trust, capital, reputation.",
    "Read something outside your domain. The best mental models come from elsewhere.",
    "The fat pitch is rare. Most decisions can wait for better conditions.",
    "Envy is the dumbest sin. It makes you worse without making anyone better.",
    "The biggest risk is not volatility. It is permanent, unrecoverable loss.",
    "Complexity is not sophistication. Strip the unnecessary before adding anything.",
    "Most preventable damage comes from a short list of well-known mistakes. Know the list.",
    "Ideology is the enemy of clear thinking. Note which conclusions you are prohibited from reaching.",
    "A model that only works under favorable conditions is not a model. It is a wish.",
    "Sit with the disconfirming evidence longer than is comfortable.",
    "Deprival makes people irrational. Know when you are fighting to avoid a loss, not to achieve a gain.",
    "The lesson is rarely visible in the moment. Write it down before the story hardens.",
    "An inability to say no is cowardice dressed as agreeableness.",
    "First principles: what is actually true here, not what usually happens.",
    "The best decision today is sometimes the one you refuse to make.",
    "Survivorship bias is everywhere. Ask what you are not seeing.",
    "Do not mistake intensity of belief for quality of evidence.",
    "The second-order effect is almost always less convenient than the first.",
    "One mental model is a hammer. A latticework of models is a workshop.",
    "Slowing down is how you avoid most self-inflicted damage.",
    "Calibration is the skill. Confidence alone is noise.",
    "Patience is not passivity. It is the discipline to wait for the right conditions.",
    "Know your biases. Then assume you are exhibiting them right now.",
    "You don't need to be brilliant. You need to be reliably not stupid.",
]
