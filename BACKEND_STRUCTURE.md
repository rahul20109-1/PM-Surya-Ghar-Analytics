# Backend Structure

## PM Surya Ghar Analytics - Data Architecture

Last Updated: May 27, 2026

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
- datewise_clean.csv: 727 rows (primary time-series input)
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
- total_applications: 6,021,454
- total_installations: 2,329,586
- total_inspections: 2,267,868
- conversion_rate_app_to_install: 38.688097592375534
- total_states: 36
- total_districts: 792
- total_discoms: 84

Note: KPI totals are computed from datewise_clean.csv.

## 4. Processing Components

- scripts/00_data_loader.py: raw data loading utilities
- scripts/01_data_cleaning.py: cleaning and standardization (writes datewise_clean.csv)
- scripts/01_data_cleaning_v2.py: fixed cleaning variant (writes datewise_clean.csv)
- scripts/02_kpi_calculation.py: KPI computation
- scripts/utils/parser.py: numeric parsing helper
 - scripts/validate_kpis.py: validation script that compares KPI artifacts to cleaned sources and warns/fails on mismatches

## 5. Data Quality Controls

- Schema normalization and column sanitization
- Numeric parsing validation for Indian number formats
- Null and duplicate checks in cleaned outputs
- Aggregation-level sanity checks for KPI integrity

## 6. Consumer Interfaces

- Notebooks: validation and exploratory analysis
- Dashboard: stakeholder-facing interactive reporting

## 7. Metric Definitions Reference

- Main KPI and normalized metric definitions are documented in `docs/metric_glossary.md`.
- The glossary covers core totals, efficiency metrics, bottleneck formulas, and backlog scenario terms.
