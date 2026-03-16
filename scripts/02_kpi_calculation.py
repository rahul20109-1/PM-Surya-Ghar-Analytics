"""
KPI Calculation Module
Computes all key performance indicators from cleaned datasets.

Metrics calculated:
- Adoption metrics (conversion rates, funnel efficiency)
- Geographic metrics (state/district rankings)
- Financial metrics (subsidy per install, utilization)
- Operational metrics (approval rates, processing time)
- Capacity metrics (total installed, residential vs RWA)

Output: kpis_master.csv with all calculated metrics
"""

import pandas as pd
import numpy as np
from pathlib import Path
import importlib.util
from datetime import datetime


def load_cleaned_datasets():
    """
    Load all cleaned datasets from data_cleaned/ folder.

    Returns:
        dict: {name -> DataFrame} for all 6 cleaned datasets
    """
    data_cleaned_path = Path(__file__).parent.parent / "data_cleaned"

    datasets = {}
    for csv_file in sorted(data_cleaned_path.glob("*_clean.csv")):
        name = csv_file.stem.replace("_clean", "")
        df = pd.read_csv(csv_file)
        datasets[name] = df
        print(f"  ✓ Loaded {name}: {df.shape[0]} rows × {df.shape[1]} columns")

    return datasets


def calculate_adoption_metrics(datewise_df, state_df):
    """
    Calculate adoption funnel metrics: conversion rates and efficiency.

    Args:
        datewise_df: Daily metrics
        state_df: State-level aggregated data

    Returns:
        dict: KPI dictionary with adoption metrics
    """
    metrics = {}

    # Aggregate from datewise to get cumulative totals
    total_applications = datewise_df["applications"].sum()
    total_installations = datewise_df["installations"].sum()
    total_inspections = datewise_df["inspection"].sum()
    total_subsidy_redeemed = datewise_df["subsidyredeemed"].sum()

    metrics["total_applications"] = int(total_applications)
    metrics["total_installations"] = int(total_installations)
    metrics["total_inspections"] = int(total_inspections)
    metrics["total_subsidy_redeemed"] = int(total_subsidy_redeemed)

    # Conversion rates
    if total_applications > 0:
        metrics["conversion_rate_app_to_install"] = (
            total_installations / total_applications
        ) * 100
        metrics["conversion_rate_app_to_subsidy"] = (
            total_subsidy_redeemed / total_applications
        ) * 100
    else:
        metrics["conversion_rate_app_to_install"] = 0
        metrics["conversion_rate_app_to_subsidy"] = 0

    if total_installations > 0:
        metrics["conversion_rate_install_to_inspection"] = (
            total_inspections / total_installations
        ) * 100
    else:
        metrics["conversion_rate_install_to_inspection"] = 0

    return metrics


def calculate_geographic_metrics(state_df, district_df, discom_df):
    """
    Calculate state and district rankings.

    Args:
        state_df: State level metrics
        district_df: District level metrics
        discom_df: DISCOM level metrics

    Returns:
        dict: Geographic KPIs and rankings
    """
    metrics = {}

    # State rankings
    state_summary = {}
    for _, row in state_df.iterrows():
        state = row["state"]
        if pd.isna(state) or state == "":
            continue

        state_summary[state] = {
            "applications": row.get("application_status", 0) or 0,
            "installations": row.get("installation", 0) or 0,
            "subsidy_redeemed": row.get("total_redeem_amt", 0) or 0,
            "capacity_installed": row.get("installed_capacity", 0) or 0,
        }

    # Top states
    if state_summary:
        top_state_by_apps = max(
            state_summary.items(), key=lambda x: x[1]["applications"]
        )
        metrics["top_state_by_applications"] = top_state_by_apps[0]
        metrics["top_state_applications_count"] = int(
            top_state_by_apps[1]["applications"]
        )

        top_state_by_installs = max(
            state_summary.items(), key=lambda x: x[1]["installations"]
        )
        metrics["top_state_by_installations"] = top_state_by_installs[0]
        metrics["top_state_installations_count"] = int(
            top_state_by_installs[1]["installations"]
        )

        # State count
        metrics["total_states"] = len(state_summary)

    # District analysis
    districts_count = len(district_df.dropna(subset=["district"]))
    metrics["total_districts"] = districts_count

    # DISCOM analysis
    discoms_count = len(discom_df.dropna(subset=["discom"]))
    metrics["total_discoms"] = discoms_count

    return metrics


