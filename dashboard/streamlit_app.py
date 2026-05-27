"""
PM Surya Ghar Analytics Dashboard
==================================
Main Streamlit application for exploring PM Surya Ghar program analytics.

Author: Analytics Team
Date: March 15, 2026
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import utility modules
from dashboard.utils.data_loader import load_data
from dashboard.utils.components import kpi_card, create_conversion_funnel
from dashboard.utils.charts import (
    create_adoption_trend,
    create_state_ranking_chart,
    filter_all_zero_rows,
)

# Configure Streamlit
st.set_page_config(
    page_title="PM Surya Ghar Analytics",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown(
    """
<style>
    [data-testid="stMetricValue"] { font-size: 2rem; }
    .main-header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; margin-bottom: 10px; }
    .sub-header { font-size: 1.3rem; color: #555; margin-bottom: 20px; }
    .metric-card { 
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 4px solid #1f77b4;
    }
    .section-divider { 
        border-top: 2px solid #e8e8e8; 
        margin: 30px 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# MAIN LAYOUT
# ============================================================================

# Header
st.markdown(
    '<div class="main-header">PM Surya Ghar Program Dashboard</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Simple view of the scheme data, the main numbers, and where the process slows down</div>',
    unsafe_allow_html=True,
)

# Sidebar - Navigation
st.sidebar.title("Pages")
page_options = {
    "Program snapshot": "Overview",
    "State comparison": "State Analysis",
    "District comparison": "District Analysis",
    "Trend over time": "Trends",
    "Capacity and system size": "Capacity Metrics",
    "About this dashboard": "About",
}
page = page_options[st.sidebar.radio("Choose a page:", list(page_options.keys()))]


# Load data with caching
@st.cache_data
def get_data():
    return load_data()


try:
    kpi_national, kpi_state, kpi_district, datewise, state_master, district = get_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ============================================================================
# PAGE ROUTING
# ============================================================================

if page == "Overview":
    # ========================================================================
    # OVERVIEW PAGE - Main Dashboard
    # ========================================================================

    st.write("""
    This page gives a quick snapshot of program scale, progress, and movement through the main stages.
    """)

    total_apps = int(kpi_national["total_applications"].values[0])
    total_installs = int(kpi_national["total_installations"].values[0])
    total_inspections = int(kpi_national["total_inspections"].values[0])
    total_subsidy_redeemed = int(kpi_national["total_subsidy_redeemed"].values[0])
    total_subsidy_redeemed_crore = total_subsidy_redeemed / 1e7
    app_to_install_rate = float(
        kpi_national["conversion_rate_app_to_install"].values[0]
    )
    install_to_inspection_rate = float(
        kpi_national["conversion_rate_install_to_inspection"].values[0]
    )
    app_to_subsidy_rate = float(
        kpi_national["conversion_rate_app_to_subsidy"].values[0]
    )
    apps_not_installed = max(total_apps - total_installs, 0)

    st.markdown("---")

    # Row 1: Core volume metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            title="Applications recorded",
            value=total_apps,
            delta=None,
            format_type="number",
        )

    with col2:
        kpi_card(
            title="Installations completed",
            value=total_installs,
            delta=None,
            format_type="number",
        )

    with col3:
        kpi_card(
            title="Inspections approved",
            value=total_inspections,
            delta=None,
            format_type="number",
        )

    with col4:
        kpi_card(
            title="Subsidy redeemed amount",
            value=total_subsidy_redeemed_crore,
            delta=None,
            format_type="decimal",
            suffix=" crore",
        )

    st.markdown("---")

    # Row 2: Core rates and backlog
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            title="Application to installation rate",
            value=app_to_install_rate,
            delta=None,
            format_type="percent",
        )

    with col2:
        kpi_card(
            title="Installation to inspection rate",
            value=install_to_inspection_rate,
            delta=None,
            format_type="percent",
        )

    with col3:
        kpi_card(
            title="Application to subsidy rate",
            value=app_to_subsidy_rate,
            delta=None,
            format_type="percent",
        )

    with col4:
        kpi_card(
            title="Applications not yet installed",
            value=apps_not_installed,
            delta=None,
            format_type="number",
        )

    st.markdown("---")

    # Row 3: Coverage
    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_card(
            title="States covered",
            value=int(kpi_national["total_states"].values[0]),
            delta=None,
            format_type="number",
        )

    with col2:
        kpi_card(
            title="Districts covered",
            value=int(kpi_national["total_districts"].values[0]),
            delta=None,
            format_type="number",
        )

    with col3:
        kpi_card(
            title="DISCOMs covered",
            value=int(kpi_national["total_discoms"].values[0]),
            delta=None,
            format_type="number",
        )

    st.markdown("---")

    # Row 4: Trend
    st.subheader("Applications and installations over time")
    fig = create_adoption_trend(datewise)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Row 5: Conversion Funnel
    st.subheader("How applications move through the main stages in the data")

    funnel_data = {
        "Stage": [
            "Applications recorded",
            "Vendor selected",
            "Feasibility approved",
            "Installations completed",
            "Inspections approved",
            "Subsidy redeemed",
        ],
        "Count": [
            int(state_master["application_status"].sum()),
            int(state_master["vendor_selected"].sum()),
            int(state_master["feasibility_approved"].sum()),
            int(state_master["installation"].sum()),
            int(state_master["inspection_approved"].sum()),
            int(state_master["total_redeem"].sum()),
        ],
    }

    funnel_df = pd.DataFrame(funnel_data)
    funnel_df = filter_all_zero_rows(funnel_df, ["Count"])
    if funnel_df.empty:
        st.info("No non-zero stage data available for this period.")
    else:
        cleaned_funnel = {
            "Stage": funnel_df["Stage"].tolist(),
            "Count": funnel_df["Count"].tolist(),
        }
        fig = create_conversion_funnel(cleaned_funnel)
        st.plotly_chart(fig, use_container_width=True)

