"""viz.py — Plotly visualizations for Munger OS."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PRINCIPLE_COLUMNS = [
    "Inversion", "Incentives", "Margin of Safety", "Opportunity Cost", "Second-Order", "Probability", "Disconfirming"
]


def build_decision_quality_distribution(decisions: pd.DataFrame) -> go.Figure:
    """Horizontal stacked bar showing reasoning coverage by decision."""
    if decisions.empty:
        return go.Figure()

    df = decisions.tail(12).copy()
    labels = df["decision"].astype(str).str.slice(0, 42)

    # Approximate coverage values from available fields and score.
    coverage = pd.DataFrame({"Decision": labels})
    coverage["Inversion"] = df["score"].astype(float).clip(0, 100) * 0.16
    coverage["Incentives"] = df["incentives"].fillna("").astype(str).str.len().clip(0, 120) / 120 * 14
    coverage["Margin of Safety"] = (100 - df["downside"].astype(float)).clip(0, 100) * 0.12
    coverage["Opportunity Cost"] = df["opportunity_cost"].fillna("").astype(str).str.len().clip(0, 120) / 120 * 14
    coverage["Second-Order"] = df["risks"].fillna("").astype(str).str.len().clip(0, 160) / 160 * 16
    coverage["Probability"] = df["confidence"].astype(float).clip(0, 100) * 0.12
    coverage["Disconfirming"] = df["disconfirming_evidence"].fillna("").astype(str).str.len().clip(0, 100) / 100 * 12

    fig = go.Figure()
    colors = ["#fff2b2", "#ffd166", "#fca311", "#f77f00", "#e85d04", "#d00000", "#9d0208"]
    for col, color in zip(PRINCIPLE_COLUMNS, colors):
        fig.add_trace(go.Bar(
            y=coverage["Decision"],
            x=coverage[col],
            name=col,
            orientation="h",
            marker=dict(color=color, line=dict(width=0.4, color="rgba(255,255,255,0.7)")),
            hovertemplate=f"%{{y}}<br>{col}: %{{x:.1f}}<extra></extra>",
        ))

    fig.update_layout(
        title="Decision Quality Distribution by Principle<br><sup>Band width = strength of reasoning coverage by mental model</sup>",
        barmode="stack",
        height=max(450, 42 * len(coverage) + 160),
        xaxis_title="Reasoning coverage index",
        yaxis_title="",
        legend_orientation="h",
        legend_y=-0.18,
        margin=dict(l=20, r=20, t=80, b=90),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.10)")
    fig.update_yaxes(autorange="reversed")
    return fig


def build_model_usage_chart(reflections: pd.DataFrame) -> go.Figure:
    if reflections.empty:
        return go.Figure()
    counts = reflections["model"].value_counts().reset_index()
    counts.columns = ["Mental Model", "Count"]
    fig = px.bar(counts, x="Count", y="Mental Model", orientation="h", title="Reflection Count by Mental Model")
    fig.update_layout(height=max(400, 32 * len(counts) + 120), plot_bgcolor="white", paper_bgcolor="white")
    return fig


def build_score_trend(decisions: pd.DataFrame) -> go.Figure:
    if decisions.empty:
        return go.Figure()
    df = decisions.copy()
    df["entry"] = range(1, len(df) + 1)
    fig = px.line(df, x="entry", y="score", markers=True, title="Decision Quality Score Trend")
    fig.update_layout(yaxis_range=[0, 100], plot_bgcolor="white", paper_bgcolor="white")
    return fig
