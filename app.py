"""
app.py — Streamlit interface for Munger OS.

Run locally with:
    streamlit run app.py
"""

from __future__ import annotations

from datetime import datetime, date

import pandas as pd
import streamlit as st

from data import MENTAL_MODELS, BIAS_TAXONOMY, DECISION_CRITERIA
from model import calculate_decision_score, detect_bias_flags
from journal import save_reflection, load_reflections, save_decision, load_decisions, save_review, load_reviews
from wisdom_engine import get_daily_model, get_daily_theme, generate_inversion_prompt
from viz import build_decision_quality_distribution, build_model_usage_chart, build_score_trend

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
        "Bias Detector",
        "Wisdom Dashboard",
        "Methodology",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("This app is a judgment-training system, not a quote collector.")


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
        action = st.text_area("What action will you take?", height=120)
        if st.button("Save Reflection"):
            if reflection.strip():
                save_reflection(daily.name, theme, reflection, action)
                st.success("Reflection saved.")
            else:
                st.error("Write a reflection before saving.")


elif page == "Mental Models Library":
    st.title("Mental Models Library")
    st.write("A practical multidisciplinary checklist for judgment.")

    df = pd.DataFrame([m.__dict__ for m in MENTAL_MODELS])
    categories = st.multiselect("Filter by category", sorted(df["category"].unique()))
    if categories:
        df = df[df["category"].isin(categories)]

    for _, row in df.iterrows():
        with st.expander(f"{row['name']} — {row['category']}"):
            st.markdown(f"**Principle:** {row['principle']}")
            st.write(row["explanation"])
            st.markdown(f"**Decision use:** {row['decision_use']}")
            st.markdown(f"**Question:** {row['question']}")
            st.markdown(f"**Action:** {row['action']}")


elif page == "Anti-Stupidity Checklist":
    st.title("Anti-Stupidity Checklist")
    st.write("Use this before consequential decisions. The goal is to avoid preventable damage.")

    checked = {}
    col1, col2 = st.columns(2)
    for i, item in enumerate(DECISION_CRITERIA):
        target = col1 if i % 2 == 0 else col2
        checked[item["key"]] = target.checkbox(f"{item['label']} ({item['weight']} pts)")

    confidence = st.slider("Confidence", 0, 100, 65)
    downside = st.slider("Downside severity if wrong", 0, 100, 50)
    result = calculate_decision_score(checked, confidence, downside)

    st.metric("Process Score", f"{result['score']}/100", result["grade"])
    st.write(result["interpretation"])
    if result["risk_warning"]:
        st.error(result["risk_warning"])
    if result["missing"]:
        st.markdown("### Missing Review Items")
        for item in result["missing"]:
            st.write(f"- {item}")


