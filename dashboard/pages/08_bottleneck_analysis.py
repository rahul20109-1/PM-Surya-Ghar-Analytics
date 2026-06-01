"""
Bottleneck Analysis - Identify Where Applications Get Stuck
============================================================
Advanced analytics to identify process bottlenecks and improvement opportunities.

Author: Analytics Team
Date: March 15, 2026
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add parent directory to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dashboard.utils.data_loader import load_data, apply_date_range_filter
from dashboard.utils.charts import filter_all_zero_rows
from dashboard.utils.components import chart_caption, how_to_read_chart

# Page configuration is set centrally in `dashboard/streamlit_app.py`.
# Avoid calling `st.set_page_config` here to prevent duplicate page title
# showing in the sidebar when this page is executed via `runpy.run_path`.


# Load data
@st.cache_data
def get_data():
    return load_data()


try:
    kpi_national, kpi_state, kpi_district, datewise, state_master, district = get_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()


# Custom styling
st.markdown(
    """
<style>
    .critical { color: #d62728; font-weight: bold; }
    .warning { color: #ff7f0e; font-weight: bold; }
    .success { color: #2ca02c; font-weight: bold; }
    .insight-box {
        background-color: #f0f7ff;
        border-left: 4px solid #1f77b4;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.header("Process bottlenecks: where applications stall")
st.markdown(
    """
This page synthesizes the process diagnostics we can extract from the cleaned scheme data.
It shows where applications are lost, where they accumulate in backlog, and which states exhibit the most pronounced operational friction.

Use the section-by-section analysis below to understand the full funnel, compare state-level performance, and judge how backlog pressure is evolving over time.
"""
)
st.caption(
    "Data scope note: Stages shown reflect process steps available in the dataset: application submission, vendor selection, installation completed, project inspection by DISCOM, and subsidy redeem."
)

st.markdown("---")

# ============================================================================
# SECTION 1: FUNNEL STAGE ANALYSIS
# ============================================================================

st.header("1. Stage-by-stage drop-off")

# Calculate funnel metrics (feasibility approval stage removed — not used for operational diagnostics)
funnel_stages = {
    "Stage": [
        "Application submission",
        "Vendor selection",
        "Installation completed",
        "Project inspection by DISCOM",
        "Subsidy redeem",
    ],
    "Count": [
        state_master["application_status"].sum(),
        state_master["vendor_selected"].sum(),
        state_master["installation"].sum(),
        state_master["inspection_approved"].sum(),
        state_master["total_redeem"].sum(),
    ],
}

# Calculate metrics
funnel_df = pd.DataFrame(funnel_stages)
funnel_df["Cumulative %"] = (
    funnel_df["Count"] / funnel_df["Count"].iloc[0] * 100
).round(2)
funnel_df["Stage Dropout %"] = 0.0
funnel_df["Loss Count"] = 0

for i in range(1, len(funnel_df)):
    loss = funnel_df["Count"].iloc[i - 1] - funnel_df["Count"].iloc[i]
    funnel_df.loc[i, "Loss Count"] = loss
    funnel_df.loc[i, "Stage Dropout %"] = (
        loss / funnel_df["Count"].iloc[i - 1] * 100
    ).round(2)

# Display metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Applications submitted", f"{int(funnel_df['Count'].iloc[0]):,}", delta=None
    )

with col2:
    successful = funnel_df["Count"].iloc[-1]
    success_rate = successful / funnel_df["Count"].iloc[0] * 100
    st.metric(
        "Reached final stage",
        f"{int(successful):,}",
        delta=None,
    )

with col3:
    total_pending = funnel_df["Count"].iloc[0] - funnel_df["Count"].iloc[-1]
    st.metric(
        "Still in process",
        f"{int(total_pending):,}",
        delta=None,
    )

with col4:
    worst_stage_idx = funnel_df["Stage Dropout %"].idxmax()
    worst_dropout = funnel_df["Stage Dropout %"].max()
    worst_stage = funnel_df["Stage"].iloc[worst_stage_idx]
    prev_stage = (
        funnel_df["Stage"].iloc[worst_stage_idx - 1]
        if worst_stage_idx > 0
        else worst_stage
    )
    worst_loss = funnel_df["Loss Count"].iloc[worst_stage_idx]
    st.metric(
        "Largest drop-off stage",
        worst_stage,
        delta=None,
    )

st.caption(
    "Summary: "
    f"{success_rate:.1f}% reached subsidy redeem stage, "
    f"{(total_pending / funnel_df['Count'].iloc[0] * 100):.1f}% remain in process, "
    f"largest stage drop is {worst_dropout:.1f}% between {prev_stage} and {worst_stage}."
)

st.markdown("---")

# Display funnel table
st.subheader("Stage breakdown table")

display_df = funnel_df.copy()
display_df = display_df.rename(
    columns={
        "Count": "Applications at stage (count)",
        "Cumulative %": "Cumulative share from submission (%)",
        "Stage Dropout %": "Drop-off from previous stage (%)",
        "Loss Count": "Applications lost at handoff (count)",
    }
)
display_df["Applications at stage (count)"] = display_df[
    "Applications at stage (count)"
].apply(lambda x: f"{int(x):,}")
display_df["Applications lost at handoff (count)"] = display_df[
    "Applications lost at handoff (count)"
].apply(
    lambda x: f"{int(x):,}" if x > 0 else "-"
)

st.dataframe(display_df, width="stretch", hide_index=True)
st.markdown("**How to read this table**")
st.markdown(
    "- Compare stage counts and drop-off percentages together: high count loss with high percentage loss indicates a priority handoff."
)
st.markdown(
    "- Cumulative share shows what proportion of original applications survives through each stage."
)

# Funnel visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Stage funnel chart")

    funnel_chart_df = filter_all_zero_rows(
        funnel_df[["Stage", "Count", "Cumulative %"]].copy(), ["Count"]
    )
    if funnel_chart_df.empty:
        st.info("No non-zero stage data available for this chart.")
    else:
        fig = go.Figure(
            go.Funnel(
                y=funnel_chart_df["Stage"],
                x=funnel_chart_df["Count"],
                marker=dict(
                    color=[
                        "#1f77b4",
                        "#1f77b4",
                        "#ff7f0e",
                        "#ff7f0e",
                        "#d62728",
                        "#2ca02c",
                    ]
                ),
                text=[
                    f"{count:,}<br>({pct:.1f}%)"
                    for count, pct in zip(
                        funnel_chart_df["Count"], funnel_chart_df["Cumulative %"]
                    )
                ],
                textposition="inside",
            )
        )

        fig.update_traces(hovertemplate="%{x:,} applications – %{y}")
        fig.update_layout(
            title="Stage funnel counts and cumulative share from submission",
            height=520,
            template="plotly_white",
        )
        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "Each funnel step represents the count of applications that reached that stage.",
                "The shape narrows as applications drop out across the process.",
                "Use steep narrowing points to identify operational handoffs that need intervention.",
            ]
        )
        chart_caption(
            "Funnel counts show how many applications reach each tracked stage",
            "",
        )

with col2:
    st.subheader("Drop-off rate between stages")

    # Remove first stage (no prior stage)
    dropout_data = funnel_df.iloc[1:][["Stage", "Stage Dropout %"]].copy()
    dropout_data = filter_all_zero_rows(dropout_data, ["Stage Dropout %"])

    if dropout_data.empty:
        st.info("No non-zero drop-off data available for this chart.")
    else:
        fig = px.bar(
            dropout_data,
            x="Stage",
            y="Stage Dropout %",
            title="Drop-off rate by stage",
            color="Stage Dropout %",
            color_continuous_scale=["#2ca02c", "#ff7f0e", "#d62728"],
            text="Stage Dropout %",
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            hovertemplate="%{y:.1f}% dropout – %{x}",
        )
        fig.update_layout(
            height=500,
            showlegend=False,
            xaxis_tickangle=-45,
            xaxis_title="Stage",
            yaxis_title="Drop-off (%)",
        )
        fig.update_xaxes(tickfont=dict(size=10))
        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "Bars show percentage drop relative to the immediately previous stage.",
                "Higher bars indicate weaker handoff quality and larger proportional loss.",
                "Prioritise stages where high percentage drop combines with high absolute volume.",
            ]
        )
        chart_caption(
            "Bars show the percent lost between adjacent funnel stages",
            "",
        )

