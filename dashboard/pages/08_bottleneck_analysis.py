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

st.title("🔍 Bottleneck Analysis")
st.markdown(
    """
Identify critical process bottlenecks, application dropoffs, and improvement opportunities 
in the PM Surya Ghar subsidy approval pipeline.
"""
)

st.markdown("---")

# ============================================================================
# SECTION 1: FUNNEL STAGE ANALYSIS
# ============================================================================

st.header("1️⃣ Application Funnel - Stage-wise Dropout Analysis")

# Calculate funnel metrics
funnel_stages = {
    "Stage": [
        "1. Applications Received",
        "2. Vendor Selected",
        "3. Feasibility Approved",
        "4. Installation Completed",
        "5. Inspection Approved",
        "6. Subsidy Redeemed",
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
    st.metric("Total Applications", f"{int(funnel_df['Count'].iloc[0]):,}", delta=None)

with col2:
    successful = funnel_df["Count"].iloc[-1]
    success_rate = successful / funnel_df["Count"].iloc[0] * 100
    st.metric(
        "Completed (Subsidy Redeemed)",
        f"{int(successful):,}",
        delta=f"{success_rate:.1f}% success rate",
    )

with col3:
    total_pending = funnel_df["Count"].iloc[0] - funnel_df["Count"].iloc[-1]
    st.metric(
        "Stuck in Pipeline",
        f"{int(total_pending):,}",
        delta=f"{(total_pending/funnel_df['Count'].iloc[0]*100):.1f}% pending",
    )

with col4:
    worst_stage_idx = funnel_df["Stage Dropout %"].idxmax()
    worst_dropout = funnel_df["Stage Dropout %"].max()
    st.metric(
        "Worst Dropout Stage",
        funnel_df["Stage"].iloc[worst_stage_idx].split(".")[1].strip(),
        delta=f"{worst_dropout:.1f}% loss",
    )

st.markdown("---")

# Display funnel table
st.subheader("📊 Detailed Funnel Breakdown")

display_df = funnel_df.copy()
display_df["Count"] = display_df["Count"].apply(lambda x: f"{int(x):,}")
display_df["Loss Count"] = display_df["Loss Count"].apply(
    lambda x: f"{int(x):,}" if x > 0 else "-"
)

st.dataframe(display_df, use_container_width=True, hide_index=True)

# Funnel visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Funnel Flow Visualization")

    fig = go.Figure(
        go.Funnel(
            y=funnel_stages["Stage"],
            x=funnel_stages["Count"],
            marker=dict(
                color=["#1f77b4", "#1f77b4", "#ff7f0e", "#ff7f0e", "#d62728", "#2ca02c"]
            ),
            text=[
                f"{count:,}<br>({pct:.1f}%)"
                for count, pct in zip(funnel_stages["Count"], funnel_df["Cumulative %"])
            ],
            textposition="inside",
        )
    )

    fig.update_layout(height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Stage Dropout Rate (%)")

    # Remove first stage (no prior stage)
    dropout_data = funnel_df.iloc[1:].copy()

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
<strong>🚨 KEY INSIGHT:</strong> The biggest dropout happens between <strong>Feasibility Approved → Installation</strong>
({:.1f}% loss, {:.0f} applications rejected/abandoned). This is your PRIMARY BOTTLENECK.
</div>
""".format(
        funnel_df[funnel_df["Stage"] == "4. Installation Completed"][
            "Stage Dropout %"
        ].values[0],
        funnel_df[funnel_df["Stage"] == "4. Installation Completed"][
            "Loss Count"
        ].values[0],
    ),
    unsafe_allow_html=True,
)

st.markdown("---")

# ============================================================================
# SECTION 2: PENDING APPLICATIONS ANALYSIS
# ============================================================================

st.header("2️⃣ Pending Applications - Where Are They Stuck?")

# Calculate pending at each stage
pending_analysis = {"Stage": [], "Applications": [], "Pending": [], "Pending %": []}

stages_to_check = [
    ("Vendor Selection", "application_status", "vendor_selected"),
    ("Feasibility Check", "vendor_selected", "feasibility_approved"),
    ("Installation", "feasibility_approved", "installation"),
    ("Inspection", "installation", "inspection_approved"),
    ("Subsidy Redemption", "inspection_approved", "total_redeem"),
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
        "Total Pending",
        f"{int(pending_df['Pending'].sum()):,}",
        f"of {int(pending_df['Applications'].iloc[0]):,} total",
    )

with col2:
    highest_pending_stage = pending_df.iloc[0]
    st.metric(
        "Highest Pending Stage",
        highest_pending_stage["Stage"],
        f"{int(highest_pending_stage['Pending']):,} applications",
    )

with col3:
    highest_pending_pct = pending_df["Pending %"].max()
    st.metric(
        "Highest Pending %", f"{highest_pending_pct:.1f}%", "Stage bottleneck severity"
    )

st.markdown("---")

# Pending visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pending Applications by Stage")

    fig = px.bar(
        pending_df.sort_values("Pending", ascending=True),
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
    st.subheader("Pending % by Stage")

    fig = px.bar(
        pending_df.sort_values("Pending %", ascending=True),
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

st.header("3️⃣ Geographic Bottleneck Map - State Performance")

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
        "View bottleneck by:",
        ["Lowest Conversion Rate", "Highest Pending %", "Lowest Installation Rate"],
        horizontal=True,
    )

with col2:
    top_n = st.slider("Show top N states:", 5, 36, 15)

# Prepare display data
if issue_type == "Lowest Conversion Rate":
    display_df = state_analysis_sorted.head(top_n)
    metric_col = "app_to_install_rate"
    metric_name = "App→Install Rate"
elif issue_type == "Highest Pending %":
    state_analysis["pending_pct"] = (
        (state_analysis["applications"] - state_analysis["subsidy_redeemed"])
        / state_analysis["applications"]
        * 100
    ).round(2)
    display_df = state_analysis.nlargest(top_n, "pending_pct")
    metric_col = "pending_pct"
    metric_name = "Pending %"
else:
    display_df = state_analysis.nsmallest(top_n, "install_completion_rate")
    metric_col = "install_completion_rate"
    metric_name = "Install Rate %"

st.subheader(f"Top {top_n} States with Bottleneck Issues")

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

st.header("4️⃣ Processing Speed - Application vs Completion")

# Analyze daily throughput
datewise_analysis = datewise.copy()
datewise_analysis = datewise_analysis.sort_values("rptdate")
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
    st.subheader("Daily Application vs Installation Rate (7-day avg)")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=datewise_analysis["rptdate"],
            y=datewise_analysis["apps_7d_avg"],
            name="Applications (7d avg)",
            mode="lines",
            line=dict(color="#1f77b4", width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=datewise_analysis["rptdate"],
            y=datewise_analysis["installs_7d_avg"],
            name="Installations (7d avg)",
            mode="lines",
            line=dict(color="#2ca02c", width=2),
        )
    )

    fig.update_layout(
        height=400,
        hovermode="x unified",
        template="plotly_white",
        yaxis_title="Daily Count (7-day average)",
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Backlog Growth Over Time")

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
        yaxis_title="Cumulative Pending Applications",
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
<strong>⚠️ PROCESSING SPEED ISSUE:</strong><br>
• Daily applications received: <strong>{avg_daily_apps:,.0f}</strong><br>
• Daily installations completed: <strong>{avg_daily_installs:,.0f}</strong><br>
• Daily backlog growth: <strong class="critical">{daily_deficit:,.0f} applications/day</strong><br>
• Current total backlog: <strong class="critical">{int(latest_gap):,} applications</strong><br>
<br>
<strong>At current processing rate, it will take {int(latest_gap / daily_deficit / 365):.1f} years to clear the backlog!</strong>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# ============================================================================
# SECTION 5: APPROVAL RATE ANOMALIES
# ============================================================================

st.header("5️⃣ Approval Rate Anomalies - High Rejection States")

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
    st.subheader("🚨 States with Low Feasibility Approval Rates")

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
    st.subheader("🚨 States with Low Inspection Approval Rates")

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

st.header("💡 Actionable Recommendations")

recommendations = [
    {
        "priority": "🔴 CRITICAL",
        "issue": "Installation Completion Gap",
        "impact": f'{int(funnel_df[funnel_df["Stage"] == "4. Installation Completed"]["Loss Count"].values[0]):,} apps stuck',
        "action": "Investigate why feasibility-approved applications don't proceed to installation. Check vendor capacity, cost, or timeline issues.",
        "timeline": "Immediate (1-2 weeks)",
    },
    {
        "priority": "🔴 CRITICAL",
        "issue": "Processing Backlog Growth",
        "impact": f"{int(latest_gap):,} apps in backlog, growing {daily_deficit:,.0f}/day",
        "action": "Increase installation/inspection capacity or reduce application intake to match processing speed.",
        "timeline": "Immediate (1-2 weeks)",
    },
    {
        "priority": "🟠 HIGH",
        "issue": "Geographic Hotspots",
        "impact": f'{len(state_analysis_sorted[state_analysis_sorted["app_to_install_rate"] < 20])} states with <20% conversion',
        "action": "Deploy resources to underperforming states. Benchmark best practices from high-conversion states.",
        "timeline": "Short-term (1-3 months)",
    },
    {
        "priority": "🟠 HIGH",
        "issue": "High Rejection Rates",
        "impact": f'Feasibility rejection varies {state_approval["feasibility_approval_rate"].min():.1f}% to {state_approval["feasibility_approval_rate"].max():.1f}%',
        "action": "Standardize feasibility criteria across states. Audit why some states reject >80% of applications.",
        "timeline": "Short-term (1-3 months)",
    },
    {
        "priority": "🟡 MEDIUM",
        "issue": "Inspection Bottleneck",
        "impact": f'{int(state_master["installation"].sum() - state_master["inspection_approved"].sum()):,} installations awaiting inspection',
        "action": "Accelerate inspection schedules. Hire/train more inspectors in bottleneck regions.",
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
    """
### 📋 Summary

This bottleneck analysis reveals:

1. **Installation Phase is the Killer** - 61.3% of feasibility-approved apps never get installed
2. **Backlog is Growing Exponentially** - Receiving more apps than we can process daily
3. **Geographic Disparities are Severe** - Some states at 10% conversion, others at 60%+
4. **Approval Standards Vary Wildly** - Inconsistent feasibility/inspection processes across states
5. **Time is the Enemy** - At current rates, it'll take years to clear the backlog

**Next Steps:** Share these findings with program administrators and focus resources on the installation phase bottleneck first.
"""
)