elif page == "Decision Journal":
    st.title("Decision Journal")
    st.write("Record decisions before knowing the outcome. That is how judgment improves.")

    with st.form("decision_form"):
        decision = st.text_area("Decision", height=80)
        domain = st.selectbox("Domain", ["Career", "Work", "Investment", "Health", "Family", "Learning", "Other"])
        primary_model = st.selectbox("Primary mental model", [m.name for m in MENTAL_MODELS])
        expected_outcome = st.text_area("Expected outcome", height=80)
        risks = st.text_area("Main risks / failure modes", height=90)
        opportunity_cost = st.text_area("Opportunity cost", height=80)
        incentives = st.text_area("Relevant incentives", height=80)
        disconfirming = st.text_area("What evidence would change your mind?", height=80)
        confidence = st.slider("Confidence level", 0, 100, 65)
        downside = st.slider("Downside severity if wrong", 0, 100, 50)
        revisit_date = st.date_input("Revisit date")

        st.markdown("### Process Checks")
        checked = {}
        cols = st.columns(3)
        for i, item in enumerate(DECISION_CRITERIA):
            checked[item["key"]] = cols[i % 3].checkbox(item["label"])

        submitted = st.form_submit_button("Save Decision")

    if submitted:
        if not decision.strip():
            st.error("Enter a decision before saving.")
        else:
            result = calculate_decision_score(checked, confidence, downside)
            row = {
                "date": str(date.today()),
                "decision": decision,
                "domain": domain,
                "primary_model": primary_model,
                "expected_outcome": expected_outcome,
                "risks": risks,
                "opportunity_cost": opportunity_cost,
                "incentives": incentives,
                "disconfirming_evidence": disconfirming,
                "confidence": confidence,
                "downside": downside,
                "score": result["score"],
                "grade": result["grade"],
                "revisit_date": str(revisit_date),
                "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            }
            save_decision(row)
            st.success(f"Decision saved. Process score: {result['score']}/100 — {result['grade']}.")
            if result["risk_warning"]:
                st.warning(result["risk_warning"])

    st.markdown("---")
    st.markdown("## Past Decisions")
    decisions = load_decisions()
    if decisions.empty:
        st.info("No decisions saved yet.")
    else:
        st.dataframe(decisions.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)
        st.download_button(
            "Download Decisions CSV",
            decisions.to_csv(index=False).encode("utf-8"),
            file_name="munger_os_decisions.csv",
            mime="text/csv",
        )


elif page == "Bias Detector":
    st.title("Bias Detector")
    st.write("A simple transparent bias screen. It flags language patterns; it does not diagnose your mind.")

    text = st.text_area("Paste a decision memo, thought, email, or argument", height=220)
    if st.button("Analyze"):
        flags = detect_bias_flags(text)
        if flags:
            st.warning(f"Detected {len(flags)} possible bias flags.")
            for flag in flags:
                st.markdown(f"**{flag['bias']}** — {flag['description']}")
        else:
            st.success("No obvious keyword-based bias flags detected. That does not mean the reasoning is sound.")

    st.markdown("---")
    st.markdown("### Bias Taxonomy")
    for bias, desc in BIAS_TAXONOMY.items():
        st.markdown(f"**{bias}:** {desc}")


elif page == "Wisdom Dashboard":
    st.title("Wisdom Dashboard")
    reflections = load_reflections()
    decisions = load_decisions()
    reviews = load_reviews()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reflections", len(reflections))
    c2.metric("Decisions", len(decisions))
    c3.metric("Reviews", len(reviews))
    if decisions.empty:
        c4.metric("Avg Score", "N/A")
    else:
        c4.metric("Avg Score", f"{decisions['score'].astype(float).mean():.1f}")

    st.markdown("---")
    if not decisions.empty:
        st.plotly_chart(build_decision_quality_distribution(decisions), use_container_width=True)
        st.plotly_chart(build_score_trend(decisions), use_container_width=True)
    else:
        st.info("Save decisions to populate the decision-quality visuals.")

    if not reflections.empty:
        st.plotly_chart(build_model_usage_chart(reflections), use_container_width=True)

    with st.expander("Export Data"):
        if not reflections.empty:
            st.download_button("Download Reflections CSV", reflections.to_csv(index=False).encode("utf-8"), "munger_os_reflections.csv")
        if not decisions.empty:
            st.download_button("Download Decisions CSV", decisions.to_csv(index=False).encode("utf-8"), "munger_os_decisions.csv")


elif page == "Methodology":
    st.title("Methodology")
    st.markdown("""
### What this app does

Munger OS is a structured decision-review system. It borrows the architecture of a simulation dashboard: data layer, scoring model, persistence layer, visualization layer, and Streamlit interface.

### What the score means

The score is not truth. It is a process-quality score. It asks whether the decision has been reviewed through key mental models: inversion, circle of competence, incentives, opportunity cost, margin of safety, second-order effects, probabilistic thinking, disconfirming evidence, and checklist discipline.

### Why this is better than a quote app

Quotes feel intelligent but often do not change behavior. This app forces the useful thing: write the decision, name the risk, identify incentives, define what would change your mind, and revisit later.

### Proper use

Use it before consequential decisions, not after you already want permission to do something. The danger is not lack of intelligence. The danger is motivated reasoning with a good vocabulary.
""")
