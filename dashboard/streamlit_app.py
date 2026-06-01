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
from dashboard.utils.components import (
    kpi_card,
    create_conversion_funnel,
    chart_caption,
    how_to_read_chart,
)
from dashboard.utils.charts import (
    create_adoption_trend,
    create_state_scatter_chart,
    create_state_ranking_chart,
    filter_all_zero_rows,
)
import runpy

# Configure Streamlit
st.set_page_config(
    page_title="PM Surya Ghar Analytics",
    page_icon=":sunny:",
    layout="wide",
    initial_sidebar_state="collapsed",
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
    '<div class="sub-header">Decision-support dashboard for PM Surya Ghar, providing a clear view of program scale, implementation performance, and bottlenecks requiring targeted intervention.</div>',
    unsafe_allow_html=True,
)

# Sidebar - Navigation
st.sidebar.title("Pages")
page_options = {
    "Program snapshot": "Overview",
    "State comparison": "State Analysis",
    "District comparison": "District Analysis",
    "Trend over time": "Trends",
    "About this dashboard": "About",
}
selected_page_label = st.sidebar.radio("Choose a page:", list(page_options.keys()))


# Load data with caching
@st.cache_data
def get_data():
    return load_data()


def apply_date_range_filter(df, key_prefix):
    df = df.copy()
    df["rptdate"] = pd.to_datetime(df["rptdate"], errors="coerce")
    df = df.dropna(subset=["rptdate"])
    if df.empty:
        return df, None, None

    min_date = df["rptdate"].min().date()
    max_date = df["rptdate"].max().date()
    full_days = (max_date - min_date).days
    default_start = (pd.Timestamp(max_date) - pd.Timedelta(days=365)).date()
    if default_start < min_date:
        default_start = min_date

    preset_options = [
        "Last 30 days",
        "Last 90 days",
        "Year to date",
        "Last 12 months",
        "All",
        "Custom",
    ]
    preset_index = 3 if full_days > 365 else 4
    preset = st.selectbox(
        "Quick range",
        preset_options,
        index=preset_index,
        key=f"{key_prefix}_preset",
    )

    if preset == "Custom":
        selected_dates = st.date_input(
            "Custom range",
            value=(default_start, max_date),
            key=f"{key_prefix}_custom",
        )
        if isinstance(selected_dates, tuple) or isinstance(selected_dates, list):
            if len(selected_dates) == 2:
                start_date, end_date = selected_dates
            elif len(selected_dates) == 1:
                start_date = selected_dates[0]
                end_date = max_date
            else:
                start_date = default_start
                end_date = max_date
        else:
            start_date = selected_dates
            end_date = max_date
    elif preset == "Last 30 days":
        start_date = (pd.Timestamp(max_date) - pd.Timedelta(days=29)).date()
        end_date = max_date
    elif preset == "Last 90 days":
        start_date = (pd.Timestamp(max_date) - pd.Timedelta(days=89)).date()
        end_date = max_date
    elif preset == "Year to date":
        start_date = pd.Timestamp(max_date.year, 1, 1).date()
        end_date = max_date
    elif preset == "Last 12 months":
        start_date = default_start
        end_date = max_date
    else:
        start_date = min_date
        end_date = max_date

    if start_date < min_date:
        start_date = min_date
    if end_date > max_date:
        end_date = max_date

    mask = (df["rptdate"].dt.date >= start_date) & (
        df["rptdate"].dt.date <= end_date
    )
    filtered = df.loc[mask].copy()
    return filtered, start_date, end_date


def summarize_period_totals(df, start_date, end_date):
    period_df = df.copy()
    period_df["rptdate"] = pd.to_datetime(period_df["rptdate"], errors="coerce")
    period_df = period_df.dropna(subset=["rptdate"])
    if start_date is not None:
        period_df = period_df[period_df["rptdate"].dt.date >= start_date]
    if end_date is not None:
        period_df = period_df[period_df["rptdate"].dt.date <= end_date]
    # Support both 'inspection_approved' and 'inspection' column names depending on source
    inspections_col = None
    if "inspection_approved" in period_df.columns:
        inspections_col = "inspection_approved"
    elif "inspection" in period_df.columns:
        inspections_col = "inspection"

    return {
        "applications": int(period_df["applications"].sum()) if "applications" in period_df else 0,
        "installations": int(period_df["installations"].sum()) if "installations" in period_df else 0,
        "inspections": int(period_df[inspections_col].sum()) if inspections_col is not None else 0,
        "subsidy_redeemed": int(period_df["subsidyredeemed"].sum()) if "subsidyredeemed" in period_df else 0,
    }