# Critical insight
st.markdown(
    """
<div class="insight-box">
<strong>Key insight:</strong> The largest operational loss occurs between <strong>{}</strong> and <strong>{}</strong>, where the process sheds <strong>{pct:.1f}%</strong> of volume from the prior stage. That translates to roughly <strong>{loss:,}</strong> applications not advancing at this handoff.
<br><em>Implication:</em> This is the clearest pressure point in the funnel and should be treated as the first intervention target.
</div>
""".format(prev_stage, worst_stage, pct=worst_dropout, loss=int(worst_loss)),
    unsafe_allow_html=True,
)

st.markdown("---")

# ============================================================================
# SECTION 2: PENDING APPLICATIONS ANALYSIS
# ============================================================================

st.header("2. Where applications wait")

# Calculate pending at each stage
pending_analysis = {"Stage": [], "Applications": [], "Pending": [], "Pending %": []}

# Stages to check for pending/backlog comparisons (feasibility removed)
stages_to_check = [
    ("Vendor selection", "application_status", "vendor_selected"),
    ("Installation completed", "vendor_selected", "installation"),
    ("Project inspection by DISCOM", "installation", "inspection_approved"),
    ("Subsidy redeem", "inspection_approved", "total_redeem"),
]

for stage_name, prev_col, curr_col in stages_to_check:
    prev_count = state_master[prev_col].sum()
    curr_count = state_master[curr_col].sum()
    pending = prev_count - curr_count
    pending_pct = (pending / prev_count * 100) if prev_count > 0 else 0

    pending_analysis["Stage"].append(stage_name)
    pending_analysis["Applications"].append(prev_count)
    pending_analysis["Pending"].append(pending)
    pending_analysis["Pending %"].append(pending_pct)