def calculate_financial_metrics(state_df, datewise_df):
    """
    Calculate financial metrics: subsidy, cost efficiency.

    Args:
        state_df: State level financial data
        datewise_df: Daily metrics

    Returns:
        dict: Financial KPIs
    """
    metrics = {}

    # Total subsidy released and redeemed
    total_released = state_df["total_released_amt"].sum()
    total_redeemed = state_df["total_redeem_amt"].sum()
    total_installations = datewise_df["installations"].sum()

    metrics["total_subsidy_released"] = (
        float(total_released) if total_released > 0 else 0
    )
    metrics["total_subsidy_redeemed"] = (
        float(total_redeemed) if total_redeemed > 0 else 0
    )

    # Subsidy per installation
    if total_installations > 0:
        metrics["subsidy_per_installation"] = total_redeemed / total_installations
    else:
        metrics["subsidy_per_installation"] = 0

    # Subsidy utilization rate
    if total_released > 0:
        metrics["subsidy_utilization_rate"] = (total_redeemed / total_released) * 100
    else:
        metrics["subsidy_utilization_rate"] = 0

    return metrics


def calculate_operational_metrics(state_df, datewise_df):
    """
    Calculate operational metrics: approval rates, pending counts.

    Args:
        state_df: State level operational data
        datewise_df: Daily metrics

    Returns:
        dict: Operational KPIs
    """
    metrics = {}

    # Vendor selection approval rate
    vendor_selected_total = state_df["vendor_selected"].sum()
    applications_total = state_df["application_status"].sum()

    if applications_total > 0:
        metrics["vendor_selection_approval_rate"] = (
            vendor_selected_total / applications_total
        ) * 100
    else:
        metrics["vendor_selection_approval_rate"] = 0

    # Feasibility approval rate
    feasibility_approved_total = state_df["feasibility_approved"].sum()
    if applications_total > 0:
        metrics["feasibility_approval_rate"] = (
            feasibility_approved_total / applications_total
        ) * 100
    else:
        metrics["feasibility_approval_rate"] = 0

    # Inspection approval rate
    inspection_approved_total = state_df["inspection_approved"].sum()
    installations_total = state_df["installation"].sum()

    if installations_total > 0:
        metrics["inspection_approval_rate"] = (
            inspection_approved_total / installations_total
        ) * 100
    else:
        metrics["inspection_approval_rate"] = 0

    # Pending counts
    metrics["pending_vendor_selection"] = int(
        state_df["vendor_selected"].sum() - vendor_selected_total
    )
    metrics["pending_feasibility"] = int(state_df["feasibility_pending"].sum())
    metrics["pending_inspection"] = int(state_df["inspection_pending"].sum())

    return metrics


def calculate_capacity_metrics(state_df, datewise_df):
    """
    Calculate capacity metrics: total installed, residential vs RWA, average size.

    Args:
        state_df: State level capacity data
        datewise_df: Daily metrics

    Returns:
        dict: Capacity KPIs
    """
    metrics = {}

    # Total capacity
    total_capacity = state_df["installed_capacity"].sum()
    metrics["total_capacity_installed_kw"] = (
        float(total_capacity) if total_capacity > 0 else 0
    )

    # Residential vs RWA
    residential_installs = (
        datewise_df["residential"].sum() if "residential" in datewise_df.columns else 0
    )
    rwa_installs = datewise_df["rwa"].sum() if "rwa" in datewise_df.columns else 0
    total_installs = datewise_df["installations"].sum()

    if total_installs > 0:
        metrics["residential_percentage"] = (
            residential_installs / total_installs
        ) * 100
        metrics["rwa_percentage"] = (rwa_installs / total_installs) * 100
    else:
        metrics["residential_percentage"] = 0
        metrics["rwa_percentage"] = 0

    # Capacity segment breakdown
    upto_10kw = state_df["upto_10_kw"].sum()
    above_10kw = state_df["above_10_kw"].sum()

    metrics["installations_upto_10kw"] = int(upto_10kw)
    metrics["installations_above_10kw"] = int(above_10kw)

    # Average system size
    if total_installs > 0:
        metrics["average_system_size_kw"] = total_capacity / total_installs
    else:
        metrics["average_system_size_kw"] = 0

    return metrics


