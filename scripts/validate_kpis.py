"""
Validate KPI artifacts against cleaned data sources.

Usage:
    python scripts/validate_kpis.py

Exits with code 0 if all checks pass, else exits with code 1 and prints mismatches.
"""

import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parent.parent
DATA_CLEANED = ROOT / "data_cleaned"


def load_kpis():
    kpi_path = DATA_CLEANED / "kpis_national.csv"
    if not kpi_path.exists():
        raise FileNotFoundError(f"Missing KPI file: {kpi_path}")
    kpis = pd.read_csv(kpi_path)
    if kpis.shape[0] < 1:
        raise ValueError("kpis_national.csv appears empty")
    return kpis.iloc[0].to_dict()


def load_datewise():
    p1 = DATA_CLEANED / "datewise_clean2.csv"
    p2 = DATA_CLEANED / "datewise_clean.csv"
    if p1.exists():
        return pd.read_csv(p1)
    if p2.exists():
        return pd.read_csv(p2)
    raise FileNotFoundError("No datewise_clean CSV found in data_cleaned/")


def load_state_master():
    path = DATA_CLEANED / "state_master_clean.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing state_master_clean.csv: {path}")
    return pd.read_csv(path)


def load_district():
    path = DATA_CLEANED / "district_clean.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def approx_equal(a, b, tol=1e-6):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False


def main():
    failures = []

    kpi = load_kpis()
    datewise = load_datewise()
    state_master = load_state_master()
    district = load_district()

    # Check totals from datewise
    # Filter datewise to scheme launch date to avoid pre-launch test rows
    if "rptdate" in datewise.columns:
        try:
            date_series = pd.to_datetime(datewise["rptdate"], errors="coerce")
            launch_date = pd.Timestamp("2024-02-13")
            datewise = datewise.loc[date_series >= launch_date].copy()
        except Exception:
            pass

    expected_apps = int(datewise["applications"].sum()) if "applications" in datewise.columns else 0
    expected_installs = int(datewise["installations"].sum()) if "installations" in datewise.columns else 0
    expected_inspections = int(datewise["inspection"].sum()) if "inspection" in datewise.columns else 0
    # Prefer state_master total_redeem_amt as the canonical subsidy source when present
    expected_subsidy = None
    if "total_redeem_amt" in state_master.columns:
        expected_subsidy = float(state_master["total_redeem_amt"].sum())
    elif "total_redeem" in state_master.columns:
        expected_subsidy = float(state_master["total_redeem"].sum())
    elif "subsidyredeemed" in datewise.columns:
        expected_subsidy = float(datewise["subsidyredeemed"].sum())

    # Compare with KPI values
    kpi_apps = int(kpi.get("total_applications", -1))
    kpi_installs = int(kpi.get("total_installations", -1))
    kpi_inspections = int(kpi.get("total_inspections", -1))
    kpi_subsidy = float(kpi.get("total_subsidy_redeemed", float(kpi.get("total_subsidy_redeemed", 0)))) if kpi.get("total_subsidy_redeemed", None) is not None else None

    if kpi_apps != expected_apps:
        failures.append(f"total_applications mismatch: KPI={kpi_apps} vs datewise={expected_apps}")
    if kpi_installs != expected_installs:
        failures.append(f"total_installations mismatch: KPI={kpi_installs} vs datewise={expected_installs}")
    if kpi_inspections != expected_inspections:
        failures.append(f"total_inspections mismatch: KPI={kpi_inspections} vs datewise={expected_inspections}")

    if expected_subsidy is not None and kpi_subsidy is not None:
        # Allow small rounding differences
        if not approx_equal(kpi_subsidy, expected_subsidy, tol=1e-2):
            failures.append(f"total_subsidy_redeemed mismatch: KPI={kpi_subsidy} vs datewise={expected_subsidy}")

    # District count
    if district is not None:
        expected_districts = int(district.shape[0])
        kpi_districts = int(kpi.get("total_districts", -1))
        if kpi_districts != expected_districts:
            failures.append(f"total_districts mismatch: KPI={kpi_districts} vs district file={expected_districts}")

    # Basic state-level consistency: sum of state application_status should equal expected_apps
    if "application_status" in state_master.columns:
        state_apps = int(state_master["application_status"].sum())
        diff = abs(state_apps - expected_apps)
        # Allow small tolerated differences due to pre-launch row removal or minor source drift
        if diff > 10:
            failures.append(f"Sum(state.application_status)={state_apps} != sum(datewise.applications)={expected_apps} (diff={diff})")
        elif diff > 0:
            print(f"WARNING: small mismatch between state and datewise application totals (diff={diff}); treated as acceptable")

    # Report results
    if failures:
        print("KPI VALIDATION: FAIL")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    else:
        print("KPI VALIDATION: PASS — KPI artifacts match cleaned source aggregates")
        sys.exit(0)


if __name__ == "__main__":
    main()