pending_df = pd.DataFrame(pending_analysis)
pending_df = pending_df.sort_values("Pending", ascending=False)

# Display pending metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total applications currently waiting",
        f"{int(pending_df['Pending'].sum()):,}",
        f"of {int(pending_df['Applications'].iloc[0]):,} total received",
    )

with col2:
    highest_pending_stage = pending_df.iloc[0]
    st.metric(
        "Stage with the most pending applications",
        highest_pending_stage["Stage"],
        f"{int(highest_pending_stage['Pending']):,} applications waiting",
    )

with col3:
    highest_pending_pct = pending_df["Pending %"].max()
    st.metric(
        "Largest waiting share",
        f"{highest_pending_pct:.1f}%",
        "Share of applications pending at this stage",
    )

st.markdown("---")

# Pending visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Applications waiting at each stage")
    pending_chart_df = pending_df[["Stage", "Pending", "Pending %"]].copy()
    pending_chart_df = filter_all_zero_rows(pending_chart_df, ["Pending", "Pending %"])

    if pending_chart_df.empty:
        st.info("No non-zero waiting data available for this chart.")
    else:
        fig = px.bar(
            pending_chart_df.sort_values("Pending", ascending=True),
            y="Stage",
            x="Pending",
            orientation="h",
            title="Applications waiting by stage",
            color="Pending %",
            color_continuous_scale=["#2ca02c", "#ff7f0e", "#d62728"],
            text="Pending",
        )

        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            hovertemplate="%{x:,.0f} applications waiting – %{y}",
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Applications waiting",
            yaxis_title="Stage",
        )
        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "Each horizontal bar shows how many applications are currently waiting at that stage.",
                "Longer bars represent larger operational backlogs.",
                "Use this chart to prioritize stages for queue-clearing actions.",
            ]
        )
        chart_caption(
            "Pending counts identify the stage where applications accumulate",
            "",
        )

