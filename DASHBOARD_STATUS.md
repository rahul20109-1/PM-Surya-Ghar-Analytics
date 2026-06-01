# Dashboard Status Report

Date: June 1, 2026
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
- About

Advanced analysis page:

- Bottleneck Analysis

Additional note:

- A Capacity Metrics route exists in the app code, but it is not currently exposed in the sidebar navigation.

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

- Chart titles, axis labels, legend labels, and table headings were tightened so the dashboard explains the metric in the visual itself.
- Overview KPI cards are cumulative again and no longer show delta badges on the snapshot page.
- State Analysis includes a chart-mode toggle (grouped bars vs volume/conversion scatter) and a focused state multiselect.
- District Analysis includes normalized efficiency columns, pagination controls, and filtered CSV export.
- Trends includes date-range controls, 7-day overlays, and a weekday seasonality curve.
- Bottleneck Analysis now includes backlog scenario planning, direct chart callouts, per-chart date controls, and a focused state comparison selector.
- The dashboard links to the metric glossary so KPI terms are easier to trust and explain.
