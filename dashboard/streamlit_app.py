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
from dashboard.utils.components import kpi_card, create_conversion_funnel, chart_caption
from dashboard.utils.charts import (
    create_adoption_trend,
    create_state_scatter_chart,
    create_state_ranking_chart,
    filter_all_zero_rows,
)

# Configure Streamlit
st.set_page_config(
    page_title="PM Surya Ghar Analytics",
    page_icon="ÔÿÇ´©Å",
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
    '<div class="sub-header">Clear, unambiguous view of program scale, progress, and operational bottlenecks</div>',
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
        start_date, end_date = st.date_input(
            "Custom range",
            value=(default_start, max_date),
            key=f"{key_prefix}_custom",
        )
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

    return {
        "applications": int(period_df["applications"].sum()) if "applications" in period_df else 0,
        "installations": int(period_df["installations"].sum()) if "installations" in period_df else 0,
        "inspections": int(period_df["inspection_approved"].sum()) if "inspection_approved" in period_df else 0,
        "subsidy_redeemed": int(period_df["subsidyredeemed"].sum()) if "subsidyredeemed" in period_df else 0,
    }


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
    Quick snapshot of program scale and operational progress. Use these numbers to understand program reach (volume), execution (installations and inspections), and financial progress (subsidy redeemed).
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

    st.subheader("Applications and installations over time")

    # For KPI deltas default to the last 12 months window (so KPIs remain cumulative while deltas are meaningful)
    datewise_local = datewise.copy()
    datewise_local["rptdate"] = pd.to_datetime(datewise_local["rptdate"], errors="coerce")
    datewise_local = datewise_local.dropna(subset=["rptdate"]) if not datewise_local.empty else datewise_local
    if datewise_local.empty:
        current_window = {"applications": 0, "installations": 0, "inspections": 0, "subsidy_redeemed": 0}
        previous_window = current_window.copy()
    else:
        min_date = datewise_local["rptdate"].min().date()
        max_date = datewise_local["rptdate"].max().date()
        default_start = (pd.Timestamp(max_date) - pd.Timedelta(days=365)).date()
        if default_start < min_date:
            default_start = min_date
        selected_days = max((max_date - default_start).days + 1, 1)
        previous_end = (pd.Timestamp(default_start) - pd.Timedelta(days=1)).date()
        previous_start = (pd.Timestamp(previous_end) - pd.Timedelta(days=selected_days - 1)).date()
        current_window = summarize_period_totals(datewise_local, default_start, max_date)
        previous_window = summarize_period_totals(datewise_local, previous_start, previous_end)

    current_gap = current_window["applications"] - current_window["installations"]
    previous_gap = previous_window["applications"] - previous_window["installations"]

    app_delta = current_window["applications"] - previous_window["applications"]
    install_delta = current_window["installations"] - previous_window["installations"]
    inspection_delta = current_window["inspections"] - previous_window["inspections"]
    subsidy_delta = current_window["subsidy_redeemed"] - previous_window["subsidy_redeemed"]
    app_to_install_delta = (
        (current_window["installations"] / current_window["applications"] * 100)
        if current_window["applications"] > 0
        else 0
    ) - (
        (previous_window["installations"] / previous_window["applications"] * 100)
        if previous_window["applications"] > 0
        else 0
    )
    install_to_inspection_delta = (
        (current_window["inspections"] / current_window["installations"] * 100)
        if current_window["installations"] > 0
        else 0
    ) - (
        (previous_window["inspections"] / previous_window["installations"] * 100)
        if previous_window["installations"] > 0
        else 0
    )
    app_to_subsidy_delta = (
        (current_window["subsidy_redeemed"] / current_window["applications"] * 100)
        if current_window["applications"] > 0
        else 0
    ) - (
        (previous_window["subsidy_redeemed"] / previous_window["applications"] * 100)
        if previous_window["applications"] > 0
        else 0
    )
    gap_delta = current_gap - previous_gap

    # Row 1: Core volume metrics (cumulative national totals)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            title="Applications submitted",
            value=total_apps,
            delta=f"{app_delta:+,}",
            format_type="number",
        )

    with col2:
        kpi_card(
            title="Installations completed",
            value=total_installs,
            delta=f"{install_delta:+,}",
            format_type="number",
        )

    with col3:
        kpi_card(
            title="Inspections approved",
            value=total_inspections,
            delta=f"{inspection_delta:+,}",
            format_type="number",
        )

    with col4:
        kpi_card(
            title="Subsidy redeemed amount",
            value=total_subsidy_redeemed_crore,
            delta=f"{subsidy_delta / 1e7:+,.2f} crore",
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
            delta=f"{app_to_install_delta:+.1f} pp",
            format_type="percent",
        )

    with col2:
        kpi_card(
            title="Installation to inspection rate",
            value=install_to_inspection_rate,
            delta=f"{install_to_inspection_delta:+.1f} pp",
            format_type="percent",
        )

    with col3:
        kpi_card(
            title="Application to subsidy rate",
            value=app_to_subsidy_rate,
            delta=f"{app_to_subsidy_delta:+.1f} pp",
            format_type="percent",
        )

    with col4:
        kpi_card(
            title="Applications not yet installed",
            value=apps_not_installed,
            delta=f"{gap_delta:+,}",
            format_type="number",
        )

    st.caption(
        "KPI deltas compare the selected date range with the immediately preceding period of the same length."
    )

    st.markdown("---")

    chart_filter_col, chart_spacer_col = st.columns([1, 3])
    with chart_filter_col:
        st.markdown("**Date range**")
        filtered_datewise, start_dt, end_dt = apply_date_range_filter(datewise, "overview")
        if start_dt and end_dt:
            st.caption(f"Showing: {start_dt} → {end_dt}")

    if filtered_datewise.empty:
        st.info("No time-series data available for the selected range.")
    else:
        fig = create_adoption_trend(filtered_datewise, start_date=start_dt, end_date=end_dt)
        st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    # Row 5: Conversion Funnel
    st.subheader("How applications move through journey stages captured in the data")
    st.caption(
        "Stages shown below reflect the scheme journey steps available in the source data. "
        "Consumer registration, agreement upload, and subsidy approval or disbursal are not captured in this dataset."
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
        st.plotly_chart(fig, width="stretch")

elif page == "State Analysis":
    st.header("State comparison")

    st.markdown(
        """
    **What this view does:** Compare state performance on volume and conversion.

    - Use the selector to choose a prioritisation metric: raw application or installation volume, or the conversion rate from application ÔåÆ installation.
    - Lower conversion rates point to places where applications are not turning into completed installations. High volumes with low conversion are high-priority operational issues.
    - Use the charts to spot which states have high throughput and which lag on execution. Drill down using the District page for local diagnostics.
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
                "Application to installation rate",
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
        options=sorted(state_base_df["state"].tolist()),
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

    # Display table
    if selected_states:
        st.subheader(f"Selected states ({len(selected_states)})")
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
            "subsidy_per_installation",
        ]
    ].copy()
    display_table.columns = [
        "State",
        "Applications submitted",
        "Installations completed",
        "Application → Installation (%)",
        "Installations per 1,000 applications",
        "Subsidy per installation (₹)",
    ]
    display_table["Applications submitted"] = display_table[
        "Applications submitted"
    ].apply(lambda x: f"{int(x):,}")
    display_table["Installations completed"] = display_table[
        "Installations completed"
    ].apply(lambda x: f"{int(x):,}")
    display_table["Application ÔåÆ Installation (%)"] = display_table[
        "Application ÔåÆ Installation (%)"
    ].apply(lambda x: f"{float(x):.1f}%")
    display_table["Installations per 1,000 applications"] = display_table[
        "Installations per 1,000 applications"
    ].apply(lambda x: f"{float(x):.1f}")
    display_table["Subsidy per installation (₹)"] = display_table[
        "Subsidy per installation (₹)"
    ].apply(lambda x: f"₹{float(x):,.0f}")

    st.dataframe(display_table, width="stretch", hide_index=True)
    st.caption("Source: kpis_state.csv. The table is sorted and filtered to the top states for the selected metric.")
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
            st.subheader("Applications and installations by state")
            fig = create_state_ranking_chart(state_data)
            st.plotly_chart(fig, width="stretch")
            chart_caption(
                "Grouped bars compare applications submitted and installations completed",
                "Source: kpis_state.csv columns applications and installations.",
            )
        else:
            st.subheader("State volume vs conversion")
            fig = create_state_scatter_chart(state_data)
            st.plotly_chart(fig, width="stretch")
            chart_caption(
                "Scatter highlights high-volume states and conversion outliers",
                "Source: kpis_state.csv columns applications, conversion_rate_app_to_install_pct, and subsidy_redeemed_amount.",
            )

    with col2:
        st.subheader("Application to installation rate by state")
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
        st.plotly_chart(fig, width="stretch")
        chart_caption(
            "Horizontal bars rank states by application-to-installation rate",
            "Source: kpis_state.csv column conversion_rate_app_to_install_pct.",
        )

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
            "Applications submitted", int(filtered_data["application_status"].sum())
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

    table_col1, table_col2, table_col3 = st.columns([2, 1, 1])

    with table_col1:
        district_sort_by = st.selectbox(
            "Rank districts by:",
            [
                "Applications submitted",
                "Installations completed",
                "Application to installation rate",
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
        "Applications submitted",
        "Installations completed",
        "Inspections approved",
        "Subsidy redeemed",
    ]

    display_data["Application to installation rate"] = display_data.apply(
        lambda row: (
            (row["Installations completed"] / row["Applications submitted"] * 100)
            if row["Applications submitted"] > 0
            else 0
        ),
        axis=1,
    )
    display_data["Installations per 1,000 applications"] = display_data.apply(
        lambda row: (
            (row["Installations completed"] / row["Applications submitted"] * 1000)
            if row["Applications submitted"] > 0
            else 0
        ),
        axis=1,
    )

    sort_column_map = {
        "Applications submitted": "Applications submitted",
        "Installations completed": "Installations completed",
        "Application to installation rate": "Application to installation rate",
        "Inspections approved": "Inspections approved",
        "Subsidy redeemed": "Subsidy redeemed",
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

    page_data["Applications submitted"] = page_data["Applications submitted"].map(
        lambda value: f"{int(value):,}"
    )
    page_data["Installations completed"] = page_data["Installations completed"].map(
        lambda value: f"{int(value):,}"
    )
    page_data["Inspections approved"] = page_data["Inspections approved"].map(
        lambda value: f"{int(value):,}"
    )
    page_data["Subsidy redeemed"] = page_data["Subsidy redeemed"].map(
        lambda value: f"{int(value):,}"
    )
    page_data["Application to installation rate"] = page_data[
        "Application to installation rate"
    ].map(lambda value: f"{float(value):.1f}%")
    page_data["Installations per 1,000 applications"] = page_data[
        "Installations per 1,000 applications"
    ].map(lambda value: f"{float(value):.1f}")

    st.caption(
        f"Showing rows {start_index + 1} to {min(end_index, total_rows)} of {total_rows}"
    )
    st.dataframe(page_data, width="stretch", hide_index=True)
    st.caption(
        "Source: district_clean.csv. The download button exports the full filtered, sorted result set.")

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
    Review how applications and installations change over time.
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

        st.plotly_chart(fig, width="stretch")
        chart_caption(
            "Cumulative view shows the running total for applications and installations",
            "Source: datewise_clean.csv columns rptdate, applications, and installations.",
            "Filtered to the selected date range.",
        )

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
            title="Daily program activity",
            xaxis_title="Date",
            yaxis_title="Daily count",
            hovermode="x unified",
            height=600,
            template="plotly_white",
        )

        st.plotly_chart(fig, width="stretch")
        chart_caption(
            "Daily view adds 7-day averages to smooth day-to-day noise",
            "Source: datewise_clean.csv columns rptdate, applications, and installations.",
            "The dashed lines show the rolling average overlay.",
        )

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
            st.plotly_chart(fig, width="stretch")
            chart_caption(
                "Pie chart shows the residential and RWA mix",
                "Source: kpis_national.csv columns residential_percentage and rwa_percentage.",
            )

    with col2:
        st.subheader("System size distribution")

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
                    title="System size counts",
                )
                fig.update_layout(showlegend=False, height=420)
                st.plotly_chart(fig, width="stretch")

            st.metric("Median size band", median_band)
            st.caption(
                "Source: per-installation system size column 'system_size_kw' in the cleaned data."
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
                    title="System size counts",
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, width="stretch")

            st.caption(
                "Histogram-style bucket view based on the available system-size counts in the cleaned data. Finer per-installation buckets require a 'system_size_kw' column in the cleaned dataset."
            )
            st.metric("Median size band", median_band)
            st.caption(
                "Source: datewise_clean.csv columns upto_10_kw and above_10_kw. The median is shown as the bucket containing the midpoint, not a per-installation median.")

elif page == "About":
    st.header("About this dashboard")

    st.markdown("""
    ### PM Surya Ghar Analytics

    This dashboard shows how the PM Surya Ghar rooftop solar scheme is moving through each stage.
    The aim is simple: make the data easy to read, show where applications move smoothly,
    and make the problem areas easy to spot.

    **What this dashboard covers:**
    - **Time Period:** February 13, 2024 ÔÇô February 9, 2026
    - **Geography:** 36 States/UTs, 792 Districts, 84 DISCOMs
    - **Records Reviewed:** 6,021,454 applications

    **Journey stages captured in this dataset:**
    Application submission ÔåÆ Feasibility approval ÔåÆ Vendor selection ÔåÆ Installation completed ÔåÆ Project inspection by DISCOM ÔåÆ Subsidy redeem

    *Note:* Consumer registration, agreement upload, and subsidy approval or disbursal are not captured in the source data.

    **Main numbers:**
    - Applications submitted: 6,021,454
    - Installations completed: 2,329,586
    - Application to installation rate: 38.69%
    - Installed capacity: 8.56 million kW

    **What we checked:**
    - cleaned the source files before analysis
    - cross-checked the KPI totals against the cleaned data
    - reviewed the geography level counts
    - kept the dashboard focused on the main numbers first
    - documented KPI definitions in docs/metric_glossary.md

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
    **Last Updated:** May 27, 2026  
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