with col2:
    st.subheader("Waiting share by stage")

    if pending_chart_df.empty:
        st.info("No non-zero waiting share data available for this chart.")
    else:
        fig = px.bar(
            pending_chart_df.sort_values("Pending %", ascending=True),
            y="Stage",
            x="Pending %",
            orientation="h",
            title="Waiting share by stage",
            color="Pending %",
            color_continuous_scale=["#2ca02c", "#ff7f0e", "#d62728"],
            text="Pending %",
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            hovertemplate="%{x:.1f}% waiting – %{y}",
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Waiting share (%)",
            yaxis_title="Stage",
        )
        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "This view normalizes backlog by stage volume using percentages.",
                "A high waiting share means a larger fraction of incoming applications is stalled.",
                "Compare this with absolute waiting counts to avoid over-prioritizing low-volume stages.",
            ]
        )
        chart_caption(
            "Waiting share shows where backlog is largest relative to volume entering the stage",
            "",
        )

st.markdown("---")

# ============================================================================
# SECTION 3: GEOGRAPHIC BOTTLENECK ANALYSIS
# ============================================================================

# Section: State comparison
st.header("3. State comparison")

# Brief explanation and interpretation guidance for users
st.markdown(
    """
**Decision use:** Compare states across three operational risk patterns: low application-to-installation conversion, high waiting share, and low installation completion.

- Select the issue lens based on policy priority and intervention objective.
- Low conversion indicates weak end-to-end execution, high waiting share indicates queue stress, and low installation completion indicates post-vendor execution constraints.
- Start with the highest-risk states, then validate root causes through district and process-level diagnostics.
""",
    unsafe_allow_html=True,
)

# Calculate state-level conversion metrics
state_analysis = (
    state_master.groupby("state")
    .agg(
        {
            "application_status": "sum",
            "vendor_selected": "sum",
            "installation": "sum",
            "inspection_approved": "sum",
            "total_redeem": "sum",
        }
    )
    .reset_index()
)

state_analysis.columns = [
    "state",
    "applications",
    "vendor_sel",
    "installation",
    "inspection",
    "subsidy_redeemed",
]

# Calculate conversion rates
state_analysis["app_to_install_rate"] = (
    state_analysis["installation"] / state_analysis["applications"] * 100
).round(2)
state_analysis["app_to_subsidy_rate"] = (
    state_analysis["subsidy_redeemed"] / state_analysis["applications"] * 100
).round(2)
state_analysis["install_completion_rate"] = (
    state_analysis["installation"] / state_analysis["vendor_sel"] * 100
).round(2)

# Sort by conversion rate (worst first)
state_analysis_sorted = state_analysis.sort_values("app_to_install_rate")

# Display filters
col1, col2 = st.columns(2)

with col1:
    issue_type = st.radio(
        "Show states by:",
        [
            "Lowest application to installation rate",
            "Highest waiting share",
            "Lowest installation completion rate",
        ],
        horizontal=True,
        help="Choose which state-level bottleneck is shown first.",
    )

with col2:
    top_n = st.slider(
        "Number of states to show:",
        5,
        36,
        15,
        help="Limit the list to the most important states for the selected issue.",
    )

selected_focus_states = st.multiselect(
    "Focus specific states",
    sorted(state_analysis["state"].unique()),
    help="Pick one or more states to compare directly. Leave empty to use the ranked top states view.",
)

# Prepare display data
if issue_type == "Lowest application to installation rate":
    display_df = state_analysis_sorted.head(top_n)
    metric_col = "app_to_install_rate"
    metric_name = "Application-to-installation conversion rate"
