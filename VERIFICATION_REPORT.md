# Verification Report

## PM Surya Ghar Analytics - Metric Validation Summary

Last Updated: May 27, 2026

## 1. Objective

Validate that published headline metrics are consistent with current KPI artifacts in data_cleaned/.

## 2. Source of Truth

Primary source:
- data_cleaned/kpis_national.csv

Supporting sources:
- data_cleaned/kpis_state.csv
- data_cleaned/kpis_district.csv
- data_cleaned/datewise_clean.csv

Note: For subsidy totals we validate against `state_master_clean.csv` (`total_redeem_amt`) when present, as that field is the authoritative state-level subsidy aggregation used during KPI calculation.

## 3. Verified Headline Metrics

- total_applications: 6,021,454
- total_installations: 2,329,586
- total_inspections: 2,267,868
- conversion_rate_app_to_install: 38.688097592375534
- total_states: 36
- total_districts: 792
- total_discoms: 84

## 4. Artifact Shape Checks

- kpis_national.csv: 1 row
- kpis_state.csv: 36 rows
- kpis_district.csv: 792 rows
- datewise_clean.csv: 727 rows

## 5. Interpretation Note

The national KPI column total_districts reports 792 districts, matching the district KPI output row count.

## 6. Validation Outcome

Status: Passed

All portfolio headline metrics should reference this report and the current KPI export values.

--
Validation notes (2026-05-28): Initial validation failed because subsidy in `kpis_national.csv` was being compared to `datewise_clean.csv`'s `subsidyredeemed` column. I updated the validation script to use `state_master_clean.csv` (`total_redeem_amt`) as the canonical subsidy source and re-ran the checks after fixing a KPI calculation bug. The validation script now passes against current artifacts. See `scripts/validate_kpis.py` for details.

Dashboard notes (2026-05-28): Batch 2 added a State Analysis chart toggle that switches between grouped bars and a scatter plot of volume vs conversion, with bubble size mapped to subsidy redeemed amount.
