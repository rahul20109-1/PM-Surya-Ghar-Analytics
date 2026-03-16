"""
Data Loader Module
Loads and caches raw CSV datasets from raw_data/ folder.
"""

import os
import pandas as pd
from pathlib import Path


def get_raw_data_path():
    """Get path to raw_data folder (assumes standard project structure)."""
    current_dir = Path(__file__).parent.parent  # Go up from scripts/ to project root
    raw_data_path = current_dir / "raw_data"

    if not raw_data_path.exists():
        raise FileNotFoundError(f"raw_data folder not found at {raw_data_path}")

    return raw_data_path


def load_datewise_csv():
    """
    Load datewise.csv — Daily aggregated metrics (time-series).

    Returns:
        pandas.DataFrame with columns:
        - rptdate: Report date
        - applications, residential, rwa, totalhouseholds
        - upto_10_kw, above_10_kw
        - installations, inspection, subsidyredeemed
    """
    path = get_raw_data_path() / "datewise.csv"
    df = pd.read_csv(path)
    return df


def load_state_master_csv():
    """
    Load state_master.csv — State-level aggregated summary.

    Returns:
        pandas.DataFrame with 36 rows (states) and ~35 columns
    """
    path = get_raw_data_path() / "state_master.csv"
    df = pd.read_csv(path)
    return df


def load_district_csv():
    """
    Load district.csv — State × District granular breakdown.

    Returns:
        pandas.DataFrame with ~700 rows (state-district combos)
    """
    path = get_raw_data_path() / "district.csv"
    df = pd.read_csv(path)
    return df


def load_discom_master_csv():
    """
    Load discom_master.csv — Electricity distribution company level.

    Returns:
        pandas.DataFrame with ~300 rows (state-discom combos)
    """
    path = get_raw_data_path() / "discom_master.csv"
    df = pd.read_csv(path)
    return df


def load_subsidy_status_csv():
    """
    Load subsidy_status.csv — Current subsidy processing pipeline snapshot.

    Returns:
        pandas.DataFrame with pipeline stages and counts
    """
    path = get_raw_data_path() / "subsidy_status.csv"
    df = pd.read_csv(path)
    return df


def load_vendor_selection_csv():
    """
    Load vendor_selection.csv — Vendor selection request approval process.

    Returns:
        pandas.DataFrame with state-discom vendor metrics
    """
    path = get_raw_data_path() / "vendor_selection.csv"
    df = pd.read_csv(path)
    return df


def load_all_datasets():
    """
    Load all 6 raw datasets at once.

    Returns:
        dict with keys: datewise, state_master, district, discom_master,
                        subsidy_status, vendor_selection
    """
    datasets = {
        "datewise": load_datewise_csv(),
        "state_master": load_state_master_csv(),
        "district": load_district_csv(),
        "discom_master": load_discom_master_csv(),
        "subsidy_status": load_subsidy_status_csv(),
        "vendor_selection": load_vendor_selection_csv(),
    }
    return datasets


if __name__ == "__main__":
    # Test: load all datasets
    print("Loading all datasets...")
    datasets = load_all_datasets()

    for name, df in datasets.items():
        print(f"\n{name}:")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)[:5]}...")  # First 5 columns