elif issue_type == "Highest waiting share":
    state_analysis["pending_pct"] = (
        (state_analysis["applications"] - state_analysis["subsidy_redeemed"])
        / state_analysis["applications"]
        * 100
    ).round(2)
    display_df = state_analysis.nlargest(top_n, "pending_pct")
    metric_col = "pending_pct"
    metric_name = "Waiting share"
else:
    display_df = state_analysis.nsmallest(top_n, "install_completion_rate")
    metric_col = "install_completion_rate"
    metric_name = "Installation completion rate"

if selected_focus_states:
    display_df = state_analysis[state_analysis["state"].isin(selected_focus_states)].copy()
    display_df = display_df.sort_values(metric_col)

if selected_focus_states:
    st.subheader("Selected states comparison")
    st.caption(f"Focused comparison for {len(selected_focus_states)} selected state(s).")
else:
    st.subheader(f"Top {top_n} states by selected issue")

# Display table
table_df = display_df[
    ["state", "applications", "installation", "subsidy_redeemed", metric_col]
].copy()
table_df.columns = [
    "State",
    "Applications submitted (count)",
    "Installations completed (count)",
    "Subsidy redeemed (count)",
    f"{metric_name} (%)",
]
table_df["Applications submitted (count)"] = table_df[
    "Applications submitted (count)"
].apply(lambda x: f"{int(x):,}")
table_df["Installations completed (count)"] = table_df[
    "Installations completed (count)"
].apply(lambda x: f"{int(x):,}")
table_df["Subsidy redeemed (count)"] = table_df["Subsidy redeemed (count)"].apply(
    lambda x: f"{int(x):,}"
)
table_df[f"{metric_name} (%)"] = table_df[f"{metric_name} (%)"].apply(
    lambda x: f"{x:.1f}%"
)

st.dataframe(table_df, width="stretch", hide_index=True)
st.caption(
    "Tip: Sort by any column to align action sequencing with policy priorities and operational risk."
)
# Source caption removed per UI guidance

if selected_focus_states:
    st.caption(f"Focused comparison for {len(selected_focus_states)} selected states.")

st.markdown("---")

# ============================================================================
# SECTION 4: TIME-BASED BOTTLENECK ANALYSIS
# ============================================================================

st.header("4. Processing speed over time")

col1, col2 = st.columns(2)

with col1:
    st.subheader("4.1 7-day average applications and installations over time")
    st.markdown("**Date range**")
    throughput_datewise, throughput_start_date, throughput_end_date = apply_date_range_filter(
        datewise, "bottleneck_throughput"
    )
    if throughput_start_date and throughput_end_date:
        st.caption(f"Showing: {throughput_start_date} to {throughput_end_date}")

    if throughput_datewise.empty:
        st.info("No time-series data available for the selected range.")
        avg_daily_apps = 0.0
        avg_daily_installs = 0.0
        daily_deficit = 0.0
        latest_gap = 0.0
        clearance_line = "No time-series data available for the selected range."
    else:
        throughput_df = throughput_datewise[["rptdate", "applications", "installations"]].copy()
        throughput_df = filter_all_zero_rows(throughput_df, ["applications", "installations"])
        throughput_analysis = throughput_df.sort_values("rptdate")
        throughput_analysis["rptdate"] = pd.to_datetime(throughput_analysis["rptdate"])

        throughput_analysis["apps_7d_avg"] = throughput_analysis["applications"].rolling(window=7, min_periods=1).mean()
        throughput_analysis["installs_7d_avg"] = throughput_analysis["installations"].rolling(window=7, min_periods=1).mean()
        throughput_analysis["cumulative_gap"] = throughput_analysis["applications"].cumsum() - throughput_analysis["installations"].cumsum()

        avg_daily_apps = throughput_analysis["applications"].mean()
        avg_daily_installs = throughput_analysis["installations"].mean()
        daily_deficit = avg_daily_apps - avg_daily_installs
        latest_gap = throughput_analysis["cumulative_gap"].iloc[-1]

        if daily_deficit > 0:
            years_to_clear = latest_gap / daily_deficit / 365
            clearance_line = f"At the current rate, it will take about {years_to_clear:.1f} years to clear the backlog."
        else:
            clearance_line = "At the current rate, backlog is not growing; clearance timing cannot be estimated."

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=throughput_analysis["rptdate"],
                y=throughput_analysis["apps_7d_avg"],
                name="Applications (7-day avg)",
                mode="lines",
                line=dict(color="#1f77b4", width=2),
                hovertemplate="%{y:,.0f} applications - %{x|%Y-%m-%d}",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=throughput_analysis["rptdate"],
                y=throughput_analysis["installs_7d_avg"],
                name="Installations (7-day avg)",
                mode="lines",
                line=dict(color="#2ca02c", width=2),
                hovertemplate="%{y:,.0f} installations - %{x|%Y-%m-%d}",
            )
        )
        fig.update_layout(
            height=400,
            hovermode="x unified",
            template="plotly_white",
            yaxis_title="Daily applications / installations (7-day average)",
            xaxis_title="Report date",
            legend=dict(title="Metric", x=0.01, y=0.99),
        )

        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "Both lines are 7-day averages, which reduce day-to-day noise.",
                "If the applications line stays above installations, queue pressure is building.",
                "Converging lines indicate improving operational balance.",
            ]
        )
        chart_caption(
            "7-day averages smooth the daily throughput series",
            "",
            "The selected date range controls the window shown here.",
        )

