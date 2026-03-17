# Application Flow

## PM Surya Ghar Analytics - End-to-End Workflow

Last Updated: March 17, 2026

## 1. System Flow

```text
Raw Program Data (CSV)
  -> Ingestion and Schema Normalization
  -> Numeric Parsing and Data Cleaning
  -> Data Quality Validation
  -> KPI Calculation (National, State, District)
  -> Exploratory Analysis and Bottleneck Review
  -> Dashboard Rendering (Streamlit)
  -> Insight Communication for Stakeholders
```

## 2. Data Pipeline Stages

### Stage A: Ingestion
- Input files are loaded from raw_data/ using scripted loaders.
- Structural checks are applied for required columns and expected schema patterns.

### Stage B: Cleaning
- Column names are standardized.
- Indian-formatted numeric strings are parsed into numeric types.
- Empty and invalid records are handled using documented rules.

### Stage C: Validation
- Row-level sanity checks are performed.
- Duplicates, null profiles, and metric consistency are reviewed.
- Aggregation checks are used to prevent silent metric drift.

### Stage D: KPI Engineering
- National KPI artifact: data_cleaned/kpis_national.csv
- State KPI artifact: data_cleaned/kpis_state.csv
- District KPI artifact: data_cleaned/kpis_district.csv

### Stage E: Analysis and Reporting
- Notebooks provide verification and exploratory context.
- Dashboard pages convert KPI and cleaned data into interactive views.

## 3. Dashboard User Flow

1. Open overview for national KPI orientation.
2. Drill into state and district breakdowns.
3. Inspect trend behavior over time.
4. Use bottleneck analysis to evaluate stage-level drop-off.
5. Translate findings into operational recommendations.

## 4. Governance Principles

- Use cleaned artifact outputs as reporting source of truth.
- Keep business-facing claims traceable to KPI exports.
- Preserve modular separation between scripts, notebooks, and dashboard code.
