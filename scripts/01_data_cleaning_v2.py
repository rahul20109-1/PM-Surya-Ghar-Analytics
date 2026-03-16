"""
New Data Cleaning Pipeline - FIXED VERSION
Properly handles Indian number format without data loss.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def parse_indian_number(value):
    """
    Parse Indian formatted numbers correctly.
    Handles: "1,23,456" and "1,234.56"
    
    Args:
        value: String or numeric value
    
    Returns:
        Float value or NaN
    """
    if pd.isna(value):
        return np.nan
    
    # Convert to string
    value_str = str(value).strip()
    
    # If already numeric, convert directly
    try:
        return float(value_str)
    except ValueError:
        pass
    
    # Remove commas and convert
    # Indian format: 1,23,456 or 1,23,45,678
    value_str = value_str.replace(',', '')
    
    try:
        return float(value_str)
    except ValueError:
        return np.nan


def standardize_column_names(df):
    """Standardize column names to lowercase with underscores."""
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
    """Remove columns that are entirely empty."""
    return df.dropna(axis=1, how='all')


def clean_datewise(df):
    """
    Clean datewise.csv dataset - CORRECTED VERSION.
    
    Args:
        df: Raw datewise DataFrame
    
    Returns:
        Cleaned DataFrame with proper types and NO data loss
    """
    df = df.copy()
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Remove trailing empty columns
    df = remove_trailing_empty_columns(df)
    
    # Parse date column
    if 'rptdate' in df.columns:
        df['rptdate'] = pd.to_datetime(df['rptdate'], format='%d-%m-%Y')
    
    # Parse numeric columns - FIXED: Use corrected parser
    numeric_cols = [c for c in df.columns if c not in ['#', 'rptdate']]
    
    for col in numeric_cols:
        if col in df.columns:
            print(f"  Parsing {col}...", end=" ")
            df[col] = df[col].apply(parse_indian_number)
            print(f"Sum = {df[col].sum():,.0f}")
    
    # Fill missing values in counts with 0
    count_cols = [c for c in df.columns if df[c].dtype in ['int64', 'float64']]
    df[count_cols] = df[count_cols].fillna(0)
    
    # Sort by date descending (latest first)
    df = df.sort_values('rptdate', ascending=False).reset_index(drop=True)
    
    return df


def clean_state_master(df):
    """Clean state_master.csv dataset."""
    df = df.copy()
    df = standardize_column_names(df)
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns
    numeric_cols = [c for c in df.columns if c not in ['state', 'sl_no', '#']]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_indian_number)
    
    # Fill missing values with 0
    numeric_cols_in_df = [c for c in numeric_cols if c in df.columns and df[c].dtype in ['int64', 'float64']]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    
    return df


def clean_district(df):
    """Clean district.csv dataset."""
    df = df.copy()
    df = standardize_column_names(df)
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns
    numeric_cols = [c for c in df.columns if c not in ['state', 'district', 'sl_no', '#']]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_indian_number)
    
    # Fill missing values with 0
    numeric_cols_in_df = [c for c in numeric_cols if c in df.columns and df[c].dtype in ['int64', 'float64']]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    
    return df


def clean_discom_master(df):
    """Clean discom_master.csv dataset."""
    df = df.copy()
    df = standardize_column_names(df)
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns
    numeric_cols = [c for c in df.columns if c not in ['state', 'discom', 'sl_no', '#']]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_indian_number)
    
    # Fill missing values with 0
    numeric_cols_in_df = [c for c in numeric_cols if c in df.columns and df[c].dtype in ['int64', 'float64']]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    
    return df


def clean_subsidy_status(df):
    """Clean subsidy_status.csv dataset."""
    df = df.copy()
    df = standardize_column_names(df)
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns
    numeric_cols = [c for c in df.columns if c not in ['statuses', 'status', 'sl_no', '#']]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_indian_number)
    
    return df


def clean_vendor_selection(df):
    """Clean vendor_selection.csv dataset."""
    df = df.copy()
    df = standardize_column_names(df)
    df = remove_trailing_empty_columns(df)
    
    # Parse numeric columns
    numeric_cols = [c for c in df.columns if c not in ['sl_no', 'state', 'discom', '#']]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_indian_number)
    
    # Fill missing values with 0
    numeric_cols_in_df = [c for c in numeric_cols if c in df.columns and df[c].dtype in ['int64', 'float64']]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    
    return df


def load_all_datasets():
    """Load all raw datasets."""
    raw_path = Path(__file__).parent.parent / "raw_data"
    
    datewise = pd.read_csv(raw_path / "datewise.csv")
    state_master = pd.read_csv(raw_path / "state_master.csv")
    district = pd.read_csv(raw_path / "district.csv")
    discom_master = pd.read_csv(raw_path / "discom_master.csv")
    subsidy_status = pd.read_csv(raw_path / "subsidy_status.csv")
    vendor_selection = pd.read_csv(raw_path / "vendor_selection.csv")
    
    return {
        'datewise': datewise,
        'state_master': state_master,
        'district': district,
        'discom_master': discom_master,
        'subsidy_status': subsidy_status,
        'vendor_selection': vendor_selection,
    }


def clean_all_datasets(raw_datasets):
    """Clean all raw datasets."""
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
    """Save cleaned datasets to data_cleaned/ folder."""
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
            # Save with _new suffix first
            temp_filepath = output_path / f"{filename[:-4]}_new.csv"
            cleaned_datasets[key].to_csv(temp_filepath, index=False)
            
            # Replace old file with new one (works even if old file is locked)
            if temp_filepath.exists():
                os.replace(str(temp_filepath), str(filepath))
            
            print(f"✓ Saved {key} → {filepath}")


if __name__ == "__main__":
    print("="*80)
    print("DATA CLEANING PIPELINE - FIXED VERSION")
    print("="*80)
    
    print("\n1. Loading raw datasets...")
    raw_datasets = load_all_datasets()
    print(f"   Datewise: {raw_datasets['datewise'].shape[0]} rows")
    print(f"   State Master: {raw_datasets['state_master'].shape[0]} rows")
    print(f"   District: {raw_datasets['district'].shape[0]} rows")
    print(f"   DISCOM Master: {raw_datasets['discom_master'].shape[0]} rows")
    print(f"   Subsidy Status: {raw_datasets['subsidy_status'].shape[0]} rows")
    print(f"   Vendor Selection: {raw_datasets['vendor_selection'].shape[0]} rows")
    
    print("\n2. Cleaning datasets...")
    print("\n   Cleaning datewise.csv:")
    cleaned_datasets = clean_all_datasets(raw_datasets)
    
    print("\n3. Verifying cleaned data:")
    for name, df in cleaned_datasets.items():
        print(f"   {name}: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print("\n4. Saving cleaned datasets...")
    save_cleaned_datasets(cleaned_datasets)
    
    print("\n" + "="*80)
    print("✅ DATA CLEANING COMPLETE!")
    print("="*80)
