# PM Surya Ghar Analytics

Portfolio-grade analytics project for evaluating adoption performance, operational efficiency, and bottlenecks in the PM Surya Ghar rooftop solar subsidy program.

## Executive Snapshot

PM Surya Ghar Analytics is an end-to-end data analytics and dashboard project built to demonstrate professional data workflow capability: ingestion, cleaning, validation, KPI design, exploratory analysis, and interactive reporting.

The project analyzes multi-level program data (datewise, state, district, DISCOM, subsidy, vendor) and surfaces insights through a Streamlit dashboard.

Data disclaimer: This project uses demo data modeled after PM Surya Ghar scheme datasets and does not expose sensitive, personal, or confidential information.

## Portfolio Value

This project demonstrates:

- Production-oriented data cleaning with validation checkpoints
- KPI engineering from raw public program data
- Interactive visualization design for decision support
- Modular Python architecture suitable for extension
- Documentation and governance practices expected in analytics teams

## Business Context

PM Surya Ghar is a large-scale public subsidy initiative. For policy and operations stakeholders, the key question is not only total adoption, but where and why applications stall through the processing pipeline.

This repository focuses on:

- Conversion through core funnel stages
- Geographic performance variation across states and districts
- Processing bottlenecks and pending load concentration
- Program capacity and subsidy-related metrics

## Scope and Data Coverage

- Geographic scope: 36 states and UTs, 789 districts, 84 DISCOMs
- Time coverage: datewise data available in cleaned outputs
- Data source type: CSV files (read-only raw inputs, cleaned analytical outputs)
- Processing model: batch scripts + reusable utilities

## Key Verified Outputs

From current cleaned KPI outputs:

- Total applications: 6,021,455
- Total installations: 2,329,634
- Application to installation conversion: 38.69%
- Total inspections: 2,267,907
- Total states analyzed: 36
- Total districts analyzed: 789

Note: Financial values are retained in the same reporting unit as source datasets and cleaned KPI files.

## Architecture

```text
Raw CSV Data
  -> Data Loading and Standardization
  -> Cleaning and Validation
  -> KPI Calculation
  -> Exploratory Analysis
  -> Streamlit Dashboard
  -> Insights and Recommendations
```

## Dashboard Coverage

Core dashboard includes:

- Overview: National KPIs, trend and funnel summary
- State Analysis: Ranking and metric comparison by state
- District Analysis: District-level drill-down
- Trends: Program trajectory over time
- Capacity Metrics: Capacity and segment indicators
- About: Method and project context

Advanced page:

- Bottleneck Analysis: Drop-off and stage-level delay diagnostics

## Technology Stack

- Python 3.11
- pandas 2.0.3
- numpy 1.24.3
- plotly 5.17.0
- streamlit 1.28.1
- streamlit-aggrid 0.3.4
- matplotlib 3.7.2
- seaborn 0.12.2

Full pinned dependencies are in requirements.txt.

## Repository Structure

```text
PM-Surya-Ghar-Analytics/
  dashboard/                Streamlit application
  scripts/                  Reusable data processing modules
  notebooks/                Analysis and validation notebooks
  data_cleaned/             Cleaned datasets and KPI outputs
  docs and root markdowns   Project governance and implementation docs
  requirements.txt          Locked Python dependencies
```

## How to Run

1. Create or activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start dashboard:

```bash
python -m streamlit run dashboard/streamlit_app.py
```

4. Open local URL shown by Streamlit (typically http://localhost:8501).

## Quality and Validation Approach

- Cleaning pipeline includes numeric parsing and schema normalization
- Validation includes row-level checks, duplicates/null checks, and KPI sanity checks
- KPI outputs are materialized as CSV artifacts for reproducibility
- Dashboard uses cached loading for responsiveness

## Documentation Map

- PRD.md: Product and KPI requirements
- IMPLEMENTATION_PLAN.md: Delivery roadmap by phase
- BACKEND_STRUCTURE.md: Data schema and pipeline definitions
- FRONTEND_GUIDELINES.md: Visualization and UX standards
- TECH_STACK.md: Approved tools and locked versions
- progress.txt: Current execution status

## Recruiter and Reviewer Guidance

If you are evaluating this repository for role fit, start with:

1. README.md for scope and approach
2. scripts/01_data_cleaning.py and scripts/02_kpi_calculation.py for implementation quality
3. dashboard/streamlit_app.py and dashboard/pages/08_bottleneck_analysis.py for productization
4. notebooks/03_KPI_Verification.ipynb for analytical verification workflow

## License and Usage

This repository is intended for portfolio demonstration and learning use. Review source data licensing terms before any production reuse.
