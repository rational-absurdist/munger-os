"""
app.py — Streamlit interface for Munger OS v2.

Run locally with:
    streamlit run app.py
"""

from __future__ import annotations

from datetime import datetime, date

import pandas as pd
import streamlit as st

from data import MENTAL_MODELS, BIAS_TAXONOMY, DECISION_CRITERIA
from model import calculate_decision_score, detect_bias_flags
from journal import (
    save_reflection, load_reflections,
    save_decision, load_decisions,
    save_review, load_reviews,
)
from wisdom_engine import get_daily_model, get_daily_theme, generate_inversion_prompt
from viz import (
    build_decision_quality_distribution,
    build_model_usage_chart,
    build_score_trend,
    build_calibration_chart,
    build_magnitude_reversibility_scatter,
)

st.set_page_config(page_title="Munger OS", page_icon="🧠", layout="wide")

st.sidebar.title("Munger OS")
st.sidebar.caption("Avoid stupidity. Think clearly. Compound wisdom.")
page = st.sidebar.radio(
    "Navigation",
    [
        "Daily Dose",
        "Mental Models Library",
        "Anti-Stupidity Checklist",
        "Decision Journal",
        "Outcome Review",
        "Bias Detector",
        "Wisdom Dashboard",
        "Methodology",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("This app is a judgment-training system, not a quote collector.")


# ── Daily Dose ──────────────────────────────────────────────────────────────

if page == "Daily Dose":
    daily = get_daily_model()
    theme = get_daily_theme()

    st.title("Munger OS")
    st.subheader("Daily Dose of Judgment")

    c1, c2 = st.columns([2.2, 1])
    with c1:
        st.markdown(f"## {daily.name}")
        st.markdown(f"**Category:** {daily.category}")
        st.info(daily.principle)
        st.write(daily.explanation)
        st.markdown("### Daily Theme")
        st.warning(theme)
        st.markdown("### Question")
        st.write(daily.question)
        st.markdown("### Action")
        st.success(daily.action)

    with c2:
        st.markdown("### Reflection")
        reflection = st.text_area("What does this mean today?", height=170)
        action_text = st.text_area("What action will you take?", height=120)
        if st.button("Save Reflection"):
            if reflection.strip():
                save_reflection(daily.name, theme, reflection, action_text)
                st.success("Reflection saved.")
            else:
                st.error("Write a reflection before saving.")


# ── Mental Models Library ────────────────────────────────────────────────────

elif page == "Mental Models Library":
    st.title("Mental Models Library")
    st.write(
        "A multidisciplinary latticework for judgment. "
        f"{len(MENTAL_MODELS)} models across {len(set(m.category for m in MENTAL_MODELS))} disciplines."
    )

    df = pd.DataFrame([m.__dict__ for m in MENTAL_MODELS])
    categories = st.multiselect("Filter by category", sorted(df["category"].unique()))
    if categories:
        df = df[df["category"].isin(categories)]

    search = st.text_input("Search models", placeholder="e.g. incentives, loop, loss…")
    if search:
        mask = df.apply(lambda r: search.lower() in r.to_string().lower(), axis=1)
        df = df[mask]

    st.caption(f"Showing {len(df)} model(s).")
    for _, row in df.iterrows():
        with st.expander(f"{row['name']} — {row['category']}"):
            st.markdown(f"**Principle:** {row['principle']}")
            st.write(row["explanation"])
            st.markdown(f"**Decision use:** {row['decision_use']}")
            st.markdown(f"**Question:** *{row['question']}*")
            st.markdown(f"**Action:** {row['action']}")


# ── Anti-Stupidity Checklist ─────────────────────────────────────────────────

elif page == "Anti-Stupidity Checklist":
    st.title("Anti-Stupidity Checklist")
    st.write(
        "Use this before consequential decisions. "
        "The goal is to avoid preventable damage, not to guarantee a good outcome."
    )

    checked = {}
    col1, col2 = st.columns(2)
    for i, item in enumerate(DECISION_CRITERIA):
        target = col1 if i % 2 == 0 else col2
        checked[item["key"]] = target.checkbox(f"{item['label']} ({item['weight']} pts)")

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    confidence  = c1.slider("Confidence",          0, 100, 65)
    downside    = c2.slider("Downside severity",   0, 100, 50)
    reversibility = c3.slider(
        "Reversibility", 0, 100, 50,
        help="0 = permanent decision, 100 = fully reversible within 6 months",
    )
    magnitude   = c4.slider(
        "Magnitude", 0, 100, 50,
        help="0 = minor, 100 = career or life-defining",
    )

    result = calculate_decision_score(checked, confidence, downside, reversibility, magnitude)

    st.metric("Process Score", f"{result['score']}/100", result["grade"])
    st.write(result["interpretation"])
    if result["risk_warning"]:
        st.error(result["risk_warning"])
    if result["missing"]:
        st.markdown("### Missing Review Items")
        for item in result["missing"]:
            st.write(f"- {item}")


# ── Decision Journal ─────────────────────────────────────────────────────────

elif page == "Decision Journal":
    st.title("Decision Journal")
    st.write(
        "Record decisions **before** knowing the outcome. "
        "That is how judgment improves. The feedback loop closes in Outcome Review."
    )

    with st.form("decision_form"):
        decision = st.text_area("Decision", height=80,
            placeholder="Be specific. Vague decisions produce vague lessons.")

        fat_pitch_confirmed = st.checkbox(
            "This decision is worth making now — not a reflex, not FOMO, not someone else's urgency.",
            value=False,
        )

        c1, c2 = st.columns(2)
        domain = c1.selectbox(
            "Domain",
            ["Career", "Work", "Investment", "Health", "Family", "Learning", "Other"],
        )
        primary_model = c2.selectbox("Primary mental model", [m.name for m in MENTAL_MODELS])

        st.markdown("---")
        st.markdown("#### Inversion")
        st.caption(
            "Munger's most important tool: before planning for success, "
            "identify the reliable causes of failure and remove them."
        )
        inversion_response = st.text_area(
            "Assume this decision fails badly. What are the three most likely causes?",
            height=90,
            placeholder="1. …  2. …  3. …",
        )

        st.markdown("---")
        expected_outcome = st.text_area("Expected outcome", height=80)
        risks = st.text_area("Main risks and failure modes", height=80)

        c1, c2 = st.columns(2)
        opportunity_cost = c1.text_area("Opportunity cost (what you give up)", height=80)
        incentives       = c2.text_area("Relevant incentives (all parties)", height=80)

        disconfirming = st.text_area(
            "What evidence would change your mind?",
            height=70,
            placeholder="If X happens, I was wrong.",
        )

        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        confidence    = c1.slider("Confidence",        0, 100, 65)
        downside      = c2.slider("Downside severity", 0, 100, 50)
        reversibility = c3.slider(
            "Reversibility", 0, 100, 50,
            help="0 = permanent, 100 = fully reversible within 6 months",
        )
        magnitude = c4.slider(
            "Magnitude", 0, 100, 50,
            help="0 = minor, 100 = career or life-defining",
        )

        revisit_date = st.date_input("Revisit date")

        st.markdown("#### Process Checks")
        checked = {}
        cols = st.columns(3)
        for i, item in enumerate(DECISION_CRITERIA):
            checked[item["key"]] = cols[i % 3].checkbox(item["label"])

        submitted = st.form_submit_button("Save Decision")

    if submitted:
        if not decision.strip():
            st.error("Enter a decision before saving.")
        else:
            if not fat_pitch_confirmed:
                st.warning(
                    "You haven't confirmed this is worth deciding now. "
                    "Munger's most valuable habit was **not deciding** until conditions were right. "
                    "Check the box if you've genuinely considered this."
                )

            result = calculate_decision_score(checked, confidence, downside, reversibility, magnitude)
            row = {
                "date":                  str(date.today()),
                "decision":              decision,
                "domain":                domain,
                "primary_model":         primary_model,
                "inversion_response":    inversion_response,
                "expected_outcome":      expected_outcome,
                "risks":                 risks,
                "opportunity_cost":      opportunity_cost,
                "incentives":            incentives,
                "disconfirming_evidence": disconfirming,
                "confidence":            confidence,
                "downside":              downside,
                "reversibility":         reversibility,
                "magnitude":             magnitude,
                "fat_pitch_confirmed":   fat_pitch_confirmed,
                "score":                 result["score"],
                "grade":                 result["grade"],
                "revisit_date":          str(revisit_date),
                "timestamp":             datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            }
            save_decision(row)
            st.success(f"Decision saved. Process score: {result['score']}/100 — {result['grade']}.")
            st.write(result["interpretation"])
            if result["risk_warning"]:
                st.error(result["risk_warning"])
            if result["missing"]:
                st.markdown("**Missing review items:** " + " | ".join(result["missing"]))

    st.markdown("---")
    st.markdown("## Past Decisions")
    decisions = load_decisions()
    if decisions.empty:
        st.info("No decisions saved yet.")
    else:
        display_cols = ["date", "decision", "domain", "primary_model", "score", "grade", "revisit_date"]
        available = [c for c in display_cols if c in decisions.columns]
        st.dataframe(
            decisions[available].sort_values("date", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            "Download Decisions CSV",
            decisions.to_csv(index=False).encode("utf-8"),
            file_name="munger_os_decisions.csv",
            mime="text/csv",
        )


# ── Outcome Review ───────────────────────────────────────────────────────────

elif page == "Outcome Review":
    st.title("Outcome Review")
    st.write(
        "Close the loop. Without comparing predictions to outcomes, "
        "the Decision Journal is a one-way street. This is where calibration happens."
    )

    decisions = load_decisions()
    if decisions.empty:
        st.info("No decisions saved yet. Record decisions before reviewing outcomes.")
    else:
        decision_labels = [
            f"{row['date']} — {str(row['decision'])[:65]}…"
            for _, row in decisions.iterrows()
        ]
        selected_idx = st.selectbox(
            "Select a decision to review",
            range(len(decision_labels)),
            format_func=lambda i: decision_labels[i],
        )
        selected = decisions.iloc[selected_idx]

        with st.expander("Original Decision Details", expanded=True):
            c1, c2 = st.columns(2)
            c1.markdown(f"**Decision:** {selected.get('decision', '—')}")
            c1.markdown(f"**Expected outcome:** {selected.get('expected_outcome', '—')}")
            c1.markdown(f"**Inversion response:** {selected.get('inversion_response', '—')}")
            c2.markdown(f"**Confidence at time:** {selected.get('confidence', '—')}%")
            c2.markdown(f"**Downside severity:** {selected.get('downside', '—')}")
            c2.markdown(f"**Process score:** {selected.get('score', '—')} — {selected.get('grade', '—')}")
            reversibility_val = selected.get("reversibility", "—")
            magnitude_val = selected.get("magnitude", "—")
            c2.markdown(f"**Reversibility / Magnitude:** {reversibility_val} / {magnitude_val}")

        with st.form("review_form"):
            actual_outcome = st.text_area("What actually happened?", height=100)
            prediction_accuracy = st.slider(
                "How accurate was your prediction?", 0, 100, 50,
                help="0 = completely wrong, 100 = exactly right",
            )
            grade_accuracy = st.radio(
                "Did the process score reflect the quality of your reasoning?",
                ["Accurate", "Score was too high", "Score was too low"],
                horizontal=True,
            )
            lesson = st.text_area(
                "What is the one lesson to carry forward?",
                height=90,
                placeholder="Be specific. Vague lessons don't compound.",
            )
            review_submitted = st.form_submit_button("Save Review")

        if review_submitted:
            if not actual_outcome.strip():
                st.error("Enter what actually happened before saving.")
            else:
                row = {
                    "date":                str(date.today()),
                    "decision_ref":        str(selected.get("timestamp", "")),
                    "original_decision":   str(selected.get("decision", "")),
                    "predicted_outcome":   str(selected.get("expected_outcome", "")),
                    "actual_outcome":      actual_outcome,
                    "prediction_accuracy": prediction_accuracy,
                    "process_score":       str(selected.get("score", "")),
                    "grade_accuracy":      grade_accuracy,
                    "lesson":              lesson,
                    "timestamp":           datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                }
                save_review(row)
                st.success("Review saved.")

                if prediction_accuracy < 40:
                    st.error(
                        "Your prediction was significantly off. "
                        "That is useful data. What assumption was wrong? "
                        "The lesson is in the gap between what you expected and what happened."
                    )
                elif prediction_accuracy < 65:
                    st.warning(
                        "Partial accuracy. Identify which part of the prediction was wrong "
                        "and whether the process could have caught it."
                    )
                else:
                    st.info(
                        "Good prediction. Before crediting the process, verify whether "
                        "the outcome was driven by your reasoning or by favorable conditions."
                    )

        st.markdown("---")
        reviews = load_reviews()
        if not reviews.empty:
            st.markdown("## Review History")
            display_cols = ["date", "original_decision", "prediction_accuracy", "grade_accuracy", "lesson"]
            available = [c for c in display_cols if c in reviews.columns]
            st.dataframe(
                reviews[available].sort_values("date", ascending=False),
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "Download Reviews CSV",
                reviews.to_csv(index=False).encode("utf-8"),
                file_name="munger_os_reviews.csv",
                mime="text/csv",
            )
        else:
            st.info("No outcome reviews saved yet.")


# ── Bias Detector ────────────────────────────────────────────────────────────

elif page == "Bias Detector":
    st.title("Bias Detector")
    st.write(
        "Paste a decision memo, email, or argument. "
        "This flags language patterns — it does not diagnose your mind."
    )

    text = st.text_area("Text to analyze", height=220)
    if st.button("Analyze"):
        if not text.strip():
            st.error("Paste some text first.")
        else:
            flags = detect_bias_flags(text)
            if flags:
                st.warning(f"Detected {len(flags)} possible bias flag(s).")
                for flag in flags:
                    st.markdown(f"**{flag['bias']}** — {flag['description']}")
                st.caption(
                    "Keyword matches are a starting point, not a verdict. "
                    "Use this to prompt a question, not to reach a conclusion."
                )
            else:
                st.success(
                    "No keyword-based bias flags detected. "
                    "That does not mean the reasoning is sound — "
                    "it means none of the common linguistic markers appeared."
                )

    st.markdown("---")
    st.markdown(f"### Bias Taxonomy ({len(BIAS_TAXONOMY)} biases)")
    for bias, desc in BIAS_TAXONOMY.items():
        st.markdown(f"**{bias}:** {desc}")


# ── Wisdom Dashboard ─────────────────────────────────────────────────────────

elif page == "Wisdom Dashboard":
    st.title("Wisdom Dashboard")
    reflections = load_reflections()
    decisions   = load_decisions()
    reviews     = load_reviews()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Reflections", len(reflections))
    c2.metric("Decisions", len(decisions))
    c3.metric("Reviews", len(reviews))

    if not decisions.empty:
        avg_score = decisions["score"].astype(float).mean()
        c4.metric("Avg Process Score", f"{avg_score:.1f}")
    else:
        c4.metric("Avg Process Score", "—")

    if not reviews.empty and "prediction_accuracy" in reviews.columns:
        avg_acc = pd.to_numeric(reviews["prediction_accuracy"], errors="coerce").mean()
        c5.metric("Avg Prediction Accuracy", f"{avg_acc:.0f}%")
    else:
        c5.metric("Avg Prediction Accuracy", "—")

    st.markdown("---")

    if not decisions.empty:
        st.plotly_chart(build_score_trend(decisions), use_container_width=True)
        st.plotly_chart(build_decision_quality_distribution(decisions), use_container_width=True)
        if {"magnitude", "reversibility"}.issubset(decisions.columns):
            st.plotly_chart(build_magnitude_reversibility_scatter(decisions), use_container_width=True)
    else:
        st.info("Save decisions to populate the decision-quality charts.")

    if not reviews.empty:
        st.plotly_chart(build_calibration_chart(reviews), use_container_width=True)
    else:
        st.info("Complete outcome reviews to see the calibration chart.")

    if not reflections.empty:
        st.plotly_chart(build_model_usage_chart(reflections), use_container_width=True)

    with st.expander("Export Data"):
        if not reflections.empty:
            st.download_button(
                "Download Reflections CSV",
                reflections.to_csv(index=False).encode("utf-8"),
                "munger_os_reflections.csv",
            )
        if not decisions.empty:
            st.download_button(
                "Download Decisions CSV",
                decisions.to_csv(index=False).encode("utf-8"),
                "munger_os_decisions.csv",
            )
        if not reviews.empty:
            st.download_button(
                "Download Reviews CSV",
                reviews.to_csv(index=False).encode("utf-8"),
                "munger_os_reviews.csv",
            )


# ── Methodology ──────────────────────────────────────────────────────────────

elif page == "Methodology":
    st.title("Methodology")
    st.markdown(f"""
### What this app does

Munger OS is a structured decision-review system. It borrows the architecture
of a simulation dashboard: data layer, scoring model, persistence layer,
visualization layer, and a Streamlit interface.

### What the score means

The score is not truth. It is a process-quality score. It asks whether the
decision has been reviewed through key mental models: inversion, circle of
competence, incentives, opportunity cost, margin of safety, second-order
effects, probabilistic thinking, disconfirming evidence, and checklist
discipline. Reversibility and magnitude now factor into the score — a
high-magnitude, irreversible decision with incomplete review is penalized.

### The feedback loop

v1 was a one-way street: record decisions, never close the loop.
v2 adds **Outcome Review**: link a past decision to its actual outcome,
score your prediction accuracy, and extract a lesson. The calibration chart
in the Wisdom Dashboard shows whether your process score correlates with
prediction accuracy over time. That is the mechanism by which judgment improves.

### Why inversion is explicit

In v1, inversion was a mental model in a library. In v2, it is a required
response field in the Decision Journal. Munger used inversion on nearly every
decision. The question — "assume this fails, what were the three most likely
causes?" — is not optional.

### The fat pitch

Most decisions don't need to be made today. v2 includes a confirmation
checkbox: "This decision is worth making now." If you can't check that box,
the system flags it. Patience is not passivity.

### Why this is better than a quote app

Quotes feel intelligent but rarely change behavior. This app forces the useful
thing: write the decision before you know the outcome, name the risks, identify
incentives, define disconfirming evidence, and revisit later. The test is
calibration: were your predictions right?

### Proper use

Use it before consequential decisions, not after you already want permission
to proceed. The danger is not lack of intelligence. The danger is motivated
reasoning with a good vocabulary.

**Mental models:** {len(MENTAL_MODELS)} | **Bias taxonomy:** {len(BIAS_TAXONOMY)} | **Daily themes:** 30
""")
