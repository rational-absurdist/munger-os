"""viz.py — Plotly visualizations for Munger OS v2."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PRINCIPLE_COLUMNS = [
    "Inversion", "Incentives", "Margin of Safety", "Opportunity Cost",
    "Second-Order", "Probability", "Disconfirming",
]


def build_decision_quality_distribution(decisions: pd.DataFrame) -> go.Figure:
    """Horizontal stacked bar showing reasoning coverage by decision."""
    if decisions.empty:
        return go.Figure()

    df = decisions.tail(12).copy()
    labels = df["decision"].astype(str).str.slice(0, 42)

    coverage = pd.DataFrame({"Decision": labels})
    coverage["Inversion"]        = df["score"].astype(float).clip(0, 100) * 0.16
    coverage["Incentives"]       = df["incentives"].fillna("").astype(str).str.len().clip(0, 120) / 120 * 14
    coverage["Margin of Safety"] = (100 - df["downside"].astype(float)).clip(0, 100) * 0.12
    coverage["Opportunity Cost"] = df["opportunity_cost"].fillna("").astype(str).str.len().clip(0, 120) / 120 * 14
    coverage["Second-Order"]     = df["risks"].fillna("").astype(str).str.len().clip(0, 160) / 160 * 16
    coverage["Probability"]      = df["confidence"].astype(float).clip(0, 100) * 0.12
    coverage["Disconfirming"]    = df["disconfirming_evidence"].fillna("").astype(str).str.len().clip(0, 100) / 100 * 12

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
    fig = px.bar(counts, x="Count", y="Mental Model", orientation="h",
                 title="Reflection Count by Mental Model")
    fig.update_layout(height=max(400, 32 * len(counts) + 120),
                      plot_bgcolor="white", paper_bgcolor="white")
    return fig


def build_score_trend(decisions: pd.DataFrame) -> go.Figure:
    if decisions.empty:
        return go.Figure()
    df = decisions.copy()
    df["entry"] = range(1, len(df) + 1)
    fig = px.line(df, x="entry", y="score", markers=True,
                  title="Decision Quality Score Trend",
                  labels={"entry": "Decision #", "score": "Process score"})
    fig.update_layout(yaxis_range=[0, 100], plot_bgcolor="white", paper_bgcolor="white")
    fig.add_hline(y=70, line_dash="dot", line_color="rgba(0,0,0,0.25)",
                  annotation_text="Adequate (70)", annotation_position="bottom right")
    return fig


def build_calibration_chart(reviews: pd.DataFrame) -> go.Figure:
    """Scatter of process score vs prediction accuracy — are you well-calibrated?"""
    if reviews.empty or "prediction_accuracy" not in reviews.columns:
        return go.Figure()

    df = reviews.copy()
    df["process_score"] = pd.to_numeric(df.get("process_score", pd.Series(dtype=float)), errors="coerce").fillna(50)
    df["prediction_accuracy"] = pd.to_numeric(df["prediction_accuracy"], errors="coerce").fillna(50)

    label_col = "original_decision" if "original_decision" in df.columns else None
    hover_text = df[label_col].astype(str).str.slice(0, 40) + "…" if label_col else None

    fig = go.Figure()
    fig.add_shape(
        type="line", x0=0, y0=0, x1=100, y1=100,
        line=dict(color="rgba(0,0,0,0.20)", dash="dash"),
    )
    fig.add_trace(go.Scatter(
        x=df["process_score"],
        y=df["prediction_accuracy"],
        mode="markers+text",
        text=hover_text,
        textposition="top center",
        marker=dict(size=10, color="#fca311", line=dict(width=1, color="#333")),
        hovertemplate="Process score: %{x}<br>Prediction accuracy: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title="Calibration: Process Score vs Prediction Accuracy<br><sup>Points above the diagonal = better outcome than the process score predicted</sup>",
        xaxis_title="Process score at decision time",
        yaxis_title="Actual prediction accuracy",
        xaxis_range=[0, 100],
        yaxis_range=[0, 100],
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=420,
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
    return fig


def build_magnitude_reversibility_scatter(decisions: pd.DataFrame) -> go.Figure:
    """Scatter: magnitude vs reversibility, colored by process score."""
    needed = {"magnitude", "reversibility", "score", "decision"}
    if decisions.empty or not needed.issubset(decisions.columns):
        return go.Figure()

    df = decisions.copy()
    df["magnitude"]     = pd.to_numeric(df["magnitude"], errors="coerce").fillna(50)
    df["reversibility"] = pd.to_numeric(df["reversibility"], errors="coerce").fillna(50)
    df["score"]         = pd.to_numeric(df["score"], errors="coerce").fillna(50)
    df["label"]         = df["decision"].astype(str).str.slice(0, 35) + "…"

    fig = px.scatter(
        df,
        x="reversibility",
        y="magnitude",
        color="score",
        color_continuous_scale="RdYlGn",
        range_color=[0, 100],
        hover_name="label",
        title="Decision Risk Profile<br><sup>Top-left = high magnitude + irreversible: highest-stakes quadrant</sup>",
        labels={"reversibility": "Reversibility (0 = permanent)", "magnitude": "Magnitude (0 = minor)"},
    )
    fig.add_vline(x=50, line_dash="dot", line_color="rgba(0,0,0,0.15)")
    fig.add_hline(y=50, line_dash="dot", line_color="rgba(0,0,0,0.15)")
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white", height=420,
        coloraxis_colorbar=dict(title="Process score"),
    )
    return fig
