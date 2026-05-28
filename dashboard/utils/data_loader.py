"""
Data Loading and Caching Utilities
===================================
Handles loading and caching of cleaned data files with error handling.
"""

import pandas as pd
from pathlib import Path
import streamlit as st


@st.cache_data
def load_data():
    """
    Load all cleaned data files with error handling.

    Returns:
        tuple: (kpi_national, kpi_state, kpi_district, datewise, state_master, district)
    """

    # Determine data directory
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data_cleaned"

    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    try:
        # Load KPI files
        kpi_national = pd.read_csv(data_dir / "kpis_national.csv")
        kpi_state = pd.read_csv(data_dir / "kpis_state.csv")
        kpi_district = pd.read_csv(data_dir / "kpis_district.csv")

        # Load detail data files
        datewise = pd.read_csv(data_dir / "datewise_clean.csv")
        if "rptdate" in datewise.columns:
            launch_date = pd.Timestamp("2024-02-13")
            date_series = pd.to_datetime(datewise["rptdate"], errors="coerce")
            datewise = datewise.loc[date_series >= launch_date].copy()
            datewise["rptdate"] = date_series.loc[
                date_series >= launch_date
            ].dt.strftime("%Y-%m-%d")
        state_master = pd.read_csv(data_dir / "state_master_clean.csv")
        district = pd.read_csv(data_dir / "district_clean.csv")

        return kpi_national, kpi_state, kpi_district, datewise, state_master, district

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Failed to load data files: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")


def apply_date_range_filter(df, key_prefix=None):
    """
    Helper: apply a date-range selection UI and filter a dataframe with 'rptdate'.

    Returns: (filtered_df, start_date, end_date)
    """
    import streamlit as st

    df = df.copy()
    if "rptdate" not in df.columns:
        return df, None, None

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
        key=(f"{key_prefix}_preset" if key_prefix else None),
        help="Pick a common date window or switch to Custom for an exact from/to range.",
    )

    if preset == "Custom":
        start_date, end_date = st.date_input(
            "Custom range",
            value=(default_start, max_date),
            key=(f"{key_prefix}_custom" if key_prefix else None),
            help="Choose the exact start and end dates for the chart.",
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

    mask = (df["rptdate"].dt.date >= start_date) & (df["rptdate"].dt.date <= end_date)
    filtered = df.loc[mask].copy()
    return filtered, start_date, end_date
