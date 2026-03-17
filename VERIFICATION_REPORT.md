# Verification Report

## PM Surya Ghar Analytics - Metric Validation Summary

Last Updated: March 17, 2026

## 1. Objective

Validate that published headline metrics are consistent with current KPI artifacts in data_cleaned/.

## 2. Source of Truth

Primary source:
- data_cleaned/kpis_national.csv

Supporting sources:
- data_cleaned/kpis_state.csv
- data_cleaned/kpis_district.csv
- data_cleaned/datewise_clean.csv

## 3. Verified Headline Metrics

- total_applications: 6,021,455
- total_installations: 2,329,634
- total_inspections: 2,267,907
- conversion_rate_app_to_install: 38.68888831686029
- total_states: 36
- total_districts: 789
- total_discoms: 84

## 4. Artifact Shape Checks

- kpis_national.csv: 1 row
- kpis_state.csv: 36 rows
- kpis_district.csv: 792 rows
- datewise_clean.csv: 795 rows

## 5. Interpretation Note

The national KPI column total_districts reports unique districts (789), while district KPI output contains 792 rows, indicating repeated district naming across state contexts.

## 6. Validation Outcome

Status: Passed

All portfolio headline metrics should reference this report and the current KPI export values.