with col2:
    st.subheader("4.2 Backlog growth over time")
    st.markdown("**Date range**")
    backlog_datewise, backlog_start_date, backlog_end_date = apply_date_range_filter(
        datewise, "bottleneck_backlog"
    )
    if backlog_start_date and backlog_end_date:
        st.caption(f"Showing: {backlog_start_date} to {backlog_end_date}")

    if backlog_datewise.empty:
        st.info("No time-series data available for the selected range.")
    else:
        backlog_df = backlog_datewise[["rptdate", "applications", "installations"]].copy()
        backlog_df = filter_all_zero_rows(backlog_df, ["applications", "installations"])
        backlog_analysis = backlog_df.sort_values("rptdate")
        backlog_analysis["rptdate"] = pd.to_datetime(backlog_analysis["rptdate"])
        backlog_analysis["cumulative_gap"] = backlog_analysis["applications"].cumsum() - backlog_analysis["installations"].cumsum()

        backlog_latest_gap = backlog_analysis["cumulative_gap"].iloc[-1]
        backlog_avg_daily_apps = backlog_analysis["applications"].mean()
        backlog_avg_daily_installs = backlog_analysis["installations"].mean()
        backlog_daily_deficit = backlog_avg_daily_apps - backlog_avg_daily_installs

        if backlog_daily_deficit > 0:
            backlog_years_to_clear = backlog_latest_gap / backlog_daily_deficit / 365
            backlog_clearance_line = (
                f"At the current rate, it will take about {backlog_years_to_clear:.1f} years to clear the backlog."
            )
        else:
            backlog_clearance_line = (
                "At the current rate, backlog is not growing; clearance timing cannot be estimated."
            )

        if backlog_latest_gap > 0 and backlog_daily_deficit != 0:
            backlog_scenario_rows = [
                {
                    "Scenario": "Current pace",
                    "Daily intake": f"{backlog_avg_daily_apps:,.0f}",
                    "Daily installations": f"{backlog_avg_daily_installs:,.0f}",
                    "Daily deficit": f"{backlog_daily_deficit:,.0f}",
                    "Years to clear": f"{(backlog_latest_gap / backlog_daily_deficit / 365):.1f}" if backlog_daily_deficit > 0 else "Not growing",
                },
                {
                    "Scenario": "+25% capacity",
                    "Daily intake": f"{backlog_avg_daily_apps:,.0f}",
                    "Daily installations": f"{backlog_avg_daily_installs * 1.25:,.0f}",
                    "Daily deficit": f"{(backlog_avg_daily_apps - backlog_avg_daily_installs * 1.25):,.0f}",
                    "Years to clear": f"{(backlog_latest_gap / (backlog_avg_daily_apps - backlog_avg_daily_installs * 1.25) / 365):.1f}"
                    if (backlog_avg_daily_apps - backlog_avg_daily_installs * 1.25) > 0
                    else "No backlog growth",
                },
                {
                    "Scenario": "-25% intake",
                    "Daily intake": f"{backlog_avg_daily_apps * 0.75:,.0f}",
                    "Daily installations": f"{backlog_avg_daily_installs:,.0f}",
                    "Daily deficit": f"{(backlog_avg_daily_apps * 0.75 - backlog_avg_daily_installs):,.0f}",
                    "Years to clear": f"{(backlog_latest_gap / (backlog_avg_daily_apps * 0.75 - backlog_avg_daily_installs) / 365):.1f}"
                    if (backlog_avg_daily_apps * 0.75 - backlog_avg_daily_installs) > 0
                    else "No backlog growth",
                },
            ]
        else:
            backlog_scenario_rows = [
                {
                    "Scenario": "Current pace",
                    "Daily intake": f"{backlog_avg_daily_apps:,.0f}",
                    "Daily installations": f"{backlog_avg_daily_installs:,.0f}",
                    "Daily deficit": f"{backlog_daily_deficit:,.0f}",
                    "Years to clear": "Not applicable",
                },
                {
                    "Scenario": "+25% capacity",
                    "Daily intake": f"{backlog_avg_daily_apps:,.0f}",
                    "Daily installations": f"{backlog_avg_daily_installs * 1.25:,.0f}",
                    "Daily deficit": f"{(backlog_avg_daily_apps - backlog_avg_daily_installs * 1.25):,.0f}",
                    "Years to clear": "Not applicable",
                },
                {
                    "Scenario": "-25% intake",
                    "Daily intake": f"{backlog_avg_daily_apps * 0.75:,.0f}",
                    "Daily installations": f"{backlog_avg_daily_installs:,.0f}",
                    "Daily deficit": f"{(backlog_avg_daily_apps * 0.75 - backlog_avg_daily_installs):,.0f}",
                    "Years to clear": "Not applicable",
                },
            ]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=backlog_analysis["rptdate"],
                y=backlog_analysis["cumulative_gap"],
                name="Backlog (cumulative)",
                mode="lines",
                fill="tozeroy",
                line=dict(color="#d62728", width=2),
                hovertemplate="%{y:,.0f} pending applications - %{x|%Y-%m-%d}",
            )
        )
        fig.update_layout(
            height=400,
            hovermode="x",
            template="plotly_white",
            yaxis_title="Cumulative pending applications",
            xaxis_title="Report date",
            legend=dict(title="Metric", x=0.01, y=0.99),
        )

        latest_backlog = backlog_analysis["cumulative_gap"].iloc[-1]
        latest_backlog_date = backlog_analysis["rptdate"].iloc[-1]
        fig.add_annotation(
            x=latest_backlog_date,
            y=latest_backlog,
            text=f"Current backlog: {int(latest_backlog):,}",
            showarrow=True,
            arrowhead=2,
            ax=-40,
            ay=-40,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#d62728",
            borderwidth=1,
        )

        st.plotly_chart(fig, width="stretch")
        st.subheader("Backlog clearance scenarios")
        how_to_read_chart(
            [
                "The line shows cumulative difference between applications submitted and installations completed.",
                "An upward slope means backlog growth, while a flattening slope means improving clearance.",
                "The annotation marks the latest backlog value in the selected period.",
            ]
        )
        scenario_df = pd.DataFrame(backlog_scenario_rows).rename(
            columns={
                "Daily intake": "Daily applications submitted (count)",
                "Daily installations": "Daily installations completed (count)",
                "Daily deficit": "Daily backlog change (count)",
                "Years to clear": "Estimated years to clear backlog",
            }
        )
        st.dataframe(scenario_df, width="stretch", hide_index=True)
        st.markdown("**How to read this table**")
        st.markdown(
            "- Compare scenarios by daily backlog change (count): negative or near-zero values indicate improved control of backlog growth."
        )
        st.markdown(
            "- Estimated years to clear backlog is directional and assumes each scenario remains stable over time."
        )
        st.caption(
            "Scenarios compare current flow with a 25% capacity increase and a 25% intake reduction to estimate potential backlog stabilization paths."
        )
        chart_caption(
            "Backlog line shows how the application gap accumulates over time",
            "",
            "Filtered to the selected date range.",
        )

    st.markdown(
        f"""
    <div class="insight-box">
    <strong>Decision summary:</strong><br>
    - Applications received per day: <strong>{avg_daily_apps:,.0f}</strong><br>
    - Installations completed per day: <strong>{avg_daily_installs:,.0f}</strong><br>
    - Backlog grows by: <strong class="critical">{daily_deficit:,.0f} applications per day</strong><br>
    - Current total backlog: <strong class="critical">{int(latest_gap):,} applications</strong><br>
    <br>
    <strong>{clearance_line}</strong>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================================================
# SECTION 5: ACTIONABLE RECOMMENDATIONS
# ============================================================================

st.header("5. Recommended interventions")

recommendations = [
    {
        "priority": "High",
        "issue": f"Gap between {prev_stage} and {worst_stage}",
        "impact": f"{int(worst_loss):,} applications do not move forward here",
        "action": "Review stage handoff controls, vendor capacity, and local process delays.",
        "timeline": "Immediate (1-2 weeks)",
    },
    {
        "priority": "High",
        "issue": "Backlog is growing",
        "impact": f"{int(latest_gap):,} applications are still waiting, and the backlog grows by {daily_deficit:,.0f} per day",
        "action": "Increase processing capacity or moderate intake until throughput stabilizes.",
        "timeline": "Immediate (1-2 weeks)",
    },
    {
        "priority": "Medium",
        "issue": "Geographic Hotspots",
        "impact": f'{len(state_analysis_sorted[state_analysis_sorted["app_to_install_rate"] < 20])} states have an application to installation rate below 20%',
        "action": "Deploy targeted implementation support in weak states and benchmark against stronger peers.",
        "timeline": "Short-term (1-3 months)",
    },
    {
        "priority": "Medium",
        "issue": "Vendor selection variability",
        "impact": "Vendor selection rates and criteria vary across states; investigate vendor onboarding and selection rules.",
        "action": "Review vendor onboarding and selection controls; standardize where feasible.",
        "timeline": "Short-term (1-3 months)",
    },
    {
        "priority": "Medium",
        "issue": "Project inspection bottleneck",
        "impact": f'{int(state_master["installation"].sum() - state_master["inspection_approved"].sum()):,} installations are still waiting for project inspection approval',
        "action": "Accelerate inspection scheduling and add inspection capacity in high-delay locations.",
        "timeline": "Medium-term (1-2 months)",
    },
]

for i, rec in enumerate(recommendations, 1):
    st.markdown(
        f"""
    <div style='background-color: #f8f9fa; border-left: 4px solid #ff7f0e; padding: 15px; margin: 15px 0; border-radius: 5px;'>
    <strong>{rec['priority']} Priority Action #{i}: {rec['issue']}</strong><br>
    <strong>Impact:</strong> {rec['impact']}<br>
    <strong>Action:</strong> {rec['action']}<br>
    <strong>Timeline:</strong> {rec['timeline']}
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

st.markdown(
    f"""
### Executive summary

The analysis points to a clear operational bottleneck between **{prev_stage}** and **{worst_stage}**, where the largest volume of applications falls out of the process.
Backlog pressure is still building, with intake exceeding clearance by roughly **{daily_deficit:,.0f}** applications per day.

State performance is uneven, which means the same process weakness is not being experienced uniformly across geographies.
The practical response is to prioritise the highest-volume weak states, tighten the handoff at the largest loss point, and add short-term throughput support where the backlog is most exposed.
"""
)
