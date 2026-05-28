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
from dashboard.utils.components import chart_caption

# Configure page
st.set_page_config(page_title="Bottleneck Analysis", layout="wide")


# Load data
@st.cache_data
def get_data():
    return load_data()


try:
    kpi_national, kpi_state, kpi_district, datewise, state_master, district = get_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Date range selector for Bottleneck time analyses
st.markdown("**Date range (Bottleneck analysis)**")
filtered_datewise, start_dt, end_dt = apply_date_range_filter(datewise, "bottleneck")
if start_dt and end_dt:
    st.caption(f"Showing: {start_dt} ÔåÆ {end_dt}")

# Use filtered_datewise for time-based analyses below
if filtered_datewise is None or filtered_datewise.empty:
    st.warning("No time-series data available for selected date range. Time-based charts will be empty.")

# ============================================================================
# HEADER
# ============================================================================

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

st.title("Process bottlenecks ÔÇö where applications stall")
st.markdown(
    """
This analysis highlights stages where applications are delayed, dropped, or accumulate in backlog. Use it to prioritise operational interventions and state-level support.

The visualisations below show where the program loses applications (drop-off), where applications are waiting (backlog), and which states exhibit the largest issues.
"""
)
st.caption(
    "Data note: Stages shown reflect the steps captured in the dataset. Consumer registration, agreement upload, and subsidy disbursal are not recorded here."
)

st.markdown("---")

# ============================================================================
# SECTION 1: FUNNEL STAGE ANALYSIS
# ============================================================================

st.header("1. Stage-by-stage drop-off")