elif page == "State Analysis":
    st.header("State comparison")

    st.write("""
    Compare states by application volume, installation volume, and application to installation rate.
    """)

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        sort_by = st.selectbox(
            "Rank states by:",
            [
                "Applications recorded",
                "Installations completed",
                "Application to installation rate",
            ],
        )

    with col2:
        show_top = st.slider("Number of states to show:", 5, 36, 10)

    state_base_df = kpi_state[
        [
            "state",
            "applications",
            "installations",
            "conversion_rate_app_to_install_pct",
        ]
    ].copy()
    state_base_df = filter_all_zero_rows(
        state_base_df, ["applications", "installations"]
    )

    # Prepare sorted data
    if sort_by == "Applications recorded":
        state_data = state_base_df.nlargest(show_top, "applications")
    elif sort_by == "Installations completed":
        state_data = state_base_df.nlargest(show_top, "installations")
    else:
        state_data = state_base_df.nlargest(
            show_top, "conversion_rate_app_to_install_pct"
        )

    # Display table
    st.subheader(f"Top {show_top} states")
    st.dataframe(
        state_data[
            [
                "state",
                "applications",
                "installations",
                "conversion_rate_app_to_install_pct",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Applications and installations by state")
        fig = create_state_ranking_chart(state_data)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Application to installation rate by state")
        import plotly.express as px

        fig = px.bar(
            state_data.sort_values(
                "conversion_rate_app_to_install_pct", ascending=True
            ),
            y="state",
            x="conversion_rate_app_to_install_pct",
            orientation="h",
            title="",
            labels={
                "conversion_rate_app_to_install_pct": "Application to installation rate (%)",
                "state": "State",
            },
            color="conversion_rate_app_to_install_pct",
            color_continuous_scale=["#ff7f0e", "#ffaa1f", "#ffcc66", "#1f77b4"],
        )
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

elif page == "District Analysis":
    st.header("District comparison")

    st.write("""
    Review district level results for the selected state.
    """)

    # State filter
    selected_state = st.selectbox(
        "Choose a state:",
        ["All States"] + sorted(kpi_district["state"].unique().tolist()),
    )

    # Filter data
    if selected_state == "All States":
        filtered_data = district.copy()
    else:
        filtered_data = district[district["state"] == selected_state].copy()

    st.subheader(f"Districts in {selected_state} ({len(filtered_data)} districts)")

    # Show summary
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Applications recorded", int(filtered_data["application_status"].sum())
        )

    with col2:
        st.metric("Installations completed", int(filtered_data["installation"].sum()))

    with col3:
        apps = filtered_data["application_status"].sum()
        insts = filtered_data["installation"].sum()
        conv_rate = (insts / apps * 100) if apps > 0 else 0
        st.metric("Application to installation rate", f"{conv_rate:.1f}%")

    # District table
    st.subheader("District-level table")

    display_cols = [
        "state",
        "district",
        "application_status",
        "installation",
        "inspection_approved",
        "total_redeem",
    ]

    display_data = filtered_data[display_cols].copy()
    display_data.columns = [
        "State",
        "District",
        "Applications recorded",
        "Installations completed",
        "Inspections approved",
        "Subsidy redeemed",
    ]

    st.dataframe(
        display_data.sort_values("Applications", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

elif page == "Trends":
    st.header("Trend over time")

    st.write("""
    Review how applications and installations change over time.
    """)

    trend_df = datewise[["rptdate", "applications", "installations"]].copy()
    trend_df = filter_all_zero_rows(trend_df, ["applications", "installations"])
    datewise_sorted = trend_df.sort_values("rptdate")
    datewise_sorted["rptdate"] = pd.to_datetime(datewise_sorted["rptdate"])
    datewise_sorted["cum_applications"] = datewise_sorted["applications"].cumsum()
    datewise_sorted["cum_installations"] = datewise_sorted["installations"].cumsum()

    # Chart type selector
    chart_type = st.radio("Choose a view:", ["Cumulative", "Daily"], horizontal=True)

    if chart_type == "Cumulative":
        st.subheader("Cumulative applications and installations")

        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": False}]])

        fig.add_trace(
            go.Scatter(
                x=datewise_sorted["rptdate"],
                y=datewise_sorted["cum_applications"],
                name="Applications",
                mode="lines",
                line=dict(color="#1f77b4", width=2),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=datewise_sorted["rptdate"],
                y=datewise_sorted["cum_installations"],
                name="Installations",
                mode="lines",
                line=dict(color="#ff7f0e", width=2),
            )
        )

        fig.update_layout(
            title="Cumulative program totals",
            xaxis_title="Date",
            yaxis_title="Cumulative count",
            hovermode="x unified",
            height=600,
            template="plotly_white",
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.subheader("Daily applications and installations")

        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=datewise_sorted["rptdate"],
                y=datewise_sorted["applications"],
                name="Applications",
                mode="lines",
                line=dict(color="#1f77b4", width=1.5),
                fill="tozeroy",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=datewise_sorted["rptdate"],
                y=datewise_sorted["installations"],
                name="Installations",
                mode="lines",
                line=dict(color="#ff7f0e", width=1.5),
                fill="tozeroy",
            )
        )

        fig.update_layout(
            title="Daily program activity",
            xaxis_title="Date",
            yaxis_title="Daily count",
            hovermode="x unified",
            height=600,
            template="plotly_white",
        )

        st.plotly_chart(fig, use_container_width=True)

elif page == "Capacity Metrics":
    st.header("Capacity and system size")

    st.write("""
    Review installed capacity, average system size, and the split between residential and RWA systems.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Installed capacity (kW)",
            f"{int(kpi_national['total_capacity_installed_kw'].values[0]):,}",
        )

    with col2:
        st.metric(
            "Average system size (kW)",
            f"{float(kpi_national['average_system_size_kw'].values[0]):.2f}",
        )

    with col3:
        st.metric(
            "Installations completed",
            f"{int(kpi_national['total_installations'].values[0]):,}",
        )

    st.markdown("---")

    # Residential vs RWA
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Residential and RWA share")

        adoption_data = {
            "Type": ["Residential systems", "RWA systems"],
            "Percentage": [
                float(kpi_national["residential_percentage"].values[0]),
                float(kpi_national["rwa_percentage"].values[0]),
            ],
        }
        adoption_df = pd.DataFrame(adoption_data)
        adoption_df = filter_all_zero_rows(adoption_df, ["Percentage"])

        import plotly.express as px

        if adoption_df.empty:
            st.info("No non-zero adoption share data available.")
        else:
            fig = px.pie(
                adoption_df,
                values="Percentage",
                names="Type",
                color_discrete_sequence=["#1f77b4", "#ff7f0e"],
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Systems up to 10 kW and above 10 kW")

        # Calculate up to 10kW and above 10kW
        upto_10kw = datewise["upto_10_kw"].sum()
        above_10kw = datewise["above_10_kw"].sum()

        capacity_data = {
            "Size": ["Up to 10 kW", "Above 10 kW"],
            "Count": [int(upto_10kw), int(above_10kw)],
        }
        capacity_df = pd.DataFrame(capacity_data)
        capacity_df = filter_all_zero_rows(capacity_df, ["Count"])

        import plotly.express as px

        if capacity_df.empty:
            st.info("No non-zero system size data available.")
        else:
            fig = px.bar(
                capacity_df,
                x="Size",
                y="Count",
                color="Size",
                color_discrete_sequence=["#2ca02c", "#d62728"],
                title="System size counts",
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

elif page == "About":
    st.header("About this dashboard")

    st.markdown("""
    ### PM Surya Ghar Analytics

    This dashboard shows how the PM Surya Ghar rooftop solar scheme is moving through each stage.
    The aim is simple: make the data easy to read, show where applications move smoothly,
    and make the problem areas easy to spot.

    **What this dashboard covers:**
    - **Time Period:** September 17, 2022 – February 9, 2026
    - **Geography:** 36 States/UTs, 792 Districts, 84 DISCOMs
    - **Records Reviewed:** 6,021,455 applications

    **Main numbers:**
    - Applications recorded: 6,021,455
    - Installations completed: 2,329,634
    - Application to installation rate: 38.69%
    - Installed capacity: 17.1 Million kW

    **What we checked:**
    - cleaned the source files before analysis
    - cross-checked the KPI totals against the cleaned data
    - reviewed the geography level counts
    - kept the dashboard focused on the main numbers first

    **What you can see here:**
    - **Overview:** the main numbers and the funnel summary
    - **State Analysis:** which states are doing well and which are lagging
    - **District Analysis:** the district level picture
    - **Trends:** how the program changes over time
    - **Capacity Metrics:** how system size and segment mix compare
    - **Bottleneck Analysis:** where the process slows down

    **Built with:**
    - Python 3.11, Streamlit, Pandas, and Plotly
    - simple checks for data cleaning and validation
    - interactive charts with hover details
    - responsive layout for desktop and mobile

    **Version:** 1.0.0  
    **Last Updated:** March 15, 2026  
    **Status:** Production Ready
    """)

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
    PM Surya Ghar Analytics Dashboard | Clear, simple insights from program data
    </div>
    """,
        unsafe_allow_html=True,
    )
