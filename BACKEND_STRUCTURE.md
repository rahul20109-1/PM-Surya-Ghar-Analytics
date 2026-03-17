# Backend Structure

## PM Surya Ghar Analytics - Data Architecture

Last Updated: March 17, 2026

## 1. Dataset Layers

### Raw Layer
- Location: raw_data/
- Purpose: immutable source extracts
- Usage: ingestion only, no in-place edits

### Cleaned Layer
- Location: data_cleaned/
- Purpose: standardized and validated analytical sources

### KPI Layer
- Location: data_cleaned/
- Purpose: materialized metric outputs for reporting and dashboard usage

## 2. Current Artifact Inventory

### Cleaned Source Artifacts
- datewise_clean.csv: 795 rows
- state_master_clean.csv: 36 rows
- district_clean.csv: 792 rows
- discom_master_clean.csv: 84 rows
- subsidy_status_clean.csv: 29 rows
- vendor_selection_clean.csv: 94 rows

### KPI Artifacts
- kpis_national.csv: 1 row
- kpis_state.csv: 36 rows
- kpis_district.csv: 792 rows

## 3. KPI Headline Snapshot (Current Export)

From data_cleaned/kpis_national.csv:
- total_applications: 6,021,455
- total_installations: 2,329,634
- total_inspections: 2,267,907
- conversion_rate_app_to_install: 38.68888831686029
- total_states: 36
- total_districts: 789
- total_discoms: 84

Note: District KPI file contains 792 rows while total_districts KPI represents unique district count (789).

## 4. Processing Components

- scripts/00_data_loader.py: raw data loading utilities
- scripts/01_data_cleaning.py: cleaning and standardization
- scripts/02_kpi_calculation.py: KPI computation
- scripts/utils/parser.py: numeric parsing helper

## 5. Data Quality Controls

- Schema normalization and column sanitization
- Numeric parsing validation for Indian number formats
- Null and duplicate checks in cleaned outputs
- Aggregation-level sanity checks for KPI integrity

## 6. Consumer Interfaces

- Notebooks: validation and exploratory analysis
- Dashboard: stakeholder-facing interactive reporting
