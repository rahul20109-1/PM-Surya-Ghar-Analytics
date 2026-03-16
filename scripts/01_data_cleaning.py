"""
Data Cleaning Pipeline
Transforms raw datasets into clean, validated, analysis-ready form.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
import importlib.util

# Import parser module
spec = importlib.util.spec_from_file_location(
    "parser",
    str(Path(__file__).parent / "utils" / "parser.py")
)
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)
parse_indian_number_column = parser.parse_indian_number_column


def standardize_column_names(df):
    """
    Standardize column names: lowercase, strip whitespace, replace spaces/hyphens with underscores.
    
    Args:
        df: pandas DataFrame with original column names
    
    Returns:
        DataFrame with standardized column names
    """
    df.columns = (df.columns
                  .str.lower()
                  .str.strip()
                  .str.replace(' ', '_')
                  .str.replace('-', '_')
                  .str.replace('(', '')
                  .str.replace(')', '')
                  .str.replace('.', ''))
    return df


def remove_trailing_empty_columns(df):
    """
    Remove columns that are entirely empty (created by CSV trailing commas).
    
    Args:
        df: pandas DataFrame
    
    Returns:
        DataFrame without empty columns
    """
    return df.dropna(axis=1, how='all')


def clean_numeric_columns(df, numeric_cols=None):
    """
    Convert string numbers in Indian format to integers/floats.
    
    Args:
        df: pandas DataFrame
        numeric_cols: List of column names to convert. If None, auto-detect.
    
    Returns:
        DataFrame with numeric columns parsed
    """
    df = df.copy()
    
    # Auto-detect numeric columns if not specified
    if numeric_cols is None:
        numeric_cols = []
        for col in df.columns:
            # Try to detect if column looks numeric
            sample = df[col].dropna().head(10)
            if sample.empty:
                continue
            first_val = str(sample.iloc[0])
            # If contains numbers and commas, likely numeric
            if any(c.isdigit() for c in first_val):
                numeric_cols.append(col)
    
    # Parse each numeric column
    for col in numeric_cols:
        if col in df.columns:
            df[col] = parse_indian_number_column(df[col])
    
    return df


def clean_datewise(df):
    """
    Clean datewise.csv dataset.
    
    Args:
        df: Raw datewise DataFrame
    
    Returns:
        Cleaned DataFrame with proper types
    """
    df = df.copy()
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Remove trailing empty columns
    df = remove_trailing_empty_columns(df)
    
    # Parse date column
    if 'rptdate' in df.columns:
        df['rptdate'] = pd.to_datetime(df['rptdate'], format='%d-%m-%Y')
    
    # Parse numeric columns
    numeric_cols = [c for c in df.columns if c != 'rptdate']
    df = clean_numeric_columns(df, numeric_cols)
    
    # Fill missing values in counts with 0
    count_cols = [c for c in df.columns if df[c].dtype in ['int64', 'float64']]
    df[count_cols] = df[count_cols].fillna(0)
    
    # Sort by date descending (latest first)
    df = df.sort_values('rptdate', ascending=False).reset_index(drop=True)
    
    return df


def clean_state_master(df):
    """
    Clean state_master.csv dataset.
    
    Args:
        df: Raw state_master DataFrame
    
    Returns:
        Cleaned DataFrame with proper types
    """
    df = df.copy()
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Remove trailing empty columns
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns (all except 'state')
    numeric_cols = [c for c in df.columns if c != 'state']
    df = clean_numeric_columns(df, numeric_cols)
    
    # Fill missing values with 0
    numeric_cols_in_df = [c for c in numeric_cols if c in df.columns and df[c].dtype in ['int64', 'float64']]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    
    return df


def clean_district(df):
    """
    Clean district.csv dataset.
    
    Args:
        df: Raw district DataFrame
    
    Returns:
        Cleaned DataFrame with proper types
    """
    df = df.copy()
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Remove trailing empty columns
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns (all except 'state', 'district')
    numeric_cols = [c for c in df.columns if c not in ['state', 'district']]
    df = clean_numeric_columns(df, numeric_cols)
    
    # Fill missing values with 0
    numeric_cols_in_df = [c for c in numeric_cols if c in df.columns and df[c].dtype in ['int64', 'float64']]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    
    return df


def clean_discom_master(df):
    """
    Clean discom_master.csv dataset.
    
    Args:
        df: Raw discom_master DataFrame
    
    Returns:
        Cleaned DataFrame with proper types
    """
    df = df.copy()
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Remove trailing empty columns
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns (all except 'state', 'discom')
    numeric_cols = [c for c in df.columns if c not in ['state', 'discom']]
    df = clean_numeric_columns(df, numeric_cols)
    
    # Fill missing values with 0
    numeric_cols_in_df = [c for c in numeric_cols if c in df.columns and df[c].dtype in ['int64', 'float64']]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    
    return df


def clean_subsidy_status(df):
    """
    Clean subsidy_status.csv dataset.
    
    Args:
        df: Raw subsidy_status DataFrame
    
    Returns:
        Cleaned DataFrame with proper types
    """
    df = df.copy()
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Remove trailing empty columns
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns (all except 'statuses')
    numeric_cols = [c for c in df.columns if c not in ['statuses']]
    df = clean_numeric_columns(df, numeric_cols)
    
    return df


def clean_vendor_selection(df):
    """
    Clean vendor_selection.csv dataset.
    
    Args:
        df: Raw vendor_selection DataFrame
    
    Returns:
        Cleaned DataFrame with proper types
    """
    df = df.copy()
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Remove trailing empty columns
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns (all except location strings)
    numeric_cols = [c for c in df.columns if c not in ['sl_no', 'state', 'discom']]
    df = clean_numeric_columns(df, numeric_cols)
    
    # Fill missing values with 0
    numeric_cols_in_df = [c for c in numeric_cols if c in df.columns and df[c].dtype in ['int64', 'float64']]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    
    return df


def clean_all_datasets(raw_datasets):
    """
    Clean all raw datasets.
    
    Args:
        raw_datasets: Dict with keys 'datewise', 'state_master', etc.
    
    Returns:
        Dict with cleaned datasets
    """
    cleaned = {
        'datewise': clean_datewise(raw_datasets['datewise']),
        'state_master': clean_state_master(raw_datasets['state_master']),
        'district': clean_district(raw_datasets['district']),
        'discom_master': clean_discom_master(raw_datasets['discom_master']),
        'subsidy_status': clean_subsidy_status(raw_datasets['subsidy_status']),
        'vendor_selection': clean_vendor_selection(raw_datasets['vendor_selection']),
    }
    return cleaned


def save_cleaned_datasets(cleaned_datasets):
    """
    Save cleaned datasets to data_cleaned/ folder.
    
    Args:
        cleaned_datasets: Dict with cleaned dataframes
    """
    output_path = Path(__file__).parent.parent / "data_cleaned"
    output_path.mkdir(exist_ok=True)
    
    mapping = {
        'datewise': 'datewise_clean.csv',
        'state_master': 'state_master_clean.csv',
        'district': 'district_clean.csv',
        'discom_master': 'discom_master_clean.csv',
        'subsidy_status': 'subsidy_status_clean.csv',
        'vendor_selection': 'vendor_selection_clean.csv',
    }
    
    for key, filename in mapping.items():
        if key in cleaned_datasets:
            filepath = output_path / filename
            cleaned_datasets[key].to_csv(filepath, index=False)
            print(f"✓ Saved {key} → {filepath}")


if __name__ == "__main__":
    # Import data_loader using importlib
    spec_loader = importlib.util.spec_from_file_location(
        "data_loader",
        str(Path(__file__).parent / "00_data_loader.py")
    )
    data_loader = importlib.util.module_from_spec(spec_loader)
    spec_loader.loader.exec_module(data_loader)
    load_all_datasets = data_loader.load_all_datasets
    
    print("Loading raw datasets...")
    raw_datasets = load_all_datasets()
    
    print("\nCleaning datasets...")
    cleaned_datasets = clean_all_datasets(raw_datasets)
    
    print("\nCleaned dataset shapes:")
    for name, df in cleaned_datasets.items():
        print(f"  {name}: {df.shape}")
    
    print("\nSaving cleaned datasets...")
    save_cleaned_datasets(cleaned_datasets)
    
    print("\n✅ Data cleaning complete!")