try:
    kpi_national, kpi_state, kpi_district, datewise, state_master, district = get_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Map the sidebar selection to an internal page key.
page = page_options[selected_page_label]

# ============================================================================
# PAGE ROUTING
# ============================================================================

if page == "Overview":
    # ========================================================================
    # OVERVIEW PAGE - Main Dashboard
    # ========================================================================

    st.write("""
    National decision snapshot of scheme performance. These indicators summarize program scale,
    delivery execution, inspection flow, and subsidy progression to support prioritization and review.
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
            title="Applications submitted",
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

    # Row 3: Trend
    st.subheader("Cumulative applications and installations over time")
    st.markdown("**Date range**")
    filtered_datewise, start_date, end_date = apply_date_range_filter(
        datewise, "overview"
    )
    if start_date and end_date:
        st.caption(f"Showing: {start_date} to {end_date}")

    if filtered_datewise.empty:
        st.info("No time-series data available for the selected range.")
    else:
        fig = create_adoption_trend(filtered_datewise)
        st.plotly_chart(fig, use_container_width=True)
        how_to_read_chart(
            [
                "Both lines are cumulative totals, so steeper slopes mean faster day-to-day additions.",
                "The vertical gap between the two lines reflects how many applications have not yet converted to installations.",
                "Use the date-range filter to compare recent momentum against longer-term performance.",
            ]
        )
        chart_caption(
            "Cumulative trend compares program intake and execution over the selected period",
            "",
            "The chart shows running totals for the selected date range.",
        )

    st.markdown("---")

    # Row 5: Conversion Funnel
    st.subheader("Application progression across tracked operational stages")
    st.caption(
        "Stages shown below represent only process steps captured in the cleaned and validated data: application submission, feasibility approval, vendor selection, installation completed, project inspection by DISCOM, and subsidy redeem."
    )

    funnel_data = {
        "Stage": [
            "Application submission",
            "Feasibility approval",
            "Vendor selection",
            "Installation completed",
            "Project inspection by DISCOM",
            "Subsidy redeem",
        ],
        "Count": [
            int(state_master["application_status"].sum()),
            int(state_master["feasibility_approved"].sum()),
            int(state_master["vendor_selected"].sum()),
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
        how_to_read_chart(
            [
                "Each funnel step shows the number of applications that have reached that stage.",
                "Large drops between adjacent stages signal potential process bottlenecks.",
                "Prioritise stage transitions with both high absolute loss and high percentage loss.",
            ]
        )
        chart_caption(
            "Funnel view shows where applications drop between operational stages",
            "",
        )

elif page == "State Analysis":
    st.header("State comparison")

    st.markdown(
        """
    **Decision use:** Compare state-level throughput and conversion to identify where intervention will have the highest impact.

    - Select a prioritization metric based on policy objective: volume coverage or conversion efficiency.
    - Low conversion rates indicate execution gaps where applications are not reaching installation.
    - High-volume, low-conversion states should be treated as priority intervention zones.
    - Use District Comparison for localized follow-up and field-level diagnosis.
    """,
        unsafe_allow_html=True,
    )

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        sort_by = st.selectbox(
            "Rank states by:",
            [
                "Applications submitted",
                "Installations completed",
                "Application-to-installation conversion rate",
            ],
            help="Choose whether to rank by volume or efficiency.",
        )

    with col2:
        show_top = st.slider(
            "Number of states to show:",
            5,
            36,
            10,
            help="Show a smaller list for a tighter comparison.",
        )

    # Optional: allow explicit selection of states to compare
    selected_states = st.multiselect(
        "Select specific states to compare (optional):",
        options=sorted(kpi_state["state"].unique().tolist()),
        help="If selected, only these states will be shown in the table and charts.",
    )

    state_base_df = kpi_state[
        [
            "state",
            "applications",
            "installations",
            "conversion_rate_app_to_install_pct",
            "subsidy_redeemed_amount",
        ]
    ].copy()
    state_base_df = filter_all_zero_rows(
        state_base_df, ["applications", "installations"]
    )
    state_base_df["installations_per_1000_applications"] = (
        state_base_df["installations"] / state_base_df["applications"] * 1000
    ).round(1)
    state_base_df["subsidy_per_installation"] = np.where(
        state_base_df["installations"] > 0,
        state_base_df["subsidy_redeemed_amount"] / state_base_df["installations"],
        0,
    ).round(0)

    # Prepare sorted data (or use explicit selection)
    if selected_states:
        state_data = state_base_df[state_base_df["state"].isin(selected_states)].copy()
    else:
        if sort_by == "Applications submitted":
            state_data = state_base_df.nlargest(show_top, "applications")
        elif sort_by == "Installations completed":
            state_data = state_base_df.nlargest(show_top, "installations")
        else:
            state_data = state_base_df.nlargest(
                show_top, "conversion_rate_app_to_install_pct"
            )

    # Display table: show a different heading when specific states are selected
    if selected_states:
        st.subheader("Selected states comparison")
        st.caption(
            f"Focused selection active — displaying {len(selected_states)} selected state(s)."
        )
    else:
        st.subheader(f"Top {show_top} states")

    # Prepare a recruiter-friendly display table
    display_table = state_data[
        [
            "state",
            "applications",
            "installations",
            "conversion_rate_app_to_install_pct",
            "installations_per_1000_applications",
        ]
    ].copy()
    display_table.columns = [
        "State",
        "Applications submitted (count)",
        "Installations completed (count)",
            "Application-to-installation conversion rate (%)",
        "Installations per 1,000 applications (normalized)",
    ]
    display_table["Applications submitted (count)"] = display_table[
        "Applications submitted (count)"
    ].apply(lambda x: f"{int(x):,}")
    display_table["Installations completed (count)"] = display_table[
        "Installations completed (count)"
    ].apply(lambda x: f"{int(x):,}")
    display_table["Application-to-installation conversion rate (%)"] = display_table[
        "Application-to-installation conversion rate (%)"
    ].apply(lambda x: f"{float(x):.1f}%")
    display_table["Installations per 1,000 applications (normalized)"] = display_table[
        "Installations per 1,000 applications (normalized)"
    ].apply(lambda x: f"{float(x):.1f}")

    st.dataframe(display_table, width="stretch", hide_index=True)
    st.caption("Normalized columns help compare efficiency, not just raw volume. Installations per 1,000 applications is a size-adjusted delivery rate.")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        state_chart_mode = st.radio(
            "Chart type",
            ["Grouped bars", "Scatter: volume vs conversion"],
            horizontal=True,
            key="state_chart_mode",
            help="Switch between absolute volume comparison and the volume-versus-conversion scatter.",
        )
        if state_chart_mode == "Grouped bars":
            st.subheader("Applications submitted and installations completed by state")
            fig = create_state_ranking_chart(state_data)
            st.plotly_chart(fig, width="stretch")
            how_to_read_chart(
                [
                    "For each state, compare the applications bar with the installations bar.",
                    "A large gap between the two bars indicates conversion or execution issues.",
                    "Use this chart with the rate chart to separate scale effects from efficiency effects.",
                ]
            )
            chart_caption(
                "Grouped bars compare applications submitted and installations completed",
                "",
            )
        else:
            st.subheader("State volume versus conversion rate")
            fig = create_state_scatter_chart(state_data)
            st.plotly_chart(fig, width="stretch")
            how_to_read_chart(
                [
                    "Each bubble is one state, positioned by application volume (x-axis) and conversion rate (y-axis).",
                    "Higher bubbles indicate stronger conversion, while farther-right bubbles indicate larger volume.",
                    "Larger bubbles represent higher subsidy redeemed amount and highlight high-impact states.",
                ]
            )
            chart_caption(
                "Scatter highlights high-volume states and conversion outliers",
                "",
            )

    with col2:
        st.subheader("Application-to-installation conversion rate by state")
        fig = px.bar(
            state_data.sort_values(
                "conversion_rate_app_to_install_pct", ascending=True
            ),
            y="state",
            x="conversion_rate_app_to_install_pct",
            orientation="h",
            title="",
            labels={
                "conversion_rate_app_to_install_pct": "Application-to-installation conversion rate (%)",
                "state": "State",
            },
            color="conversion_rate_app_to_install_pct",
            color_continuous_scale=["#ff7f0e", "#ffaa1f", "#ffcc66", "#1f77b4"],
        )
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "States are ranked by conversion rate from low to high.",
                "Focus first on states with both low conversion and high application volume in the table.",
                "Color intensity mirrors conversion rate, reinforcing the ranking order.",
            ]
        )
        chart_caption(
            "Horizontal bars rank states by application-to-installation conversion rate",
            "",
        )

elif page == "District Analysis":
    st.header("District comparison")

    st.write("""
    District-level operational performance view for targeted implementation planning.
    Use this page to identify districts requiring immediate execution support.
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
            "Applications submitted", int(filtered_data["application_status"].sum())
        )

    with col2:
        st.metric("Installations completed", int(filtered_data["installation"].sum()))

    with col3:
        apps = filtered_data["application_status"].sum()
        insts = filtered_data["installation"].sum()
        conv_rate = (insts / apps * 100) if apps > 0 else 0
        st.metric("Application-to-installation conversion rate", f"{conv_rate:.1f}%")

    # District table
    st.subheader("District performance table")

    table_col1, table_col2, table_col3 = st.columns([2, 1, 1])

    with table_col1:
        district_sort_by = st.selectbox(
            "Rank districts by:",
            [
                "Applications submitted",
                "Installations completed",
                "Application-to-installation conversion rate",
                "Inspections approved",
                "Subsidy redeemed",
            ],
            key="district_sort_by",
            help="Choose the district metric that drives the top/bottom ranking.",
        )

    with table_col2:
        district_view = st.selectbox(
            "View:",
            ["Top districts", "Bottom districts"],
            key="district_view",
            help="Switch between the highest and lowest values for the selected metric.",
        )

    with table_col3:
        rows_per_page = st.selectbox(
            "Rows per page:",
            [10, 25, 50],
            index=1,
            key="district_rows_per_page",
            help="Control how many districts appear on each page.",
        )

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
        "Applications submitted (count)",
        "Installations completed (count)",
        "Inspections approved (count)",
        "Subsidy redeemed (count)",
    ]

    display_data["Application-to-installation conversion rate (%)"] = display_data.apply(
        lambda row: (
            (row["Installations completed (count)"] / row["Applications submitted (count)"] * 100)
            if row["Applications submitted (count)"] > 0
            else 0
        ),
        axis=1,
    )
    display_data["Installations per 1,000 applications (normalized)"] = display_data.apply(
        lambda row: (
            (row["Installations completed (count)"] / row["Applications submitted (count)"] * 1000)
            if row["Applications submitted (count)"] > 0
            else 0
        ),
        axis=1,
    )

    sort_column_map = {
        "Applications submitted": "Applications submitted (count)",
        "Installations completed": "Installations completed (count)",
        "Application-to-installation conversion rate": "Application-to-installation conversion rate (%)",
        "Inspections approved": "Inspections approved (count)",
        "Subsidy redeemed": "Subsidy redeemed (count)",
    }
    sort_column = sort_column_map[district_sort_by]
    ascending = district_view == "Bottom districts"
    sorted_display_data = display_data.sort_values(
        sort_column,
        ascending=ascending,
    ).reset_index(drop=True)

    total_rows = len(sorted_display_data)
    total_pages = max((total_rows - 1) // rows_per_page + 1, 1)
    page_number = st.selectbox(
        "Page:",
        list(range(1, total_pages + 1)),
        key="district_page_number",
    )

    start_index = (page_number - 1) * rows_per_page
    end_index = start_index + rows_per_page
    page_data = sorted_display_data.iloc[start_index:end_index].copy()

    page_data["Applications submitted (count)"] = page_data["Applications submitted (count)"].map(
        lambda value: f"{int(value):,}"
    )
    page_data["Installations completed (count)"] = page_data["Installations completed (count)"].map(
        lambda value: f"{int(value):,}"
    )
    page_data["Inspections approved (count)"] = page_data["Inspections approved (count)"].map(
        lambda value: f"{int(value):,}"
    )
    page_data["Subsidy redeemed (count)"] = page_data["Subsidy redeemed (count)"].map(
        lambda value: f"{int(value):,}"
    )
    page_data["Application-to-installation conversion rate (%)"] = page_data[
        "Application-to-installation conversion rate (%)"
    ].map(lambda value: f"{float(value):.1f}%")
    page_data["Installations per 1,000 applications (normalized)"] = page_data[
        "Installations per 1,000 applications (normalized)"
    ].map(lambda value: f"{float(value):.1f}")

    st.caption(
        f"Showing rows {start_index + 1} to {min(end_index, total_rows)} of {total_rows}"
    )
    st.markdown("**How to read this table**")
    st.markdown(
        "- Use count columns for absolute workload and the normalized columns for fair comparison across districts with different scale."
    )
    st.markdown(
        "- Sort by application-to-installation conversion rate (%) to quickly find high-priority districts with execution gaps."
    )
    st.dataframe(page_data, width="stretch", hide_index=True)
    st.caption(
        "The download button exports the full filtered, sorted result set.")

    csv_data = sorted_display_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered CSV",
        data=csv_data,
        file_name=f"districts_{selected_state.replace(' ', '_').lower()}.csv",
        mime="text/csv",
    )