def calculate_state_level_kpis(state_df, district_df):
    """
    Calculate KPIs for each state.

    Args:
        state_df: State level metrics
        district_df: District level metrics

    Returns:
        DataFrame: State-level KPIs
    """
    state_kpis = []

    for _, row in state_df.iterrows():
        state = row["state"]
        if pd.isna(state) or state == "":
            continue

        apps = row.get("application_status", 0) or 0
        installs = row.get("installation", 0) or 0
        inspections = row.get("inspection_approved", 0) or 0
        subsidy = row.get("total_redeem_amt", 0) or 0
        capacity = row.get("installed_capacity", 0) or 0
        vendors = row.get("vendor_selected", 0) or 0

        # Calculate conversion rates for state
        conv_app_to_install = (installs / apps * 100) if apps > 0 else 0
        conv_install_to_inspect = (inspections / installs * 100) if installs > 0 else 0
        subsidy_per_install = subsidy / installs if installs > 0 else 0
        avg_capacity = capacity / installs if installs > 0 else 0

        state_kpis.append(
            {
                "state": state,
                "applications": int(apps),
                "installations": int(installs),
                "approvals": int(inspections),
                "subsidy_redeemed_amount": float(subsidy),
                "capacity_installed_kw": float(capacity),
                "vendors_selected": int(vendors),
                "conversion_rate_app_to_install_pct": round(conv_app_to_install, 2),
                "conversion_rate_install_to_approval_pct": round(
                    conv_install_to_inspect, 2
                ),
                "subsidy_per_installation": round(subsidy_per_install, 2),
                "avg_system_size_kw": round(avg_capacity, 2),
            }
        )

    return pd.DataFrame(state_kpis).sort_values("applications", ascending=False)


def calculate_district_level_kpis(district_df):
    """
    Calculate KPIs for each district.

    Args:
        district_df: District level metrics

    Returns:
        DataFrame: District-level KPIs
    """
    district_kpis = []

    for _, row in district_df.iterrows():
        state = row.get("state", "")
        district = row.get("district", "")

        if pd.isna(district) or district == "":
            continue

        apps = row.get("application_status", 0) or 0
        installs = row.get("installation", 0) or 0
        capacity = (
            row.get("installed_capacity", 0) or 0 if "installed_capacity" in row else 0
        )

        conv_rate = (installs / apps * 100) if apps > 0 else 0
        avg_capacity = capacity / installs if installs > 0 else 0

        district_kpis.append(
            {
                "state": state,
                "district": district,
                "applications": int(apps),
                "installations": int(installs),
                "conversion_rate_pct": round(conv_rate, 2),
                "capacity_installed_kw": float(capacity),
                "avg_system_size_kw": round(avg_capacity, 2),
            }
        )

    return pd.DataFrame(district_kpis).sort_values("applications", ascending=False)


def validate_kpis(kpi_dict):
    """
    Validate KPI values for reasonableness.

    Args:
        kpi_dict: Dictionary of calculated KPIs

    Prints:
        Validation results and warnings
    """
    warnings = []

    # Check conversion rates are 0-100%
    conversion_kpis = [
        k for k in kpi_dict.keys() if "conversion_rate" in k or "approval_rate" in k
    ]
    for kpi in conversion_kpis:
        value = kpi_dict.get(kpi, 0)
        if not (0 <= value <= 100):
            warnings.append(f"⚠️  {kpi}: {value:.2f}% (expected 0-100%)")

    # Check positive counts
    count_kpis = [k for k in kpi_dict.keys() if "total_" in k or "_count" in k]
    for kpi in count_kpis:
        value = kpi_dict.get(kpi, 0)
        if value < 0:
            warnings.append(f"⚠️  {kpi}: {value} (expected ≥0)")

    if warnings:
        print("\n⚠️  Validation Warnings:")
        for warning in warnings:
            print(f"   {warning}")
    else:
        print("\n✓ All KPIs validated successfully")


