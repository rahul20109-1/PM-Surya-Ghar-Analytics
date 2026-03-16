"""
Chart Creation Utilities
========================
Reusable charting functions for visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def create_adoption_trend(datewise_df):
    """
    Create cumulative adoption trend chart.

    Args:
        datewise_df (pd.DataFrame): Datewise data with date and adoption metrics

    Returns:
        go.Figure: Plotly figure object
    """

    # Prepare data
    df = datewise_df.copy()
    df["rptdate"] = pd.to_datetime(df["rptdate"])
    df = df.sort_values("rptdate")
    df["cum_applications"] = df["applications"].cumsum()
    df["cum_installations"] = df["installations"].cumsum()

    # Create figure with secondary y-axis
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["rptdate"],
            y=df["cum_applications"],
            name="Applications",
            mode="lines",
            line=dict(color="#1f77b4", width=2),
            fill="tozeroy",
            fillcolor="rgba(31, 119, 180, 0.1)",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["rptdate"],
            y=df["cum_installations"],
            name="Installations",
            mode="lines",
            line=dict(color="#ff7f0e", width=2),
            fill="tozeroy",
            fillcolor="rgba(255, 127, 14, 0.1)",
        )
    )

    fig.update_layout(
        title="Cumulative Adoption Over Time",
        xaxis_title="Date",
        yaxis_title="Cumulative Count",
        hovermode="x unified",
        height=500,
        template="plotly_white",
        legend=dict(x=0.01, y=0.99),
        margin=dict(l=0, r=0, t=30, b=0),
    )

    return fig


def create_state_ranking_chart(state_data_df):
    """
    Create state ranking bar chart.

    Args:
        state_data_df (pd.DataFrame): State data with applications and installations

    Returns:
        go.Figure: Plotly figure object
    """

    df = state_data_df.copy()

    # Create grouped bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["state"],
            y=df["applications"],
            name="Applications",
            marker_color="#1f77b4",
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["state"],
            y=df["installations"],
            name="Installations",
            marker_color="#ff7f0e",
        )
    )

    fig.update_layout(
        title="State Rankings: Applications vs Installations",
        xaxis_title="State",
        yaxis_title="Count",
        barmode="group",
        height=500,
        template="plotly_white",
        xaxis_tickangle=-45,
        margin=dict(b=100),
        legend=dict(x=0.01, y=0.99),
    )

    return fig


def create_conversion_rate_chart(state_data_df):
    """
    Create horizontal bar chart for conversion rates.

    Args:
        state_data_df (pd.DataFrame): State data with conversion rates

    Returns:
        go.Figure: Plotly figure object
    """

    df = state_data_df.sort_values("conversion_rate_app_to_install_pct", ascending=True)

    fig = go.Figure(
        go.Bar(
            y=df["state"],
            x=df["conversion_rate_app_to_install_pct"],
            orientation="h",
            marker=dict(
                color=df["conversion_rate_app_to_install_pct"],
                colorscale="Blues",
                showscale=False,
            ),
        )
    )

    fig.update_layout(
        title="Conversion Rate by State",
        xaxis_title="App → Installation Rate (%)",
        yaxis_title="State",
        height=600,
        template="plotly_white",
        margin=dict(l=150),
    )

    return fig


def create_district_heatmap(district_data_df):
    """
    Create district adoption heatmap by state.

    Args:
        district_data_df (pd.DataFrame): District data with applications

    Returns:
        go.Figure: Plotly figure object
    """

    # Aggregate by state
    state_summary = (
        district_data_df.groupby("state")
        .agg({"application_status": "sum", "installation": "sum"})
        .reset_index()
    )

    state_summary["conversion_rate"] = (
        state_summary["installation"] / state_summary["application_status"] * 100
    )

    state_summary = state_summary.sort_values("conversion_rate", ascending=False)

    fig = px.bar(
        state_summary,
        x="state",
        y="conversion_rate",
        title="Conversion Rate by State",
        labels={"conversion_rate": "App → Installation (%)", "state": "State"},
        color="conversion_rate",
        color_continuous_scale="Viridis",
    )

    fig.update_layout(height=500, xaxis_tickangle=-45, margin=dict(b=100))

    return fig