elif page == "Trends":
    st.header("Trend over time")

    st.write("""
    Time-series view of intake and execution. Use this section to assess momentum,
    detect delivery pressure early, and track whether conversion is improving.
    """)

    st.markdown("**Date range**")
    filtered_datewise, start_date, end_date = apply_date_range_filter(
        datewise, "trends"
    )
    if start_date and end_date:
        st.caption(f"Showing: {start_date} to {end_date}")

    if filtered_datewise.empty:
        st.info("No time-series data available for the selected range.")
        st.stop()

    trend_df = filtered_datewise[["rptdate", "applications", "installations"]].copy()
    trend_df = filter_all_zero_rows(trend_df, ["applications", "installations"])
    datewise_sorted = trend_df.sort_values("rptdate")
    datewise_sorted["rptdate"] = pd.to_datetime(datewise_sorted["rptdate"])
    datewise_sorted["cum_applications"] = datewise_sorted["applications"].cumsum()
    datewise_sorted["cum_installations"] = datewise_sorted["installations"].cumsum()
    datewise_sorted["apps_7d_avg"] = (
        datewise_sorted["applications"].rolling(window=7, min_periods=1).mean()
    )
    datewise_sorted["installs_7d_avg"] = (
        datewise_sorted["installations"].rolling(window=7, min_periods=1).mean()
    )

    # Chart type selector
    chart_type = st.radio("Choose a view:", ["Cumulative", "Daily"], horizontal=True)

    if chart_type == "Cumulative":
        st.subheader("Cumulative applications and installations over the selected period")

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
            title="Cumulative applications and installations over time",
            xaxis_title="Report date",
            yaxis_title="Cumulative applications / installations",
            hovermode="x unified",
            height=600,
            template="plotly_white",
        )

        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "Both lines are running totals, so slope changes indicate acceleration or slowdown.",
                "If the applications line grows faster than installations, execution backlog is increasing.",
                "Use this view for long-term trajectory rather than short-term volatility.",
            ]
        )
        chart_caption(
            "Cumulative view shows the running total for applications and installations",
            "",
            "Filtered to the selected date range.",
        )

    else:
        st.subheader("Daily applications and installations with 7-day averages")

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

        fig.add_trace(
            go.Scatter(
                x=datewise_sorted["rptdate"],
                y=datewise_sorted["apps_7d_avg"],
                name="Applications (7-day avg)",
                mode="lines",
                line=dict(color="#1f77b4", width=2, dash="dash"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=datewise_sorted["rptdate"],
                y=datewise_sorted["installs_7d_avg"],
                name="Installations (7-day avg)",
                mode="lines",
                line=dict(color="#ff7f0e", width=2, dash="dash"),
            )
        )

        fig.update_layout(
            title="Daily applications and installations with 7-day averages",
            xaxis_title="Report date",
            yaxis_title="Daily applications / installations",
            hovermode="x unified",
            height=600,
            template="plotly_white",
        )

        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "Solid lines are daily values, and dashed lines are 7-day moving averages.",
                "Look at dashed lines to identify persistent trend shifts beyond daily noise.",
                "Widening distance between application and installation averages suggests rising processing pressure.",
            ]
        )
        chart_caption(
            "Daily view adds 7-day averages to smooth day-to-day noise",
            "",
            "The dashed lines show the rolling average overlay.",
        )

    st.markdown("---")
    st.subheader("Weekday seasonality curve")
    st.caption(
        "Average daily applications and installations by weekday in the selected period. "
        "Use this to align staffing, inspections, and support operations by day-of-week demand."
    )

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    weekday_curve = (
        datewise_sorted.assign(weekday=datewise_sorted["rptdate"].dt.day_name())
        .groupby("weekday", as_index=False)[["applications", "installations"]]
        .mean()
    )
    weekday_curve["weekday"] = pd.Categorical(
        weekday_curve["weekday"], categories=weekday_order, ordered=True
    )
    weekday_curve = weekday_curve.sort_values("weekday")

    if weekday_curve.empty:
        st.info("No weekly seasonality data available for the selected range.")
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=weekday_curve["weekday"],
                y=weekday_curve["applications"],
                name="Applications",
                mode="lines+markers",
                line=dict(color="#1f77b4", width=3, shape="spline"),
                marker=dict(size=8),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=weekday_curve["weekday"],
                y=weekday_curve["installations"],
                name="Installations",
                mode="lines+markers",
                line=dict(color="#ff7f0e", width=3, shape="spline"),
                marker=dict(size=8),
            )
        )
        fig.update_layout(
            height=420,
            template="plotly_white",
            hovermode="x unified",
            xaxis_title="Weekday",
            yaxis_title="Average daily applications / installations",
        )
        st.plotly_chart(fig, width="stretch")
        how_to_read_chart(
            [
                "Each point is the average daily volume for that weekday across the selected range.",
                "Compare weekday peaks to plan staffing and operational schedules.",
                "Persistent weekday gaps between applications and installations indicate timing-related process imbalance.",
            ]
        )
        chart_caption(
            "Weekday curve shows whether applications and installations cluster on certain days of the week",
            "",
            "Filtered to the selected date range.",
        )

        # Provide a CSV download of the filtered trend data for user export
        try:
            csv_bytes = datewise_sorted.to_csv(index=False).encode("utf-8")
            safe_start = str(start_date).replace(' ', '_') if start_date is not None else 'start'
            safe_end = str(end_date).replace(' ', '_') if end_date is not None else 'end'
            st.download_button(
                "Download filtered trends CSV",
                data=csv_bytes,
                file_name=f"trends_{safe_start}_{safe_end}.csv",
                mime="text/csv",
            )
        except Exception:
            # If download fails for any reason, do not block the page
            pass

    # Installation lag distribution chart removed per project policy: only show charts
    # that are directly supported by case-level data. See project notes in progress.txt.

