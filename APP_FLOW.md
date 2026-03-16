# Application Flow (APP_FLOW.md)

# PM Surya Ghar Analytics — Data Journey & Analysis Narrative

**Purpose:** Define how data flows through the analysis system and the narrative path a user/analyst follows.

---

## 1. High-Level Data Pipeline

```
Raw Data (6 CSVs)
    ↓
[Data Ingestion]
    ↓
Data Cleaning & Standardization
    ↓
[Validated Clean Data]
    ↓
Data Understanding & Exploration
    ↓
[Schema & Pattern Discovery]
    ↓
KPI Calculation & Metrics Generation
    ↓
[Derived Metrics & Aggregations]
    ↓
Exploratory Data Analysis (EDA)
    ↓
[Deeper Patterns, Comparisons, Trends]
    ↓
Visualization Creation
    ↓
[Charts, Heatmaps, Funnels, Time-Series]
    ↓
Interactive Dashboard Integration
    ↓
[Streamlit App with Filters]
    ↓
Insight Extraction & Reporting
    ↓
[Executive Summary + Detailed Findings]
    ↓
Documentation & Portfolio Publishing
```

---

## 2. Detailed Data Ingestion Flow

### 2.1 Source Data Loading

**Input:** Raw CSV files from `raw_data/` folder  
**Process:**

1. Load 6 datasets using `pandas.read_csv()`
2. Inspect schema: columns, dtypes, rows
3. Document date ranges and data completeness
4. Flag missing values and anomalies

**Output:** 6 raw dataframes in memory (not modified)

**Files Involved:**

- `scripts/00_data_loader.py` — Load and cache data
- `notebooks/01_Data_Understanding.ipynb` — Exploratory inspection

**Example Output:**

```
datewise.csv: 300 rows, 10 columns, dates: 2026-02-01 to 2026-02-09
state_master.csv: 36 rows (states), 35 columns, latest snapshot
district.csv: ~700 rows (state-districts), 29 columns
...
```

---

## 3. Data Cleaning Flow

### 3.1 Standardization & Parsing

**Input:** Raw dataframes  
**Process:**

1. **Numeric Format Parsing:** Convert Indian format ("5,47,284") → integer (547284)
2. **Column Naming:** Standardize to lowercase, remove hyphens, underscore spaces
3. **Data Types:** Convert to numeric, datetime, category as needed
4. **Missing Values:** Document strategy (fill, drop, flag)
5. **Duplicates:** Remove if identified
6. **Outlier Flagging:** Identify unusual values for validation

**Output:** Cleaned dataframes saved to `data_cleaned/`

**Files Involved:**

- `scripts/01_data_cleaning.py` — Main cleaning logic
- `scripts/utils/parser.py` — Indian number parsing
- `notebooks/02_Data_Cleaning.ipynb` — Cleaning narrative

**Example Transformation:**

```
Before: applications = "5,47,284"
After:  applications = 547284 (integer)

Before: column = "Residential Installation"
After:  column = "residential_installation"
```

---

## 4. Data Understanding Flow

### 4.1 Schema Documentation

**Input:** Cleaned dataframes  
**Process:**

1. Create data dictionary: every column, dtype, description
2. Identify key hierarchies: State → District → DISCOM
3. Identify join keys: common columns for merging
4. Document business logic: e.g., "installation count = residential + RWA"

**Output:** Data dictionary and schema documentation

**Files Involved:**

- `notebooks/02_Data_Cleaning.ipynb` — Schema details
- `BACKEND_STRUCTURE.md` — Formal schema definition

**Example Documentation:**

```
Column: application_status
Type: integer
Description: Count of applications in current state
Hierarchy: State-level aggregation
Related: Used in funnel calculation
```

---

## 5. Exploratory Data Analysis (EDA) Flow

### 5.1 Pattern Discovery

**Input:** Cleaned, validated data  
**Process:**

#### 5.1a Distribution Analysis

- Application count by state (ranking, median, std dev)
- Installation count by district
- Subsidy amount distribution
- Capacity (kW) distribution

#### 5.1b Temporal Trends

- Daily application growth rate
- Daily installation completion rate
- Subsidy redemption over time
- Cumulative adoption curves

#### 5.1c Geographic Patterns

- State-wise adoption rate (applications per capita if enriched)
- District-level performance within states
- Regional clusters and outliers
- Vendor distribution by geography

#### 5.1d Funnel Analysis