# Calculate funnel metrics
funnel_stages = {
    "Stage": [
        "Application submission",
        "Feasibility approval",
        "Vendor selection",
        "Installation completed",
        "Project inspection by DISCOM",
        "Subsidy redeem",
    ],
    "Count": [
        state_master["application_status"].sum(),
        state_master["feasibility_approved"].sum(),
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
        delta=f"{success_rate:.1f}% of applications reached the subsidy redeem stage",
    )

with col3:
    total_pending = funnel_df["Count"].iloc[0] - funnel_df["Count"].iloc[-1]
    st.metric(
        "Still in process",
        f"{int(total_pending):,}",
        delta=f"{(total_pending/funnel_df['Count'].iloc[0]*100):.1f}% of applications have not reached the final stage",
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
        delta=f"{worst_dropout:.1f}% drop from the previous stage",
    )

st.markdown("---")

# Display funnel table
st.subheader("Stage breakdown")

display_df = funnel_df.copy()
display_df["Count"] = display_df["Count"].apply(lambda x: f"{int(x):,}")
display_df["Loss Count"] = display_df["Loss Count"].apply(
    lambda x: f"{int(x):,}" if x > 0 else "-"
)

st.dataframe(display_df, width="stretch", hide_index=True)

# Funnel visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Stage flow chart")

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

        fig.update_traces(hovertemplate="%{x:,} applications ÔÇö %{y}")
        fig.update_layout(
            title="Stage flow (counts & cumulative%)",
            height=520,
            template="plotly_white",
        )
        st.plotly_chart(fig, width="stretch")
        chart_caption(
            "Funnel counts stage-by-stage drop-off from application submission to subsidy redeem",
            "Source: state_master_clean.csv columns application_status, feasibility_approved, vendor_selected, installation, inspection_approved, and total_redeem.",
        )

with col2:
    st.subheader("Drop-off rate by stage")

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
            hovertemplate="%{y:.1f}% dropout ÔÇö %{x}",
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
        chart_caption(
            "Bars show the percent lost between adjacent funnel stages",
            "Source: same stage counts from state_master_clean.csv.",
        )

# Critical insight
st.markdown(
    """
<div class="insight-box">
<strong>Key insight:</strong> The largest operational loss occurs between <strong>{}</strong> and <strong>{}</strong> ÔÇö a {pct:.1f}% reduction from the prior stage. Approximately <strong>{loss:,}</strong> applications do not progress at this handoff.
<br><em>Suggested next step:</em> Investigate handoff procedures, vendor capacity, and local queues in the affected states.
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

stages_to_check = [
    ("Feasibility approval", "application_status", "feasibility_approved"),
    ("Vendor selection", "feasibility_approved", "vendor_selected"),
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
            hovertemplate="%{x:,.0f} applications waiting ÔÇö %{y}",
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Applications waiting",
            yaxis_title="Stage",
        )
        st.plotly_chart(fig, width="stretch")
        chart_caption(
            "Pending counts identify the stage where applications accumulate",
            "Source: state_master_clean.csv stage totals compared between adjacent steps.",
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
            hovertemplate="%{x:.1f}% waiting ÔÇö %{y}",
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Waiting share (%)",
            yaxis_title="Stage",
        )
        st.plotly_chart(fig, width="stretch")
        chart_caption(
            "Waiting share shows where backlog is largest relative to volume entering the stage",
            "Source: pending counts derived from state_master_clean.csv.",
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
**What this table shows:** Compare states on three problem types: low applicationÔåÆinstallation conversion, high waiting share, and low installation completion.

- Use the selector to pick which issue to prioritise. Lower conversion rates indicate where applications are failing to reach installation. High waiting share signals backlog or hold-ups. Low installation completion suggests execution or capacity constraints after feasibility approval.
- Tip: Start with the top states in this list, then drill down into local workflow, vendor capacity, and inspection scheduling to find root causes.
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
            "feasibility_approved": "sum",
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
    "feasibility",
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
    state_analysis["installation"] / state_analysis["feasibility"] * 100
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

# Prepare display data
if issue_type == "Lowest application to installation rate":
    display_df = state_analysis_sorted.head(top_n)
    metric_col = "app_to_install_rate"
    metric_name = "Application to installation rate"
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

st.subheader(f"Top {top_n} states by selected issue")

# Display table
table_df = display_df[
    ["state", "applications", "installation", "subsidy_redeemed", metric_col]
].copy()
table_df.columns = [
    "State",
    "Applications",
    "Installations",
    "Subsidy Redeemed",
    metric_name,
]
table_df["Applications"] = table_df["Applications"].apply(lambda x: f"{int(x):,}")
table_df["Installations"] = table_df["Installations"].apply(lambda x: f"{int(x):,}")
table_df["Subsidy Redeemed"] = table_df["Subsidy Redeemed"].apply(
    lambda x: f"{int(x):,}"
)
table_df[metric_name] = table_df[metric_name].apply(lambda x: f"{x:.1f}%")

st.dataframe(table_df, width="stretch", hide_index=True)
st.caption(
    "Tip: Click column headers to sort. Use this list to prioritise on-the-ground support and to pick states for focused diagnostics."
)
st.caption(
    "Source: state_master_clean.csv aggregated to the state level and ranked by the selected issue."
)

st.markdown("---")

# ============================================================================
# SECTION 4: TIME-BASED BOTTLENECK ANALYSIS
# ============================================================================

st.header("4. Processing speed over time")

st.markdown("**Date range**")
filtered_datewise, start_date, end_date = apply_date_range_filter(
    datewise, "bottleneck_time"
)
if start_date and end_date:
    st.caption(f"Showing: {start_date} to {end_date}")

avg_daily_apps = 0.0
avg_daily_installs = 0.0
daily_deficit = 0.0
latest_gap = 0.0

if filtered_datewise.empty:
    st.info("No time-series data available for the selected range.")
else:
    # Analyze daily throughput
    throughput_df = filtered_datewise[["rptdate", "applications", "installations"]].copy()
    throughput_df = filter_all_zero_rows(
        throughput_df, ["applications", "installations"]
    )
    datewise_analysis = throughput_df.sort_values("rptdate")
    datewise_analysis["rptdate"] = pd.to_datetime(datewise_analysis["rptdate"])

    # Calculate rolling averages
    datewise_analysis["apps_7d_avg"] = (
        datewise_analysis["applications"].rolling(window=7, min_periods=1).mean()
    )
    datewise_analysis["installs_7d_avg"] = (
        datewise_analysis["installations"].rolling(window=7, min_periods=1).mean()
    )
    datewise_analysis["gap_7d"] = (
        datewise_analysis["apps_7d_avg"] - datewise_analysis["installs_7d_avg"]
    ).round(0)

    # Calculate backlog growth
    datewise_analysis["cumulative_gap"] = (
        datewise_analysis["applications"].cumsum()
        - datewise_analysis["installations"].cumsum()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("7-day average applications and installations")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=datewise_analysis["rptdate"],
                y=datewise_analysis["apps_7d_avg"],
                name="Applications (7-day avg)",
                mode="lines",
                line=dict(color="#1f77b4", width=2),
                hovertemplate="%{y:,.0f} applications - %{x|%Y-%m-%d}",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=datewise_analysis["rptdate"],
                y=datewise_analysis["installs_7d_avg"],
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
            yaxis_title="Daily count (7-day average)",
            xaxis_title="Date",
            legend=dict(title="Series", x=0.01, y=0.99),
        )

        st.plotly_chart(fig, width="stretch")
        chart_caption(
            "7-day averages smooth the daily throughput series",
            "Source: datewise_clean.csv columns applications and installations.",
            "The selected date range controls the window shown here.",
        )

    with col2:
        st.subheader("Backlog growth over time")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=datewise_analysis["rptdate"],
                y=datewise_analysis["cumulative_gap"],
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
            xaxis_title="Date",
            legend=dict(title="Series", x=0.01, y=0.99),
        )

        latest_backlog = datewise_analysis["cumulative_gap"].iloc[-1]
        latest_backlog_date = datewise_analysis["rptdate"].iloc[-1]
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
        chart_caption(
            "Backlog line shows how the application gap accumulates over time",
            "Source: datewise_clean.csv columns applications and installations.",
            "Filtered to the selected date range.",
        )

    # Throughput metrics
    latest_gap = datewise_analysis["cumulative_gap"].iloc[-1]
    avg_daily_apps = datewise_analysis["applications"].mean()
    avg_daily_installs = datewise_analysis["installations"].mean()
    daily_deficit = avg_daily_apps - avg_daily_installs

    if daily_deficit > 0:
        years_to_clear = latest_gap / daily_deficit / 365
        clearance_line = (
            f"At the current rate, it will take about {years_to_clear:.1f} years to clear the backlog."
        )
    else:
        clearance_line = (
            "At the current rate, backlog is not growing; clearance timing cannot be estimated."
        )

    st.markdown(
        f"""
    <div class="insight-box">
    <strong>Main finding:</strong><br>
    ÔÇó Applications received per day: <strong>{avg_daily_apps:,.0f}</strong><br>
    ÔÇó Installations completed per day: <strong>{avg_daily_installs:,.0f}</strong><br>
    ÔÇó Backlog grows by: <strong class="critical">{daily_deficit:,.0f} applications per day</strong><br>
    ÔÇó Current total backlog: <strong class="critical">{int(latest_gap):,} applications</strong><br>
    <br>
    <strong>{clearance_line}</strong>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Backlog clearance scenarios")
    if latest_gap > 0 and daily_deficit != 0:
        scenario_rows = [
            {
                "Scenario": "Current pace",
                "Daily intake": f"{avg_daily_apps:,.0f}",
                "Daily installations": f"{avg_daily_installs:,.0f}",
                "Daily deficit": f"{daily_deficit:,.0f}",
                "Years to clear": f"{(latest_gap / daily_deficit / 365):.1f}" if daily_deficit > 0 else "Not growing",
            },
            {
                "Scenario": "+25% capacity",
                "Daily intake": f"{avg_daily_apps:,.0f}",
                "Daily installations": f"{avg_daily_installs * 1.25:,.0f}",
                "Daily deficit": f"{(avg_daily_apps - avg_daily_installs * 1.25):,.0f}",
                "Years to clear": f"{(latest_gap / (avg_daily_apps - avg_daily_installs * 1.25) / 365):.1f}"
                if (avg_daily_apps - avg_daily_installs * 1.25) > 0
                else "No backlog growth",
            },
            {
                "Scenario": "-25% intake",
                "Daily intake": f"{avg_daily_apps * 0.75:,.0f}",
                "Daily installations": f"{avg_daily_installs:,.0f}",
                "Daily deficit": f"{(avg_daily_apps * 0.75 - avg_daily_installs):,.0f}",
                "Years to clear": f"{(latest_gap / (avg_daily_apps * 0.75 - avg_daily_installs) / 365):.1f}"
                if (avg_daily_apps * 0.75 - avg_daily_installs) > 0
                else "No backlog growth",
            },
        ]
    else:
        scenario_rows = [
            {
                "Scenario": "Current pace",
                "Daily intake": f"{avg_daily_apps:,.0f}",
                "Daily installations": f"{avg_daily_installs:,.0f}",
                "Daily deficit": f"{daily_deficit:,.0f}",
                "Years to clear": "Not applicable",
            },
            {
                "Scenario": "+25% capacity",
                "Daily intake": f"{avg_daily_apps:,.0f}",
                "Daily installations": f"{avg_daily_installs * 1.25:,.0f}",
                "Daily deficit": f"{(avg_daily_apps - avg_daily_installs * 1.25):,.0f}",
                "Years to clear": "Not applicable",
            },
            {
                "Scenario": "-25% intake",
                "Daily intake": f"{avg_daily_apps * 0.75:,.0f}",
                "Daily installations": f"{avg_daily_installs:,.0f}",
                "Daily deficit": f"{(avg_daily_apps * 0.75 - avg_daily_installs):,.0f}",
                "Years to clear": "Not applicable",
            },
        ]

    st.dataframe(pd.DataFrame(scenario_rows), width="stretch", hide_index=True)
    st.caption(
        "Scenarios compare the current flow against a 25% capacity increase or a 25% intake reduction to show how quickly the backlog could be reduced."
    )

st.markdown("---")

# ============================================================================
# SECTION 5: APPROVAL RATE ANOMALIES
# ============================================================================

st.header("5. Approval rate gaps")

state_approval_note = (
    "Note: if an approval rate exceeds 100%, the source records are not aligned at the same grain, "
    "so treat the chart as a hotspot indicator rather than a literal pass rate."
)

# Calculate approval rates by state
state_approval = (
    state_master.groupby("state")
    .agg(
        {
            "feasibility_approved": "sum",
            "vendor_selected": "sum",
            "installation": "sum",
            "inspection_approved": "sum",
        }
    )
    .reset_index()
)

state_approval = filter_all_zero_rows(
    state_approval,
    ["feasibility_approved", "vendor_selected", "installation", "inspection_approved"],
)

state_approval["feasibility_approval_rate"] = np.where(
    state_approval["vendor_selected"] > 0,
    (state_approval["feasibility_approved"] / state_approval["vendor_selected"] * 100).round(2),
    0,
)
state_approval["inspection_approval_rate"] = np.where(
    state_approval["installation"] > 0,
    (state_approval["inspection_approved"] / state_approval["installation"] * 100).round(2),
    0,
)

# Find states with low approval rates
low_feasibility = state_approval.nsmallest(10, "feasibility_approval_rate")
low_inspection = state_approval.nsmallest(10, "inspection_approval_rate")

col1, col2 = st.columns(2)

with col1:
    st.subheader("States with lower feasibility approval rates")

    fig = px.bar(
        low_feasibility.sort_values("feasibility_approval_rate"),
        y="state",
        x="feasibility_approval_rate",
        orientation="h",
        color="feasibility_approval_rate",
        color_continuous_scale=["#d62728", "#ff7f0e", "#2ca02c"],
        text="feasibility_approval_rate",
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="%{x:.1f}% ÔÇö %{y}",
    )
    fig.update_layout(
        height=400, showlegend=False, xaxis_title="Feasibility approval rate (%)"
    )
    st.plotly_chart(fig, width="stretch")
    chart_caption(
        "Lower feasibility approval rates can indicate tighter reviews or more incomplete applications",
        "Source: state_master_clean.csv columns feasibility_approved and vendor_selected.",
    )

with col2:
    st.subheader("States with lower inspection approval rates")

    fig = px.bar(
        low_inspection.sort_values("inspection_approval_rate"),
        y="state",
        x="inspection_approval_rate",
        orientation="h",
        color="inspection_approval_rate",
        color_continuous_scale=["#d62728", "#ff7f0e", "#2ca02c"],
        text="inspection_approval_rate",
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="%{x:.1f}% ÔÇö %{y}",
    )
    fig.update_layout(
        height=400, showlegend=False, xaxis_title="Inspection approval rate (%)"
    )
    st.plotly_chart(fig, width="stretch")
    chart_caption(
        "Lower inspection approval rates show where completed installations are not clearing inspection",
        "Source: state_master_clean.csv columns inspection_approved and installation.",
    )

st.info(state_approval_note)

st.markdown("---")

# ============================================================================
# SECTION 6: ACTIONABLE RECOMMENDATIONS
# ============================================================================

st.header("6. Recommended actions")

recommendations = [
    {
        "priority": "High",
        "issue": f"Gap between {prev_stage} and {worst_stage}",
        "impact": f"{int(worst_loss):,} applications do not move forward here",
        "action": "Review handoff controls, vendor capacity, and local delays.",
        "timeline": "Immediate (1-2 weeks)",
    },
    {
        "priority": "High",
        "issue": "Backlog is growing",
        "impact": f"{int(latest_gap):,} applications are still waiting, and the backlog grows by {daily_deficit:,.0f} per day",
        "action": "Increase processing capacity or slow intake until the system catches up.",
        "timeline": "Immediate (1-2 weeks)",
    },
    {
        "priority": "Medium",
        "issue": "Geographic Hotspots",
        "impact": f'{len(state_analysis_sorted[state_analysis_sorted["app_to_install_rate"] < 20])} states have an application to installation rate below 20%',
        "action": "Move support to weaker states and compare them with better-performing states.",
        "timeline": "Short-term (1-3 months)",
    },
    {
        "priority": "Medium",
        "issue": "High Rejection Rates",
        "impact": f'Feasibility approval rates range from {state_approval["feasibility_approval_rate"].min():.1f}% to {state_approval["feasibility_approval_rate"].max():.1f}%',
        "action": "Use the same review rule across states and check why the gap is so wide.",
        "timeline": "Short-term (1-3 months)",
    },
    {
        "priority": "Medium",
        "issue": "Project inspection bottleneck",
        "impact": f'{int(state_master["installation"].sum() - state_master["inspection_approved"].sum()):,} installations are still waiting for project inspection approval',
        "action": "Speed up inspection scheduling and add more inspection capacity where needed.",
        "timeline": "Medium-term (1-2 months)",
    },
]

for i, rec in enumerate(recommendations, 1):
    st.markdown(
        f"""
    <div style='background-color: #f8f9fa; border-left: 4px solid #ff7f0e; padding: 15px; margin: 15px 0; border-radius: 5px;'>
    <strong>{rec['priority']} Priority #{i}: {rec['issue']}</strong><br>
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
### ­ƒôï Executive summary

Key takeaways for program managers and recruiters:

- **Priority issue:** The largest operational loss is between **{prev_stage}** and **{worst_stage}** ÔÇö this handoff should be investigated first.
- **Backlog risk:** Intake exceeds clearance; the backlog is growing by roughly **{daily_deficit:,.0f}** applications per day.
- **Uneven delivery:** State-level performance varies considerably ÔÇö target support to high-volume, low-conversion states.
- **Approval variability:** Feasibility and inspection approval rates differ across states and explain part of the outcome gap.

Recommended next steps: Share these findings with delivery teams, run focused diagnostics in the top-priority states, and consider temporary capacity increases in the short term.
"""
)
