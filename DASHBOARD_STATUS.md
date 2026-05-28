# Dashboard Status Report

Date: May 27, 2026
Status: Operational

## Operational State

- Dashboard launch command is available and functional
- Data is loaded from cleaned CSV outputs in data_cleaned/
- Core KPI and chart components render through dashboard utilities
- Caching is enabled for data loading performance
- Time-series views include date-range filters and 7-day average overlays

## Coverage

Core views are implemented in the main app:

- Overview
- State Analysis
- District Analysis
- Trends
- Capacity Metrics
- About

Advanced analysis page:

- Bottleneck Analysis

## Runbook

1. Activate the project virtual environment.
2. Install dependencies if needed:

```bash
pip install -r requirements.txt
```

3. Run dashboard:

```bash
python -m streamlit run dashboard/streamlit_app.py
```

4. Open the local URL shown in terminal.

## Validation Step

After regenerating cleaned artifacts and KPIs, run the validation script to confirm artifact consistency before launching the dashboard:

```bash
python scripts/validate_kpis.py
```

If validation fails, address the mismatches (check `state_master_clean.csv` and `datewise_clean.csv`) before demoing the dashboard.

## Data Dependencies

Primary files required by dashboard loaders:

- data_cleaned/datewise_clean.csv
- data_cleaned/state_master_clean.csv
- data_cleaned/district_clean.csv
- data_cleaned/kpis_national.csv
- data_cleaned/kpis_state.csv
- data_cleaned/kpis_district.csv

## Notes for Portfolio Use

- Keep screenshots or short demo recording for interview walkthroughs
- Pair dashboard demo with KPI verification notebook to show analytical rigor
- Use this file as operational reference, not as implementation history log

## Latest Dashboard Enhancements

- Overview KPI cards now show deltas against the previous period of the same length.
- State and district comparison tables now include normalized efficiency columns.
- Bottleneck Analysis now includes backlog scenario planning and direct chart callouts.
- The dashboard links to the metric glossary so KPI terms are easier to trust and explain.
