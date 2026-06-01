"""
Reusable Dashboard Components
=============================
KPI cards, metric displays, and other dashboard components.
"""

import streamlit as st
import plotly.graph_objects as go


def kpi_card(title, value, delta=None, format_type="number", suffix=""):
    """
    Display a metric card.

    Args:
        title (str): Card title
        value (float/int): Main metric value
        delta (float): Optional change/delta value
        format_type (str): "number", "percent", or "decimal"
        suffix (str): Optional suffix for the value
    """

    if format_type == "number":
        if isinstance(value, (int, float)):
            formatted_value = f"{int(value):,}{suffix}"
        else:
            formatted_value = str(value) + suffix

    elif format_type == "percent":
        formatted_value = f"{float(value):.1f}%"

    elif format_type == "decimal":
        formatted_value = f"{float(value):.2f}{suffix}"

    else:
        formatted_value = str(value) + suffix

    if delta is not None:
        st.metric(label=title, value=formatted_value, delta=delta)
    else:
        st.metric(label=title, value=formatted_value)


def create_conversion_funnel(funnel_data):
    """
    Create a conversion funnel chart.

    Args:
        funnel_data (dict): Contains 'Stage' and 'Count' lists

    Returns:
        go.Figure: Plotly figure object
    """

    # Calculate percentages
    total = funnel_data["Count"][0]
    percentages = [int((count / total) * 100) for count in funnel_data["Count"]]

    # Create labels with counts and percentages
    labels = [
        f"{stage}<br>{count:,} ({pct}%)"
        for stage, count, pct in zip(
            funnel_data["Stage"], funnel_data["Count"], percentages
        )
    ]

    fig = go.Figure(
        go.Funnel(
            x=funnel_data["Count"],
            y=funnel_data["Stage"],
            text=labels,
            textposition="inside",
            marker=dict(
                color=["#1f77b4", "#4a9ed5", "#7db8e8", "#a8ceee", "#d4e1f5", "#e8eef9"]
            ),
            connector={"line": {"color": "#cccccc"}},
        )
    )

    if len(funnel_data["Count"]) > 1:
        losses = [
            funnel_data["Count"][index] - funnel_data["Count"][index + 1]
            for index in range(len(funnel_data["Count"]) - 1)
        ]
        largest_drop_index = int(max(range(len(losses)), key=losses.__getitem__))
        largest_drop_label = (
            f"Largest drop-off: {funnel_data['Stage'][largest_drop_index]} → "
            f"{funnel_data['Stage'][largest_drop_index + 1]} ({losses[largest_drop_index]:,})"
        )
    else:
        largest_drop_label = "Largest drop-off: not enough stages to calculate"

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=40, b=40),
        template="plotly_white",
        font=dict(size=11),
        annotations=[
            dict(
                text=largest_drop_label,
                x=0.5,
                y=1.08,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=12, color="#d62728"),
                align="center",
            )
        ],
    )

    return fig


def chart_caption(label, source, note=None):
    """
    Show a short, consistent chart caption.

    Args:
        label (str): Plain-language chart description.
        source (str): Retained for backward compatibility.
        note (str | None): Optional extra context.
    """

    parts = [f"{label}."]
    if note:
        parts.append(note)
    st.caption(" ".join(parts))


def how_to_read_chart(points):
    """
    Render a compact guide for interpreting a chart.

    Args:
        points (list[str]): 2-4 short interpretation points.
    """

    if not points:
        return

    st.markdown("**How to read this chart**")
    for point in points:
        st.markdown(f"- {point}")