- Applications → Vendor Selected: what % advance?
- Vendor Selected → Feasibility Approved: what % advance?
- Feasibility → Installation: what % advance?
- Installation → Inspection Approved: what % advance?
- Inspection → Subsidy Redeemed: what % advance?

#### 5.1e Vendor Performance

- Vendor selection request approval rate
- Top vendor by installation count
- Vendor coverage by geography

#### 5.1f Bottleneck Identification

- Applications stuck in "pending" stages
- High rejection rate stages
- Processing delays (if can be inferred from dates)

**Output:** Exploratory findings, charts, patterns documented

**Files Involved:**

- `notebooks/03_EDA.ipynb` — Full exploratory analysis
- Saved charts to `visualizations/eda/`

---

## 6. KPI Calculation Flow

### 6.1 Metrics Generation

**Input:** Cleaned data, EDA findings  
**Process:**

#### 6.1a Adoption Metrics

```
Total Applications = SUM of application_status across all states/districts
Total Installations = SUM of installation across all states/districts
Conversion Rate (L1) = Installations / Applications * 100
Conversion Rate (L2) = Subsidy Redeemed / Applications * 100
Funnel Efficiency = Product of all stage conversion rates
```

#### 6.1b Geographic Metrics

```
State Ranking = ORDER BY installations DESC
District Ranking = ORDER BY installations DESC
Regional Comparison = Applications per capita (if enriched with population)
Adoption Rate By State = Installations / Applications per state
```

#### 6.1c Financial Metrics

```
Total Subsidy Released = SUM of total_released_amt
Subsidy Per Installation = Total Subsidy / Total Installations
Subsidy Per kW = Total Subsidy / Total Capacity (kW)
Subsidy Utilization Rate = Total Released / Total Approved * 100
```

#### 6.1d Operational Metrics

```
Vendor Approval Rate = Vendor Selected / Applications * 100
Feasibility Approval Rate = Feasibility Approved / Applications * 100
Inspection Approval Rate = Inspection Approved / Installations * 100
Pending Application Count = SUM by status (vendor_selection_pending, feasibility_pending, etc.)
```

#### 6.1e Capacity Metrics

```
Total Capacity Installed = SUM of installed_capacity (kW)
Residential vs RWA Split = SUM residential_installation, SUM rwa_installation
Capacity By State = SUM installed_capacity per state
Average System Size = Total Capacity / Total Installations
```

**Output:** KPI dataframe with all metrics calculated

**Files Involved:**

- `scripts/02_kpi_calculation.py` — KPI computation logic
- `notebooks/04_KPI_Creation.ipynb` — KPI generation narrative
- `data_cleaned/kpis.csv` — Output KPI table

**Validation:**

- Spot-check calculations against raw data
- Verify no division by zero errors
- Check for negative values where inappropriate
- Cross-validation across different aggregation levels

---

## 7. Visualization Creation Flow

### 7.1 Chart Generation

**Input:** KPIs, cleaned data  
**Process:**

#### 7.1a Chart Types (Plotly)

- **Heatmaps:** State/District adoption, subsidy distribution
- **Funnel Charts:** Application → Installation → Subsidy stages
- **Bar Charts:** State rankings, vendor comparison
- **Time-Series:** Daily application growth, installation pace
- **Waterfall:** Bottleneck stage distribution
- **Pie/Stacked Bar:** Residential vs RWA, capacity distribution

#### 7.1b Visualization Rules (See FRONTEND_GUIDELINES.md)

- Consistent color palette (primary, secondary, neutral)
- All charts have title, axis labels, legend
- Hover tooltips show exact values
- Interactive: zoom, pan, hover enabled
- Professional styling (no clutter, readable fonts)

**Output:** Static PNG/SVG exports + interactive Plotly objects

**Files Involved:**

- `scripts/03_visualization.py` — Chart generation functions
- `notebooks/05_Visualizations.ipynb` — Visualization creation
- `visualizations/` folder — All exported charts

---

## 8. Dashboard Integration Flow

### 8.1 Streamlit App Creation

**Input:** KPIs, charts, cleaned data  
**Process:**

#### 8.1a Multi-Page Architecture

```
streamlit_app.py (Main entry point)
├── pages/01_overview.py
├── pages/02_state_analysis.py
├── pages/03_district_analysis.py
├── pages/04_vendor_performance.py
├── pages/05_subsidy_pipeline.py
├── pages/06_trends.py
└── pages/07_insights_report.py
```

#### 8.1b Interactivity Layers

