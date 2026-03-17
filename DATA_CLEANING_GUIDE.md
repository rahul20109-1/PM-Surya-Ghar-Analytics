# Data Cleaning Guide

## PM Surya Ghar Analytics - Cleaning Standard Operating Procedure

Last Updated: March 17, 2026

## 1. Purpose

Provide a reproducible, implementation-level guide for converting raw program CSV files into validated analytical artifacts.

## 2. Pipeline Entry Points

- scripts/00_data_loader.py
- scripts/01_data_cleaning.py
- scripts/utils/parser.py

## 3. Standard Cleaning Steps

1. Load source CSV files from raw_data/.
2. Standardize column names (lowercase, underscore format).
3. Remove empty trailing columns caused by source export artifacts.
4. Parse Indian-formatted numerics to numeric types.
5. Convert date columns and enforce expected dtypes.
6. Apply null-handling and duplicate checks.
7. Export cleaned files to data_cleaned/.

## 4. Validation Gates

- Row count continuity check
- Mandatory column presence check
- Numeric conversion sanity checks
- Basic aggregation checks for major measures

## 5. Output Artifacts

- datewise_clean.csv
- state_master_clean.csv
- district_clean.csv
- discom_master_clean.csv
- subsidy_status_clean.csv
- vendor_selection_clean.csv

## 6. Operational Guidance

- Treat raw_data/ as immutable input.
- Run KPI generation after cleaning completion.
- Treat cleaned outputs as source inputs for dashboards and notebooks.
