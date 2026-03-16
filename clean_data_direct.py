import pandas as pd
from pathlib import Path

# This script cleans the data and saves to a temporary location

# Define paths
raw_path = Path("raw_data")
temp_path = Path("data_cleaned_temp")
temp_path.mkdir(exist_ok=True)

print("CLEANING ALL DATASETS - WITH PROPER PARSER")
print("=" * 80)

# Load all raw files
print("\n1. Loading raw datasets...")
datewise = pd.read_csv(raw_path / "datewise.csv")
state_master = pd.read_csv(raw_path / "state_master.csv")
district = pd.read_csv(raw_path / "district.csv")
discom_master = pd.read_csv(raw_path / "discom_master.csv")
subsidy_status = pd.read_csv(raw_path / "subsidy_status.csv")
vendor_selection = pd.read_csv(raw_path / "vendor_selection.csv")


def parse_indian_number(value):
    """Parse Indian formatted numbers."""
    if pd.isna(value):
        return float("nan")
    value_str = str(value).strip()
    try:
        return float(value_str)
    except ValueError:
        value_str = value_str.replace(",", "")
        try:
            return float(value_str)
        except ValueError:
            return float("nan")


def clean_datewise_file(df):
    df = df.copy()
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("(", "")
        .str.replace(")", "")
        .str.replace(".", "")
    )
    df = df.dropna(axis=1, how="all")
    if "rptdate" in df.columns:
        df["rptdate"] = pd.to_datetime(df["rptdate"], format="%d-%m-%Y")
    numeric_cols = [c for c in df.columns if c not in ["#", "rptdate"]]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_indian_number)
    count_cols = [c for c in df.columns if df[c].dtype in ["int64", "float64"]]
    df[count_cols] = df[count_cols].fillna(0)
    df = df.sort_values("rptdate", ascending=False).reset_index(drop=True)
    return df


def clean_other_file(df, exclude_cols):
    df = df.copy()
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("(", "")
        .str.replace(")", "")
        .str.replace(".", "")
    )
    df = df.dropna(axis=1, how="all")
    numeric_cols = [c for c in df.columns if c not in exclude_cols]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_indian_number)
    numeric_cols_in_df = [
        c
        for c in numeric_cols
        if c in df.columns and df[c].dtype in ["int64", "float64"]
    ]
    df[numeric_cols_in_df] = df[numeric_cols_in_df].fillna(0)
    return df


# Clean each file
print("\n2. Cleaning files...")
print("   datewise...")
datewise_clean = clean_datewise_file(datewise)
print(f"      Applications: {datewise_clean['applications'].sum():,.0f}")
print(f"      Installations: {datewise_clean['installations'].sum():,.0f}")
print(f"      Inspections: {datewise_clean['inspection'].sum():,.0f}")

print("   state_master...")
state_master_clean = clean_other_file(state_master, ["state", "sl_no", "#"])

print("   district...")
district_clean = clean_other_file(district, ["state", "district", "sl_no", "#"])

print("   discom_master...")
discom_master_clean = clean_other_file(discom_master, ["state", "discom", "sl_no", "#"])

print("   subsidy_status...")
subsidy_status_clean = clean_other_file(
    subsidy_status, ["statuses", "status", "sl_no", "#"]
)

print("   vendor_selection...")
vendor_selection_clean = clean_other_file(
    vendor_selection, ["sl_no", "state", "discom", "#"]
)

# Save to temp location
print("\n3. Saving to temporary folder (data_cleaned_temp/)...")
datewise_clean.to_csv(temp_path / "datewise_clean.csv", index=False)
state_master_clean.to_csv(temp_path / "state_master_clean.csv", index=False)
district_clean.to_csv(temp_path / "district_clean.csv", index=False)
discom_master_clean.to_csv(temp_path / "discom_master_clean.csv", index=False)
subsidy_status_clean.to_csv(temp_path / "subsidy_status_clean.csv", index=False)
vendor_selection_clean.to_csv(temp_path / "vendor_selection_clean.csv", index=False)
print("   ✓ All files saved to data_cleaned_temp/")

print("\n4. VERIFICATION OF CLEANED DATA:")
print(f"   Datewise: {datewise_clean.shape[0]} rows x {datewise_clean.shape[1]} cols")
print(f"     > Applications: {datewise_clean['applications'].sum():,.0f}")
print(f"     > Installations: {datewise_clean['installations'].sum():,.0f}")
print(f"     > Inspections: {datewise_clean['inspection'].sum():,.0f}")
print(f"     > Subsidy Redeemed: {datewise_clean['subsidyredeemed'].sum():,.0f}")
print(
    f"   State Master: {state_master_clean.shape[0]} rows x {state_master_clean.shape[1]} cols"
)
print(f"   District: {district_clean.shape[0]} rows x {district_clean.shape[1]} cols")
print(
    f"   DISCOM Master: {discom_master_clean.shape[0]} rows x {discom_master_clean.shape[1]} cols"
)
print(
    f"   Subsidy Status: {subsidy_status_clean.shape[0]} rows x {subsidy_status_clean.shape[1]} cols"
)
print(
    f"   Vendor Selection: {vendor_selection_clean.shape[0]} rows x {vendor_selection_clean.shape[1]} cols"
)

print("\n" + "=" * 80)
print("✅ CLEANING COMPLETE")
print("Files saved in: data_cleaned_temp/")
print("=" * 80)