def save_kpis(kpi_dict, state_kpis_df, district_kpis_df):
    """
    Save KPIs to CSV files.

    Args:
        kpi_dict: National-level KPI dictionary
        state_kpis_df: State-level KPI dataframe
        district_kpis_df: District-level KPI dataframe
    """
    output_path = Path(__file__).parent.parent / "data_cleaned"
    output_path.mkdir(exist_ok=True)

    # Save national KPIs
    kpi_df = pd.DataFrame([kpi_dict])
    kpi_path = output_path / "kpis_national.csv"
    kpi_df.to_csv(kpi_path, index=False)
    print(f"✓ Saved national KPIs → {kpi_path}")

    # Save state KPIs
    state_path = output_path / "kpis_state.csv"
    state_kpis_df.to_csv(state_path, index=False)
    print(f"✓ Saved state KPIs → {state_path} ({len(state_kpis_df)} states)")

    # Save district KPIs
    district_path = output_path / "kpis_district.csv"
    district_kpis_df.to_csv(district_path, index=False)
    print(
        f"✓ Saved district KPIs → {district_path} ({len(district_kpis_df)} districts)"
    )


def calculate_all_kpis():
    """
    Master function: Load data, calculate all KPIs, validate, and save.

    Returns:
        tuple: (kpi_dict, state_kpis_df, district_kpis_df)
    """
    print("=" * 80)
    print("KPI CALCULATION MODULE")
    print("=" * 80)

    print("\n1. Loading cleaned datasets...")
    datasets = load_cleaned_datasets()

    datewise = datasets["datewise"]
    state = datasets["state_master"]
    district = datasets["district"]
    discom = datasets["discom_master"]

    print("\n2. Calculating national-level KPIs...")

    adoption_kpis = calculate_adoption_metrics(datewise, state)
    print(f"   ✓ Adoption metrics: {len(adoption_kpis)} metrics")

    geographic_kpis = calculate_geographic_metrics(state, district, discom)
    print(f"   ✓ Geographic metrics: {len(geographic_kpis)} metrics")

    financial_kpis = calculate_financial_metrics(state, datewise)
    print(f"   ✓ Financial metrics: {len(financial_kpis)} metrics")

    operational_kpis = calculate_operational_metrics(state, datewise)
    print(f"   ✓ Operational metrics: {len(operational_kpis)} metrics")

    capacity_kpis = calculate_capacity_metrics(state, datewise)
    print(f"   ✓ Capacity metrics: {len(capacity_kpis)} metrics")

    # Combine all national KPIs
    kpi_dict = {}
    kpi_dict.update(adoption_kpis)
    kpi_dict.update(geographic_kpis)
    kpi_dict.update(financial_kpis)
    kpi_dict.update(operational_kpis)
    kpi_dict.update(capacity_kpis)

    print(f"\n   Total national KPIs: {len(kpi_dict)}")

    print("\n3. Calculating state-level KPIs...")
    state_kpis_df = calculate_state_level_kpis(state, district)
    print(f"   ✓ {len(state_kpis_df)} states analyzed")

    print("\n4. Calculating district-level KPIs...")
    district_kpis_df = calculate_district_level_kpis(district)
    print(f"   ✓ {len(district_kpis_df)} districts analyzed")

    print("\n5. Validating KPIs...")
    validate_kpis(kpi_dict)

    print("\n6. Saving KPI outputs...")
    save_kpis(kpi_dict, state_kpis_df, district_kpis_df)

    print("\n" + "=" * 80)
    print("✅ KPI CALCULATION COMPLETE")
    print("=" * 80)

    return kpi_dict, state_kpis_df, district_kpis_df


if __name__ == "__main__":
    calculate_all_kpis()
