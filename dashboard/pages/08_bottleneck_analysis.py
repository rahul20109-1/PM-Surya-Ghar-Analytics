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

from dashboard.utils.data_loader import load_data
from dashboard.utils.charts import filter_all_zero_rows

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

st.title("Where the process slows down")
st.markdown("""
This page shows where applications slow down, where they wait, and which states need the most attention.
""")
st.caption(
    "Stages in this analysis align to the scheme journey steps captured in the source data. "
    "Consumer registration, agreement upload, and subsidy approval or disbursal are not available in this dataset."
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
        "Vendor selection",
        "Feasibility approval",
        "Installation completed",
        "Project inspection by DISCOM",
        "Subsidy redeem",
    ],
    "Count": [
        state_master["application_status"].sum(),
        state_master["vendor_selected"].sum(),
        state_master["feasibility_approved"].sum(),
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
    st.metric(
        "Largest drop-off stage",
        funnel_df["Stage"].iloc[worst_stage_idx],
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

st.dataframe(display_df, use_container_width=True, hide_index=True)

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

        fig.update_layout(height=500, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

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
            title="",
            color="Stage Dropout %",
            color_continuous_scale=["#2ca02c", "#ff7f0e", "#d62728"],
            text="Stage Dropout %",
        )

        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(height=500, showlegend=False, xaxis_tickangle=-45)
        fig.update_xaxes(tickfont=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)

# Critical insight
st.markdown(
    """
<div class="insight-box">
<strong>Main finding:</strong> The biggest drop happens between <strong>Feasibility approval</strong> and <strong>Installation completed</strong>.
That gap is {:.1f}% of the previous stage, which means {:.0f} applications do not move forward here.
</div>
""".format(
        funnel_df[funnel_df["Stage"] == "Installation completed"][
            "Stage Dropout %"
        ].values[0],
        funnel_df[funnel_df["Stage"] == "Installation completed"]["Loss Count"].values[
            0
        ],
    ),
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
    ("Vendor selection", "application_status", "vendor_selected"),
    ("Feasibility approval", "vendor_selected", "feasibility_approved"),
    ("Installation completed", "feasibility_approved", "installation"),
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
        "Total waiting applications",
        f"{int(pending_df['Pending'].sum()):,}",
        f"of {int(pending_df['Applications'].iloc[0]):,} total",
    )

with col2:
    highest_pending_stage = pending_df.iloc[0]
    st.metric(
        "Stage with the most waiting applications",
        highest_pending_stage["Stage"],
        f"{int(highest_pending_stage['Pending']):,} applications",
    )

with col3:
    highest_pending_pct = pending_df["Pending %"].max()
    st.metric(
        "Largest waiting share",
        f"{highest_pending_pct:.1f}%",
        "Share of applications waiting at this stage",
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
            title="",
            color="Pending %",
            color_continuous_scale=["#2ca02c", "#ff7f0e", "#d62728"],
            text="Pending",
        )

        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

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
            title="",
            color="Pending %",
            color_continuous_scale=["#2ca02c", "#ff7f0e", "#d62728"],
            text="Pending %",
        )

        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 3: GEOGRAPHIC BOTTLENECK ANALYSIS
# ============================================================================

st.header("3. State comparison")

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
    )

with col2:
    top_n = st.slider("Number of states to show:", 5, 36, 15)

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

st.subheader(f"Top {top_n} states with the largest issues")

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

st.dataframe(table_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================================
# SECTION 4: TIME-BASED BOTTLENECK ANALYSIS
# ============================================================================

st.header("4. Processing speed over time")

# Analyze daily throughput
throughput_df = datewise[["rptdate", "applications", "installations"]].copy()
throughput_df = filter_all_zero_rows(throughput_df, ["applications", "installations"])
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
            name="Applications (7-day average)",
            mode="lines",
            line=dict(color="#1f77b4", width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=datewise_analysis["rptdate"],
            y=datewise_analysis["installs_7d_avg"],
            name="Installations (7-day average)",
            mode="lines",
            line=dict(color="#2ca02c", width=2),
        )
    )

    fig.update_layout(
        height=400,
        hovermode="x unified",
        template="plotly_white",
        yaxis_title="Daily count (7-day average)",
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Backlog growth over time")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=datewise_analysis["rptdate"],
            y=datewise_analysis["cumulative_gap"],
            name="Backlog",
            mode="lines",
            fill="tozeroy",
            line=dict(color="#d62728", width=2),
        )
    )

    fig.update_layout(
        height=400,
        hovermode="x",
        template="plotly_white",
        yaxis_title="Cumulative pending applications",
    )

    st.plotly_chart(fig, use_container_width=True)

# Throughput metrics
latest_gap = datewise_analysis["cumulative_gap"].iloc[-1]
avg_daily_apps = datewise_analysis["applications"].mean()
avg_daily_installs = datewise_analysis["installations"].mean()
daily_deficit = avg_daily_apps - avg_daily_installs

st.markdown(
    f"""
<div class="insight-box">
<strong>Main finding:</strong><br>
• Applications received per day: <strong>{avg_daily_apps:,.0f}</strong><br>
• Installations completed per day: <strong>{avg_daily_installs:,.0f}</strong><br>
• Backlog grows by: <strong class="critical">{daily_deficit:,.0f} applications per day</strong><br>
• Current total backlog: <strong class="critical">{int(latest_gap):,} applications</strong><br>
<br>
<strong>At the current rate, it will take about {int(latest_gap / daily_deficit / 365):.1f} years to clear the backlog.</strong>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# ============================================================================
# SECTION 5: APPROVAL RATE ANOMALIES
# ============================================================================

st.header("5. Approval rate gaps")

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

state_approval["feasibility_approval_rate"] = (
    state_approval["feasibility_approved"] / state_approval["vendor_selected"] * 100
).round(2)
state_approval["inspection_approval_rate"] = (
    state_approval["inspection_approved"] / state_approval["installation"] * 100
).round(2)

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

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

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

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 6: ACTIONABLE RECOMMENDATIONS
# ============================================================================

st.header("6. Recommended actions")

recommendations = [
    {
        "priority": "High",
        "issue": "Gap between feasibility approval and installation",
        "impact": f'{int(funnel_df[funnel_df["Stage"] == "Installation completed"]["Loss Count"].values[0]):,} applications do not move forward here',
        "action": "Check vendor capacity, cost, approvals, and local delays.",
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

st.markdown("""
### 📋 Summary

This bottleneck analysis reveals:

1. **The biggest loss is between feasibility approval and installation completed** - that is the clearest stage gap
2. **The backlog keeps growing** - more applications come in than the system clears each day
3. **State performance is uneven** - some states move applications much faster than others
4. **Approval rates are not the same everywhere** - feasibility and project inspection results vary by state
5. **The backlog will not clear on its own** - the process needs more capacity or a slower intake rate

**Next step:** Share these findings with program teams and focus first on the stage with the largest drop.
""")
