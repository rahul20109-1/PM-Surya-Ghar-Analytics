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
from dashboard.utils.charts import create_adoption_trend, create_state_ranking_chart

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
    '<div class="main-header">☀️ PM Surya Ghar Analytics Dashboard</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Comprehensive Analysis of India\'s Solar Rooftop Subsidy Program</div>',
    unsafe_allow_html=True,
)

# Sidebar - Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page:",
    [
        "Overview",
        "State Analysis",
        "District Analysis",
        "Trends",
        "Capacity Metrics",
        "About",
    ],
)


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

    st.markdown("---")

    # Row 1: Key National Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            title="Total Applications",
            value=int(kpi_national["total_applications"].values[0]),
            delta=None,
            format_type="number",
        )

    with col2:
        kpi_card(
            title="Total Installations",
            value=int(kpi_national["total_installations"].values[0]),
            delta=None,
            format_type="number",
        )

    with col3:
        kpi_card(
            title="App → Installation",
            value=float(kpi_national["conversion_rate_app_to_install"].values[0]),
            delta=None,
            format_type="percent",
        )

    with col4:
        kpi_card(
            title="Total States",
            value=int(kpi_national["total_states"].values[0]),
            delta=None,
            format_type="number",
        )

    st.markdown("---")

    # Row 2: Additional Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            title="Total Inspections",
            value=int(kpi_national["total_inspections"].values[0]),
            delta=None,
            format_type="number",
        )

    with col2:
        kpi_card(
            title="Total Districts",
            value=int(kpi_national["total_districts"].values[0]),
            delta=None,
            format_type="number",
        )

    with col3:
        kpi_card(
            title="Residential %",
            value=float(kpi_national["residential_percentage"].values[0]),
            delta=None,
            format_type="percent",
        )

    with col4:
        kpi_card(
            title="Avg System Size",
            value=float(kpi_national["average_system_size_kw"].values[0]),
            delta=None,
            format_type="decimal",
            suffix=" kW",
        )

    st.markdown("---")

    # Row 3: Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Adoption Trend Over Time")
        fig = create_adoption_trend(datewise)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Top 10 States by Applications")
        fig = create_state_ranking_chart(kpi_state.head(10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Row 4: Conversion Funnel
    st.subheader("🔄 Application to Subsidy Funnel")

    funnel_data = {
        "Stage": [
            "Applications",
            "Vendor Selected",
            "Feasibility Approved",
            "Installations",
            "Inspections",
            "Subsidy Redeemed",
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

    fig = create_conversion_funnel(funnel_data)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Row 5: National Statistics
    st.subheader("📊 National Statistics")

    stat_col1, stat_col2, stat_col3 = st.columns(3)

    with stat_col1:
        st.metric(
            "Total Capacity Installed",
            f"{int(kpi_national['total_capacity_installed_kw'].values[0]):,} kW",
        )

    with stat_col2:
        st.metric("Total DISCOMs", int(kpi_national["total_discoms"].values[0]))

    with stat_col3:
        st.metric(
            "Subsidy per Installation",
            f"₹{int(kpi_national['subsidy_per_installation'].values[0]):,}",
        )

elif page == "State Analysis":
    st.header("🗺️ State-Level Analysis")

    st.write(
        """
    Explore state-wise adoption metrics, conversion rates, and rankings.
    """
    )

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        sort_by = st.selectbox(
            "Sort by:", ["Applications", "Installations", "Conversion Rate"]
        )

    with col2:
        show_top = st.slider("Show top N states:", 5, 36, 10)

    # Prepare sorted data
    if sort_by == "Applications":
        state_data = kpi_state.nlargest(show_top, "applications")
    elif sort_by == "Installations":
        state_data = kpi_state.nlargest(show_top, "installations")
    else:
        state_data = kpi_state.nlargest(show_top, "conversion_rate_app_to_install_pct")

    # Display table
    st.subheader(f"Top {show_top} States")
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
        st.subheader("Applications vs Installations")
        fig = create_state_ranking_chart(state_data)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Conversion Rate by State")
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
                "conversion_rate_app_to_install_pct": "Conversion Rate (%)",
                "state": "",
            },
            color="conversion_rate_app_to_install_pct",
            color_continuous_scale=["#ff7f0e", "#ffaa1f", "#ffcc66", "#1f77b4"],
        )
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

elif page == "District Analysis":
    st.header("🎯 District-Level Analysis")

    st.write(
        """
    Analyze adoption metrics at the district level. Filter by state for detailed insights.
    """
    )

    # State filter
    selected_state = st.selectbox(
        "Select State:",
        ["All States"] + sorted(kpi_district["state"].unique().tolist()),
    )

    # Filter data
    if selected_state == "All States":
        filtered_data = district.copy()
    else:
        filtered_data = district[district["state"] == selected_state].copy()

    st.subheader(f"Districts: {selected_state} ({len(filtered_data)} districts)")

    # Show summary
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Applications", int(filtered_data["application_status"].sum()))

    with col2:
        st.metric("Total Installations", int(filtered_data["installation"].sum()))

    with col3:
        apps = filtered_data["application_status"].sum()
        insts = filtered_data["installation"].sum()
        conv_rate = (insts / apps * 100) if apps > 0 else 0
        st.metric("Conversion Rate", f"{conv_rate:.1f}%")

    # District table
    st.subheader("District Details")

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
        "Applications",
        "Installations",
        "Inspections",
        "Subsidy Redeemed",
    ]

    st.dataframe(
        display_data.sort_values("Applications", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

elif page == "Trends":
    st.header("📈 Trends Over Time")

    st.write(
        """
    Analyze adoption trends, growth patterns, and seasonal variations.
    """
    )

    # Prepare datewise data
    datewise_sorted = datewise.sort_values("rptdate")
    datewise_sorted["rptdate"] = pd.to_datetime(datewise_sorted["rptdate"])
    datewise_sorted["cum_applications"] = datewise_sorted["applications"].cumsum()
    datewise_sorted["cum_installations"] = datewise_sorted["installations"].cumsum()

    # Chart type selector
    chart_type = st.radio("Select View:", ["Cumulative", "Daily"], horizontal=True)

    if chart_type == "Cumulative":
        st.subheader("Cumulative Applications & Installations")

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
            title="Program Cumulative Growth",
            xaxis_title="Date",
            yaxis_title="Cumulative Count",
            hovermode="x unified",
            height=600,
            template="plotly_white",
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.subheader("Daily Applications & Installations")

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
            title="Daily Activity",
            xaxis_title="Date",
            yaxis_title="Daily Count",
            hovermode="x unified",
            height=600,
            template="plotly_white",
        )

        st.plotly_chart(fig, use_container_width=True)

elif page == "Capacity Metrics":
    st.header("⚡ Capacity Metrics")

    st.write(
        """
    Analyze installed capacity, system size distribution, and residential vs RWA adoption.
    """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Capacity (kW)",
            f"{int(kpi_national['total_capacity_installed_kw'].values[0]):,}",
        )

    with col2:
        st.metric(
            "Avg System Size (kW)",
            f"{float(kpi_national['average_system_size_kw'].values[0]):.2f}",
        )

    with col3:
        st.metric(
            "Total Installations",
            f"{int(kpi_national['total_installations'].values[0]):,}",
        )

    st.markdown("---")

    # Residential vs RWA
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Adoption Type Distribution")

        adoption_data = {
            "Type": ["Residential", "RWA"],
            "Percentage": [
                float(kpi_national["residential_percentage"].values[0]),
                float(kpi_national["rwa_percentage"].values[0]),
            ],
        }

        import plotly.express as px

        fig = px.pie(
            adoption_data,
            values="Percentage",
            names="Type",
            color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("System Size Distribution")

        # Calculate up to 10kW and above 10kW
        upto_10kw = datewise["upto_10_kw"].sum()
        above_10kw = datewise["above_10_kw"].sum()

        capacity_data = {
            "Size": ["Up to 10 kW", "Above 10 kW"],
            "Count": [int(upto_10kw), int(above_10kw)],
        }

        import plotly.express as px

        fig = px.bar(
            capacity_data,
            x="Size",
            y="Count",
            color="Size",
            color_discrete_sequence=["#2ca02c", "#d62728"],
            title="",
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "About":
    st.header("ℹ️ About This Dashboard")

    st.markdown(
        """
    ### PM Surya Ghar Analytics
    
    **Project Objective:**
    Comprehensive analytics of India's PM Surya Ghar (Pradhan Mantri Suryodaya) rooftop solar 
    subsidy program to showcase data analysis and visualization skills.
    
    **Data Coverage:**
    - **Time Period:** September 17, 2022 – February 9, 2026
    - **Geography:** 36 States/UTs, 792 Districts, 84 DISCOMs
    - **Records:** 6,021,455 applications analyzed
    
    **Key Metrics:**
    - Total Applications: 6,021,455
    - Total Installations: 2,329,634
    - Conversion Rate: 38.69%
    - Total Capacity Installed: 17.1 Million kW
    
    **Data Quality:**
    ✅ All data cleaned and verified  
    ✅ 0 nulls in main analytical files  
    ✅ Metrics cross-checked against source data  
    ✅ Geographic hierarchy validated
    
    **Dashboard Features:**
    - **Overview:** National KPIs and trend summary
    - **State Analysis:** State-wise rankings and metrics
    - **District Analysis:** District-level adoption details
    - **Trends:** Time-series adoption curves
    - **Capacity Metrics:** System size and adoption type analysis
    
    **Technologies:**
    - Python 3.11 | Streamlit | Pandas | Plotly
    - Data cleaning and validation with robust parsers
    - Interactive visualizations with hover information
    - Responsive design for desktop and mobile
    
    **Design Guidelines:**
    - Color scheme: Professional blue/orange palette
    - Metrics verified and validated
    - All conversions rates calculated consistently
    - Following frontend guidelines for consistency
    
    **Version:** 1.0.0  
    **Last Updated:** March 15, 2026  
    **Status:** Production Ready ✅
    """
    )

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
    PM Surya Ghar Analytics Dashboard | Data-Driven Insights for India's Solar Initiative
    </div>
    """,
        unsafe_allow_html=True,
    )