- **Data Loading:** Cached with `@st.cache_data`
- **Filter Widgets:** State, District, DISCOM, Date range, Metrics selector
- **Dynamic Calculations:** KPIs recalculated based on filter selections
- **Chart Updates:** Plotly charts re-render instantly on filter change
- **Performance:** <3 second page load with caching

#### 8.1c User Journey

1. User opens dashboard at Streamlit Cloud URL
2. Overview page loads: national KPIs, top states, funnel
3. User clicks "State Analysis" in sidebar
4. Selects filters: State, Date range, Metrics of interest
5. Page updates with filtered data and charts
6. User explores other pages, applies different filter combinations
7. User exports/screenshots insights for further analysis

**Output:** Live Streamlit Cloud deployment

**Files Involved:**

- `dashboard/streamlit_app.py` — Main app
- `dashboard/pages/*.py` — Analysis pages
- `dashboard/utils/` — Shared functions
- Deployment: GitHub + Streamlit Cloud

---

## 9. Insights Extraction Flow

### 9.1 Finding Generation

**Input:** All analysis (EDA, KPIs, visualizations)  
**Process:**

#### 9.1a Key Finding Identification

- Top 5 states by adoption
- Top 5 districts by installation conversion
- Largest bottleneck stages
- Best/worst vendor performance
- Geographic disparities
- Temporal trends (growth acceleration/deceleration)

#### 9.1b Insight Articulation

- Define the insight (e.g., "Bottleneck: 40% of applications stuck in Vendor Selection")
- Provide evidence (chart, KPI, data point)
- Explain business implication (what does this mean?)
- Suggest next steps (how to address?)

#### 9.1c Structured Reporting

Follow consultant style:

1. **Problem:** What is PM Surya Ghar?
2. **Approach:** Analytical methodology used
3. **Execution:** Steps taken (data cleaning, EDA, KPIs)
4. **Findings:** Key insights with evidence
5. **Recommendations:** Suggested actions (future phase)

**Output:** Insights notebook + executive summary

**Files Involved:**

- `notebooks/06_Insights_Report.ipynb` — Formal insights
- `docs/FINDINGS.md` — Summary of key findings
- `README.md` — High-level summary

---

## 10. Documentation & Publishing Flow

### 10.1 Portfolio Readiness

**Input:** All project artifacts  
**Process:**

1. Finalize all documentation files (PRD, BACKEND_STRUCTURE, etc.)
2. Create comprehensive README.md
3. Update progress.txt to "COMPLETED"
4. Commit all changes to GitHub
5. Verify Streamlit Cloud deployment is live
6. Test dashboard end-to-end

**Output:** Publication-ready GitHub repository

**Files Involved:**

- Root documentation: PRD.md, APP_FLOW.md, TECH_STACK.md, etc.
- README.md — Project overview and quick-start
- GitHub repository (public)

---

## 11. User/Analyst Journey

### 11.1 For Hiring Manager Reviewing Portfolio

1. **Discover:** See GitHub repo linked in resume/portfolio
2. **Understand:** Read README.md (2 min)
3. **Assess:** Review PRD.md, IMPLEMENTATION_PLAN.md (5 min)
4. **Explore:** Open Streamlit dashboard, test filters (10 min)
5. **Deep Dive:** Browse Jupyter notebooks (5-10 min)
6. **Evaluate:** Check code quality in `scripts/` (5 min)
7. **Decide:** Impressed? → Call for interview

### 11.2 For Analyst Using Project for Learning

1. **Setup:** Clone repo, install requirements
2. **Understand:** Read all docs and PRD
3. **Explore:** Open dashboard, test filters
4. **Learn:** Review notebooks (data cleaning, EDA, KPIs)
5. **Extend:** Modify analysis or add new KPIs
6. **Share:** Deploy own version

---

## 12. Iteration & Feedback Loop

**During Development:**

- After each phase, update `progress.txt`
- Document learnings in `lessons.md`
- Commit changes to Git with descriptive messages
- Validate results match expectations

**Post-Launch:**

- Gather feedback from testers
- Document insights and edge cases
- Plan Phase 2 improvements (predictions, recommendations, etc.)

---

## 13. Cross-References

- **PRD.md:** Project scope and objectives
- **TECH_STACK.md:** Technology stack for each step
- **BACKEND_STRUCTURE.md:** Data schemas and transformations
- **FRONTEND_GUIDELINES.md:** Visualization standards
- **IMPLEMENTATION_PLAN.md:** Phase-by-phase roadmap
- **CLAUDE.md:** AI workflow rules

---

**Document Owner:** Analytics Project Lead  
**Last Updated:** March 14, 2026