elif page == "Capacity Metrics":
    st.header("Capacity and system size")

    st.write("""
    Capacity profile view summarizing installed capacity, system-size patterns,
    and residential versus RWA mix for infrastructure and financing decisions.
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
        st.subheader("Residential and RWA share of installed capacity")

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
            fig.update_layout(legend_title_text="System category")
            st.plotly_chart(fig, width="stretch")
            how_to_read_chart(
                [
                    "Each slice shows the share of completed installations by system category.",
                    "Larger slices indicate where the scheme is currently concentrated.",
                    "Use this split to communicate portfolio mix to non-technical stakeholders.",
                ]
            )
            chart_caption(
                "Pie chart shows the residential and RWA mix",
                "",
            )

    with col2:
        st.subheader("System size distribution by kW bucket")

        # Date range filter for capacity view
        st.markdown("**Date range (Capacity view)**")
        cap_filtered_datewise, cap_start, cap_end = apply_date_range_filter(
            datewise, "capacity"
        )
        if cap_start and cap_end:
            st.caption(f"Showing: {cap_start} → {cap_end}")

        # If there is a per-installation 'system_size_kw' column, bucket into 0-1,1-2,...,>10
        if cap_filtered_datewise is not None and "system_size_kw" in cap_filtered_datewise.columns:
            bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, float("inf")]
            labels = ["0-1 kW", "1-2 kW", "2-3 kW", "3-4 kW", "4-5 kW", "5-6 kW", "6-7 kW", "7-8 kW", "8-9 kW", "9-10 kW", ">10 kW"]
            cap_filtered_datewise["size_bucket"] = pd.cut(cap_filtered_datewise["system_size_kw"], bins=bins, labels=labels, right=False)
            bucket_counts = cap_filtered_datewise["size_bucket"].value_counts().reindex(labels).fillna(0).astype(int)
            capacity_df = pd.DataFrame({"Size": labels, "Count": bucket_counts.values})
            median_band = capacity_df.loc[capacity_df["Count"].cumsum() >= capacity_df["Count"].sum() / 2, "Size"].iloc[0]
            import plotly.express as px

            if capacity_df["Count"].sum() == 0:
                st.info("No system-size records available for the selected range.")
            else:
                fig = px.bar(
                    capacity_df,
                    x="Size",
                    y="Count",
                    color="Size",
                    title="System size counts by kW bucket",
                )
                fig.update_layout(
                    showlegend=True,
                    legend_title_text="System size bucket",
                    height=420,
                    xaxis_title="Installed system size bucket (kW)",
                    yaxis_title="Number of installations",
                )
                st.plotly_chart(fig, width="stretch")
                how_to_read_chart(
                    [
                        "Bars show how many installations fall into each system-size bucket.",
                        "The tallest bar identifies the most common installed size range.",
                        "Use the median size band metric to summarize the center of the distribution.",
                    ]
                )

            st.metric("Median size band", median_band)
            st.caption(
                "The chart uses the per-installation system size column when available."
            )
        else:
            # Fallback to available aggregate buckets
            upto_10kw = cap_filtered_datewise["upto_10_kw"].sum() if cap_filtered_datewise is not None else datewise["upto_10_kw"].sum()
            above_10kw = cap_filtered_datewise["above_10_kw"].sum() if cap_filtered_datewise is not None else datewise["above_10_kw"].sum()
            total_systems = upto_10kw + above_10kw
            median_band = "Up to 10 kW" if upto_10kw >= (total_systems / 2) else "Above 10 kW"

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
                    title="System size counts by kW bucket",
                )
                fig.update_layout(
                    showlegend=True,
                    legend_title_text="System size bucket",
                    height=400,
                    xaxis_title="Installed system size bucket",
                    yaxis_title="Number of installations",
                )
                st.plotly_chart(fig, width="stretch")
                how_to_read_chart(
                    [
                        "This fallback chart splits installations into up to 10 kW and above 10 kW categories.",
                        "Compare bar heights to understand concentration by broad system size segment.",
                        "For finer analysis, provide case-level system_size_kw in cleaned data.",
                    ]
                )

            st.caption(
                "Histogram-style bucket view based on the available system-size counts in the cleaned data. Finer per-installation buckets require a 'system_size_kw' column in the cleaned dataset."
            )
            st.metric("Median size band", median_band)
            st.caption(
                "The median is shown as the bucket containing the midpoint, not a per-installation median.")

elif page == "Bottleneck Analysis":
    # Execute the Bottleneck Analysis page as a standalone script so its Streamlit
    # content renders in place. The page file name begins with digits so importlib
    # can't import it as a regular module; use runpy to execute the file by path.
    runpy.run_path(
        str(project_root / "dashboard" / "pages" / "08_bottleneck_analysis.py"),
        run_name="__main__",
    )

elif page == "About":
    st.header("About this dashboard")

    st.markdown("""
    ### PM Surya Ghar Analytics

    This dashboard provides a decision-support view of PM Surya Ghar implementation performance.
    It is designed to help scheme stakeholders monitor scale, track execution quality,
    and identify operational bottlenecks requiring timely action.

    **What this dashboard covers:**
    - **Time Period:** February 13, 2024 – February 9, 2026
    - **Geography:** 36 States/UTs, 792 Districts, 84 DISCOMs
    - **Records Reviewed:** 6,021,454 applications

    **Journey stages captured in this dataset:**
    Application submission → Feasibility approval → Vendor selection → Installation completed → Project inspection by DISCOM → Subsidy redeem

    *Note:* Consumer registration, agreement upload, and subsidy approval or disbursal are not captured in the source data.

    **Main numbers:**
    - Applications submitted: 6,021,454
    - Installations completed: 2,329,586
    - Application to installation rate: 38.69%
    - Installed capacity: 8.56 million kW

    **Data assurance and validation:**
    - Cleaned source files before analysis
    - Cross-verified KPI totals against cleaned datasets
    - Validated geography-level record counts
    - Maintained consistent metric definitions across pages
    - Documented KPI definitions in docs/metric_glossary.md

    **Decision views available:**
    - **Overview:** national performance snapshot and stage progression
    - **State Analysis:** comparative state performance on volume and conversion
    - **District Analysis:** district-level operational performance for targeted action
    - **Trends:** time-based movement in intake and installations

    **Built with:**
    - Python 3.11, Streamlit, Pandas, and Plotly
    - Simple checks for data cleaning and validation
    - Interactive charts with hover details
    - Responsive layout for desktop and mobile

    **Version:** 1.0.0  
    **Last Updated:** May 29, 2026  
    **Status:** Production Ready
    """)

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
    PM Surya Ghar Analytics Dashboard | Decision-support insights for scheme delivery
    </div>
    """,
        unsafe_allow_html=True,
    )
