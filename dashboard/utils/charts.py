"""
Chart Creation Utilities
========================
Reusable charting functions for visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def filter_all_zero_rows(df, metric_cols):
    """
    Remove rows where all metric columns are zero.

    Args:
        df (pd.DataFrame): Source data.
        metric_cols (list[str]): Numeric columns to evaluate.

    Returns:
        pd.DataFrame: Filtered data.
    """

    metrics = df[metric_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    all_zero = (metrics == 0).all(axis=1)
    return df.loc[~all_zero].copy()


def create_adoption_trend(datewise_df, start_date=None, end_date=None):
    """
    Create cumulative adoption trend chart.

    Args:
        datewise_df (pd.DataFrame): Datewise data with date and adoption metrics

    Returns:
        go.Figure: Plotly figure object
    """

    # Prepare data
    df = datewise_df[["rptdate", "applications", "installations"]].copy()
    # Ensure rptdate is datetime
    df["rptdate"] = pd.to_datetime(df["rptdate"], errors="coerce")
    if start_date is not None:
        df = df[df["rptdate"] >= pd.to_datetime(start_date)]
    if end_date is not None:
        df = df[df["rptdate"] <= pd.to_datetime(end_date)]
    df = filter_all_zero_rows(df, ["applications", "installations"])
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

    # Improve axis labels and hover formatting
    fig.update_traces(hovertemplate="%{y:,} <br>%{x|%Y-%m-%d}")
    fig.update_layout(
        title="Cumulative applications submitted and installations completed over time",
        xaxis_title="Report date",
        yaxis_title="Cumulative applications / installations",
        hovermode="x unified",
        height=500,
        template="plotly_white",
        legend=dict(title="Metric", x=0.01, y=0.99),
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

    df = state_data_df[["state", "applications", "installations"]].copy()
    df = filter_all_zero_rows(df, ["applications", "installations"])

    # Create grouped bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["state"],
            y=df["applications"],
            name="Applications submitted",
            marker_color="#1f77b4",
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["state"],
            y=df["installations"],
            name="Installations completed",
            marker_color="#ff7f0e",
        )
    )

    fig.update_traces(hovertemplate="%{y:,} ")
    fig.update_layout(
        title="Applications submitted and installations completed by state",
        xaxis_title="State",
        yaxis_title="Applications / installations (count)",
        barmode="group",
        height=500,
        template="plotly_white",
        xaxis_tickangle=-45,
        margin=dict(b=100),
        legend=dict(title="Metric", x=0.01, y=0.99),
    )

    return fig


def create_state_scatter_chart(state_data_df):
    """
    Create a state scatter chart for volume versus conversion.

    Args:
        state_data_df (pd.DataFrame): State data with applications, installations,
            conversion rate, and subsidy redeemed amount.

    Returns:
        go.Figure: Plotly figure object
    """

    df = state_data_df[
        [
            "state",
            "applications",
            "installations",
            "conversion_rate_app_to_install_pct",
            "subsidy_redeemed_amount",
        ]
    ].copy()
    df = filter_all_zero_rows(df, ["applications", "installations"])

    fig = px.scatter(
        df,
        x="applications",
        y="conversion_rate_app_to_install_pct",
        size="subsidy_redeemed_amount",
        color="conversion_rate_app_to_install_pct",
        hover_name="state",
        size_max=40,
        color_continuous_scale=["#ff7f0e", "#ffaa1f", "#ffcc66", "#1f77b4"],
    )

    fig.update_traces(
        hovertemplate=(
            "%{hovertext}<br>Applications: %{x:,}<br>"
            "Conversion: %{y:.1f}%<br>"
            "Subsidy redeemed: %{marker.size:,.0f}<extra></extra>"
        )
    )

    outlier_df = df.sort_values(
        ["conversion_rate_app_to_install_pct", "applications"], ascending=[True, False]
    ).head(3)
    for _, row in outlier_df.iterrows():
        fig.add_annotation(
            x=row["applications"],
            y=row["conversion_rate_app_to_install_pct"],
            text=row["state"],
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            ax=24,
            ay=-24,
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor="#999999",
            borderwidth=1,
            font=dict(size=10),
        )

    fig.update_layout(
        title="State volume versus application-to-installation conversion",
        xaxis_title="Applications submitted",
        yaxis_title="Application to installation rate (%)",
        height=500,
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        coloraxis_colorbar=dict(title="Conversion rate (%)"),
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

    df = state_data_df[
        ["state", "applications", "installations", "conversion_rate_app_to_install_pct"]
    ].copy()
    df = filter_all_zero_rows(df, ["applications", "installations"])
    df = df.sort_values("conversion_rate_app_to_install_pct", ascending=True)

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

    fig.update_traces(hovertemplate="%{x:.1f}%")
    fig.update_layout(
        title="Application-to-installation conversion rate by state",
        xaxis_title="Conversion rate (%)",
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
    base_df = district_data_df[["state", "application_status", "installation"]].copy()
    base_df = filter_all_zero_rows(base_df, ["application_status", "installation"])
    state_summary = (
        base_df.groupby("state")
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
        title="Application-to-installation conversion rate by state",
        labels={
            "conversion_rate": "Application to installation rate (%)",
            "state": "State",
        },
        color="conversion_rate",
        color_continuous_scale="Viridis",
    )

    fig.update_traces(hovertemplate="%{y:.1f}%")
    fig.update_layout(height=500, xaxis_tickangle=-45, margin=dict(b=100))

    return fig
