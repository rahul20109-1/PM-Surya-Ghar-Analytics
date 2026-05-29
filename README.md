# PM Surya Ghar Analytics

This project turns public program data from the PM Surya Ghar rooftop solar scheme into clear, easy-to-read insights. It shows how raw CSV files can be cleaned, checked, summarized, and presented in a dashboard.

## What This Project Shows

The goal is to show careful data work, not just charts. The project focuses on:

- cleaning messy source data and making it usable
- checking the numbers after each step
- tracking how applications move through the scheme
- finding where the process slows down
- presenting the results in a simple way

## Why It Matters

PM Surya Ghar is a large public subsidy program. For a recruiter or reviewer, the useful question is not only how many applications came in, but where the process moves well and where it gets stuck.

This repository looks at:

- total application and installation counts
- state and district level differences
- stage-wise drop-offs in the process
- subsidy and capacity related patterns

## What Is Included

- 36 states and UTs
- 792 districts in the cleaned KPI output
- 84 DISCOMs
- datewise data for trend analysis
- cleaned CSV outputs for repeatable reporting
- a Streamlit dashboard for quick exploration

## Main Results

From the current cleaned KPI files:

- Total applications: 6,021,454
- Total installations: 2,329,586
- Application to installation conversion: 38.69%
- Total inspections: 2,267,868
- Total states analyzed: 36
- Total districts analyzed: 792

These numbers come from the cleaned KPI outputs in [data_cleaned/](data_cleaned/).

## Metric Glossary

The main KPI definitions, normalized metrics, and bottleneck formulas are documented in [docs/metric_glossary.md](docs/metric_glossary.md).

## Resume Highlights

- Built a reproducible analytics pipeline for 6M+ public-sector records across 36 states and 792 districts.
- Cleaned, validated, and engineered KPI outputs before dashboarding the results in Streamlit.
- Added bottleneck diagnostics, date-range filtering, district export, and state-level comparison views for faster analysis.
- Added normalized efficiency metrics, backlog scenarios, and a metric glossary to make the analysis easier to trust and explain.
- Documented the validation process so the numbers can be checked and reused confidently.

## How It Works

```text
Raw CSV files
  -> Data loading
  -> Cleaning and validation
  -> KPI calculation
  -> Notebook-based analysis
  -> Streamlit dashboard
  -> Clear findings and recommendations
```

## Dashboard Pages

The dashboard includes:

- Overview: main KPIs and funnel summary
- State Analysis: compare states by volume and conversion
- District Analysis: drill into district level data
- Trends: review movement over time
- About: short project summary
- Bottleneck Analysis: see where the process slows down

Note: A Capacity Metrics section exists in code, but it is not currently exposed in the main sidebar navigation.

## Technology Stack

- Python 3.11.9
- streamlit >=1.28, <2.0
- pandas >=2.3
- numpy >=2.0
- plotly >=5.17
- matplotlib and seaborn (notebook analysis)

Runtime dependencies for Streamlit Cloud are listed in [requirements.txt](requirements.txt). Notebook-only packages are installed locally as needed.

## Project Structure

```text
PM-Surya-Ghar-Analytics/
  dashboard/        Streamlit app and dashboard helpers
  scripts/          Data loading, cleaning, and KPI scripts
  notebooks/        Analysis and validation notebooks
  data_cleaned/     Cleaned datasets and KPI outputs
  requirements.txt  Python dependencies
```

## How To Run

1. Create or activate a Python environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Start the dashboard:

```bash
python -m streamlit run dashboard/streamlit_app.py
```

4. Open the local link shown by Streamlit, usually http://localhost:8501.

## How The Data Is Checked

- numbers are parsed and standardized before analysis
- cleaned files are checked for missing values and duplicates
- KPI totals are compared against the source data
- dashboard pages use cached loading so the app stays responsive
- KPI and bottleneck terms are defined in [docs/metric_glossary.md](docs/metric_glossary.md)

## Where To Start

If you are reviewing this repository for hiring or project fit, start with:

1. [scripts/01_data_cleaning.py](scripts/01_data_cleaning.py) and [scripts/02_kpi_calculation.py](scripts/02_kpi_calculation.py) to see how the data is handled
2. [dashboard/streamlit_app.py](dashboard/streamlit_app.py) and [dashboard/pages/08_bottleneck_analysis.py](dashboard/pages/08_bottleneck_analysis.py) to see how the results are presented
3. [notebooks/03_KPI_Verification.ipynb](notebooks/03_KPI_Verification.ipynb) to see how the numbers were checked

## Validation

After running the cleaning and KPI pipeline, run the validation script to ensure KPI artifacts match the cleaned sources:

```bash
python scripts/validate_kpis.py
```

The script compares `data_cleaned/kpis_national.csv` against aggregates from `state_master_clean.csv` (preferred for subsidy totals) and `datewise_clean.csv`. It fails loudly on large mismatches and warns on small, acceptable differences.

## License And Use

This repository is intended for portfolio and learning use. If you reuse the source data in another project, review the source terms first.
