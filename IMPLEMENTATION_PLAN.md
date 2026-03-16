# Implementation Plan (IMPLEMENTATION_PLAN.md)

# PM Surya Ghar Analytics — Phase-by-Phase Roadmap

**Purpose:** Step-by-step execution plan to build the complete analytics portfolio project.

---

## Phase 1: Foundation & Environment Setup

### Step 1.1: Initialize Project Structure

**Objective:** Create folder hierarchy and version control  
**Tasks:**

- [x] Initialize Git repository
- [x] Create `.gitignore` (exclude raw_data/, **pycache**, \*.pyc, .streamlit/secrets.toml)
- [x] Create folder structure: notebooks/, scripts/, data_cleaned/, visualizations/, dashboard/, docs/
- [x] Create `requirements.txt` with locked versions
- [x] Commit initial structure

**Deliverables:** Clean folder hierarchy, .gitignore, requirements.txt  
**Files to Create:** `.gitignore`, `requirements.txt`  
**Duration:** 30 minutes

---

### Step 1.2: Set Up Development Environment

**Objective:** Install dependencies locally  
**Tasks:**

- [x] Create virtual environment (venv or conda)
- [x] Install all packages from `requirements.txt`
- [x] Verify Jupyter, Python, and Streamlit installed correctly
- [x] Test basic imports (pandas, plotly, streamlit)

**Validation:**

- [x] `python --version` → 3.14.3 (Virtual Environment at .venv)
- [x] `pip list` → 170+ packages installed with verified versions
- [x] `jupyter notebook` → Verified working
- [x] `streamlit run` → Dashboard operational at http://localhost:8501

**Duration:** 20 minutes

---

### Step 1.3: Create Initial Documentation

**Objective:** Establish canonical documentation (this phase)  
**Tasks:**

- [x] Create PRD.md (Project Requirements)
- [x] Create APP_FLOW.md (Data narrative flow)
- [x] Create TECH_STACK.md (Technology inventory)
- [x] Create BACKEND_STRUCTURE.md (Data schemas)
- [x] Create FRONTEND_GUIDELINES.md (Visualization rules)
- [x] Create IMPLEMENTATION_PLAN.md (This file)
- [x] Create CLAUDE.md (AI operating manual)
- [x] Create progress.txt (Status tracker)
- [x] Create lessons.md (Learnings log)

**Deliverables:** All canonical documents in root folder  
**Duration:** 2 hours (currently executing)

---

## Phase 2: Data Understanding & Cleaning

### Step 2.1: Load and Inspect Raw Data

**Objective:** Understand datasets, identify cleaning needs  
**Tasks:**

- [x] Create `scripts/00_data_loader.py` to load all 6 CSV files
- [x] Create `notebooks/01_Data_Understanding.ipynb`
- [x] Load each dataset, inspect schema, row counts, column types
- [x] Document date ranges, missing values, data anomalies
- [x] Create data dictionary (columns × descriptions)

**Script Creates:**

- `scripts/00_data_loader.py` — Loads CSVs, returns 6 dataframes

**Notebook Outputs:**

- Dataset summaries (shape, columns, dtypes)
- First 5 rows of each dataset
- Missing value report per dataset
- Data dictionary for BACKEND_STRUCTURE.md

**Validation:**

- [x] All 6 files load without error
- [x] Row counts match expected totals (795 daily + 36 states + 792 districts + 84 DISCOMs)
- [x] Column counts match documentation
- [x] Date ranges documented (795+ time-series points verified)

**Duration:** 2 hours

---

### Step 2.2: Data Cleaning Pipeline

**Objective:** Standardize and validate data  
**Tasks:**

- [x] Create `scripts/01_data_cleaning.py` with cleaning functions
  - [x] Parse Indian numeric format ("5,47,284" → 547284) — Robust dual-fallback parser created
  - [x] Standardize column names (lowercase, underscore)
  - [x] Convert data types (int for counts, float for decimals/capacity, datetime for dates)
  - [x] Handle missing values with documented strategy
  - [x] Remove or flag duplicates
- [x] Create `scripts/utils/parser.py` — Indian number parser function
- [x] Create `notebooks/02_Data_Cleaning.ipynb` — Narrative of cleaning steps
- [x] Apply cleaning pipeline to all 6 datasets
- [x] Save cleaned outputs to `data_cleaned/` folder

**Scripts Create:**

- `scripts/01_data_cleaning.py` — Main cleaning logic
- `scripts/utils/parser.py` — Helper function for numeric parsing

**Notebook Shows:**

- Before/after sample data
- Cleaning decisions and rationale
- Validation checks passed

**Validation:**

- [x] All numeric strings converted to integers/floats → VERIFIED: 6,021,455 applications, 2,329,634 installations
- [x] Column names standardized → All 11 columns in datewise cleaned correctly
- [x] No commas in numeric values → Verified across all cleaned files
- [x] Row counts handled: 38→36 states, 794→792 districts, 87→84 DISCOMs (garbage rows removed)
- [x] Cleaned CSVs saved to `data_cleaned/` → 6 source + 3 KPI files (9 total)

**Duration:** 3 hours

---

### Step 2.3: Data Validation & Schema Verification

**Objective:** Ensure data integrity and consistency  
**Tasks:**

- [x] Validate all hierarchy relationships (state-district, state-discom) → All verified
- [x] Verify funnel logic: Applications ≥ Vendor ≥ Feasibility ≥ Install ≥ Inspect ≥ Redeem → Confirmed
- [x] Verify capacity logic: Residential + RWA = Total, ≤10kW + >10kW = Total → Verified
- [x] Cross-check row counts across datasets → All consistent (36 states, 792 districts, 84 DISCOMs)
- [x] Document any anomalies or data quality issues → Garbage rows identified and removed
- [x] Create data quality report → PHASE_2_COMPLETION_SUMMARY.md created

**Validation Checks:**

- [x] No negative counts (impossible in real data) → Verified
- [x] Funnel stages in logical order (no progression violations) → All verified
- [x] Geographic hierarchies complete (no orphaned districts) → 36 states, 792 districts complete
- [x] Aggregations consistent across levels → All cross-verified

**Deliverables:**

- Data quality report document
- Flag any outliers or anomalies for investigation

**Duration:** 2 hours

---

## Phase 3: KPI Calculation & Metrics

### Step 3.1: Create KPI Calculation Logic

**Objective:** Calculate all performance metrics  
**Tasks:**

- [x] Create `scripts/02_kpi_calculation.py` with KPI functions
- [x] Implement adoption metrics:
  - [x] Total applications, installations, subsidy redeemed
  - [x] Conversion rates (L1, L2, L3)
  - [x] Funnel efficiency
- [x] Implement geographic metrics:
  - [x] State/district rankings
  - [x] Regional comparisons
- [x] Implement financial metrics:
  - [x] Subsidy per installation, per kW
  - [x] Subsidy utilization rate
- [x] Implement operational metrics:
  - [x] Vendor/feasibility/inspection approval rates
  - [x] Pending counts by stage
- [x] Implement capacity metrics:
  - [x] Total capacity, by segment, per system
- [x] Create KPI dataframe output

**Script Creates:**

- `scripts/02_kpi_calculation.py` — All KPI functions
- Returns comprehensive KPI table

**Validation:**

- [x] All KPIs calculated without errors → 21+ national metrics verified
- [x] Manual spot-checks (e.g., conversion rate 0-100%) → 38.69% conversion verified
- [x] Cross-verify across aggregation levels (national = sum of states) → All matches confirmed
- [x] Save KPI output to `data_cleaned/kpi_*.csv` → kpis_national.csv, kpis_state.csv, kpis_district.csv created

**Duration:** 3 hours

---

### Step 3.2: Create KPI Notebook & Visualization

**Objective:** Document and visualize KPIs  
**Tasks:**

- [x] Create `notebooks/04_KPI_Creation.ipynb`
- [x] Show KPI calculations step-by-step
- [x] Create summary tables (state rankings, top metrics)
- [x] Create initial visualizations (bar charts, heatmaps)
- [x] Document all KPI formulas and assumptions

**Deliverables:**

- KPI calculation notebook with narrative
- Summary tables by state
- Initial charts (to reuse in dashboard)

**Duration:** 2 hours

---

## Phase 4: Exploratory Data Analysis (EDA)

### Step 4.1: Comprehensive EDA Analysis

**Objective:** Discover patterns, distributions, trends, bottlenecks  
**Tasks:**

- [ ] Create `notebooks/05_EDA.ipynb`
- [ ] Perform distribution analysis (KPIs by state, district)
- [ ] Perform temporal analysis (daily trends, growth rates)
- [ ] Perform geographic analysis (state rankings, regional patterns)
- [ ] Perform funnel analysis (stage-by-stage progression)
- [ ] Perform vendor analysis (vendor rankings, coverage)
- [ ] Perform bottleneck analysis (where applications get stuck)
- [ ] Create exploratory charts (saved to `visualizations/eda/`)

**Analysis Sections:**

1. **Adoption Patterns:** Top states, fastest-growing districts
2. **Geographic Distribution:** State/district rankings, disparities
3. **Vendor Performance:** Approval rates, vendor market share
4. **Subsidy Pipeline:** Current bottlenecks, processing status
5. **Temporal Trends:** Daily/monthly growth

**Deliverables:**

- EDA notebook with detailed analysis
- 15-20 exploratory charts
- Pattern documentation

**Duration:** 4 hours

---

### Step 4.2: Findings & Bottleneck Identification

**Objective:** Answer core business questions  
**Tasks:**

- [ ] Identify answers to all 12 core analytics questions (See PRD.md)
- [ ] Document bottleneck stages (where applications get stuck)
- [ ] Identify underperforming regions
- [ ] Identify top performers
- [ ] Document key trends and patterns
- [ ] Create preliminary insights document

**Deliverables:**

- Findings summary document
- Bottleneck identification report
- Support charts and evidence

**Duration:** 2 hours

---

## Phase 5: Dashboard Development

### Step 5.1: Create Reusable Dashboard Components

**Objective:** Build modular, reusable functions  
**Tasks:**

- [ ] Create `dashboard/utils/data_loader.py` — Load & cache cleaned data
- [ ] Create `dashboard/utils/filters.py` — Filter widgets (state, district, date, metrics)
- [ ] Create `dashboard/utils/charts.py` — Chart generation functions (funnel, heatmap, bar, line, etc.)
- [ ] Create `dashboard/utils/kpi_calculators.py` — Filter-aware KPI recalculation
- [ ] Create `dashboard/config.py` — Constants, column definitions, filter options

**Utilities Create:**

- Caching mechanism (`@st.cache_data`)
- Reactive filters that trigger chart updates
- Standardized chart functions with FRONTEND_GUIDELINES compliance
- Dynamic KPI calculation based on user filters

**Validation:**

- [ ] All functions work independently
- [ ] No errors when loading data
- [ ] Filters produce expected output
- [ ] Chart rendering <2 seconds

**Duration:** 3 hours

---

### Step 5.2: Build Dashboard Pages (7 Total)

**Objective:** Create interactive analysis pages

#### 5.2a: Overview Page

**File:** `dashboard/pages/01_overview.py`  
**Components:**

- National-level KPI cards (total applications, installations, subsidy)
- Adoption funnel chart (national level)
- Top 10 states by installations
- Geographic heatmap (state adoption rate)
- Key metrics summary

**No Filters:** National view only

**Duration:** 1.5 hours

---

#### 5.2b: State Analysis Page

**File:** `dashboard/pages/02_state_analysis.py`  
**Filters:**

- State (multi-select)
- Date range (datewise data, if available)
- Metrics selector (which KPIs to display)

**Components:**

- Filtered state metrics summary
- Funnel chart (state-level conversion)
- District breakdown (pie or bar)
- Filtered metrics table
- Trend chart (if date range)

**Duration:** 2 hours

---

#### 5.2c: District Analysis Page

**File:** `dashboard/pages/03_district_analysis.py`  
**Filters:**

- State (cascading → populates district list)
- District (multi-select, auto-filter by state)
- Date range (optional)

**Components:**

- District metrics summary
- District ranking (bar chart)
- DISCOM breakdown (parent district)
- Filtered data table (all districts in selected state)
- Comparison chart (district vs district)

**Duration:** 2 hours

---

#### 5.2d: Vendor Performance Page

**File:** `dashboard/pages/04_vendor_performance.py`  
**Filters:**

- State (multi-select, optional)
- Date range (optional)

**Components:**

- Vendor selection approval rate (summary KPI)
- Vendor ranking (by approvals)
- Approval rate trend (if time available)
- Vendor distribution by state (pie/bar)
- Pending vendor requests analysis

**Duration:** 1.5 hours

---

#### 5.2e: Subsidy Pipeline Page

**File:** `dashboard/pages/05_subsidy_pipeline.py`  
**Filters:** None (snapshot view)

**Components:**

- Pipeline status waterfall (current state)
- Status distribution (pie chart)
- Amount vs count comparison
- Current bottleneck identification
- Pending applications by stage

**Duration:** 1 hour

---

#### 5.2f: Trends Analysis Page

**File:** `dashboard/pages/06_trends.py`  
**Filters:**

- State (multi-select, optional)
- Date range (from datewise data)
- Metric selection (applications, installations, inspections, subsidy)

**Components:**

- Multi-line time-series chart (Applications, Installations, Inspections)
- Growth rate calculation
- Filtered state comparison (if state selected)
- Cumulative adoption curve
- Acceleration/deceleration trend

**Duration:** 2 hours

---

#### 5.2g: Insights Report Page

**File:** `dashboard/pages/07_insights_report.py`  
**Components:**

- Executive summary (key findings)
- Top performers (states, vendors)
- Bottleneck analysis (where stuck?)
- Geographic disparities (high vs low adoption regions)
- Recommendations (future phase)

**Duration:** 1.5 hours

---

### Step 5.3: Main Entry Point

**Objective:** Build dashboard home page  
**Tasks:**

- [ ] Create `dashboard/streamlit_app.py`
- [ ] Set page title, favicon, layout
- [ ] Create sidebar navigation to all pages
- [ ] Add GitHub repo link
- [ ] Add project description

**Duration:** 1 hour

---

### Step 5.4: Dashboard Testing & Performance Optimization

**Objective:** Ensure dashboard is fast and bug-free  
**Tasks:**

- [ ] Test all pages load without errors
- [ ] Test all filters work correctly (single, multi-select, cascading)
- [ ] Test charts update <3 seconds on filter change
- [ ] Verify caching works (no redundant data loads)
- [ ] Test edge cases (empty filter, single item, large selections)
- [ ] Check for memory leaks (repeated filter changes)
- [ ] Test on different browsers (Chrome, Firefox, Safari)
- [ ] Test on mobile screen size

**Validation:**

- [ ] All pages render
- [ ] No errors in Streamlit console
- [ ] Performance metrics met (<3 sec response)
- [ ] Visualizations are polished

**Duration:** 2 hours

---

## Phase 6: Streamlit Cloud Deployment

### Step 6.1: Prepare for Deployment

**Objective:** Set up GitHub and deployment infrastructure  
**Tasks:**

- [ ] Ensure all code is committed to GitHub (public repo)
- [ ] Create `secrets.toml` (if API keys needed, leave empty for now)
- [ ] Verify `.gitignore` excludes large files and secrets
- [ ] Test that cloning repo → installing requirements → running app works locally

**Duration:** 1 hour

---

### Step 6.2: Deploy to Streamlit Cloud

**Objective:** Make dashboard accessible publicly  
**Tasks:**

- [ ] Go to streamlit.io/cloud
- [ ] Connect GitHub account
- [ ] Select repository and main file (`dashboard/streamlit_app.py`)
- [ ] Deploy
- [ ] Get public URL
- [ ] Test live deployment (all pages, all filters)

**Deliverables:**

- Live Streamlit Cloud URL
- Public accessible dashboard

**Duration:** 30 minutes

---

## Phase 7: Documentation & README

### Step 7.1: Create Comprehensive README.md

**Objective:** Explain project for GitHub visitors  
**Tasks:**

- [ ] Create `README.md` in root folder
- [ ] Follow consultant-style structure:
  1. Problem Identification: What is PM Surya Ghar?
  2. Solution Planning: Analysis approach
  3. Execution: Data pipeline, KPIs, visualizations
  4. Results: Key findings
  5. Outcomes: What we learned
- [ ] Add live dashboard link
- [ ] Add project structure explanation
- [ ] Add how to run locally (setup instructions)
- [ ] Add key insights summary
- [ ] Add visualization examples (screenshots)

**Duration:** 2 hours

---

### Step 7.2: Create Supplementary Documentation

**Objective:** Add supporting docs  
**Tasks:**

- [ ] Create `docs/FINDINGS.md` — Detailed findings and insights
- [ ] Create `docs/METHODOLOGY.md` — Analysis approach explanation
- [ ] Create `docs/DATA_QUALITY.md` — Data cleaning decisions
- [ ] Update `progress.txt` to "COMPLETED"
- [ ] Update `lessons.md` with learnings

**Deliverables:**

- Supporting documentation
- Methodology explanation

**Duration:** 2 hours

---

## Phase 8: Final Review & Polish

### Step 8.1: Quality Assurance

**Objective:** Ensure portfolio-ready quality  
**Tasks:**

- [ ] Code review: Check for consistency, comments, naming
- [ ] Documentation review: All docs complete, readable, technically accurate
- [ ] Visualization review: Charts are professional, follow FRONTEND_GUIDELINES
- [ ] Functionality review: All features work correctly
- [ ] Spelling & grammar review: No typos in docs or UI

**Duration:** 2 hours

---

### Step 8.2: Portfolio Packaging

**Objective:** Prepare for hiring managers  
**Tasks:**

- [ ] Ensure GitHub repo is public
- [ ] README is comprehensive
- [ ] Live dashboard URL is accessible
- [ ] Code is clean and well-commented
- [ ] All documentation is present and polished
- [ ] Create a project summary slide (optional)

**Deliverables:**

- Portfolio-ready GitHub repo
- Live dashboard
- Professional documentation

**Duration:** 1 hour

---

## Phase 6: Advanced Analytics - Bottleneck Analysis

### Objective: Deep-dive operational analytics to identify process bottlenecks

**File:** `dashboard/pages/08_bottleneck_analysis.py`

### Components Implemented:

✅ **Application Funnel Analysis**

- 6-stage funnel: Applications → Vendor → Feasibility → Installation → Inspection → Subsidy
- Stage-wise dropout %calculation
- Key insight: 61% dropout Feasibility→Installation

✅ **Pending Applications Tracking**

- 5 pipeline stages analysis
- Pending counts and percentages
- Identifies bottleneck stages

✅ **Geographic Bottleneck Map**

- State-level performance ranking
- Conversion rates (App→Installation) by state
- Geographic disparity identification

✅ **Processing Speed Analysis**

- Daily throughput comparison
- 7-day rolling average
- Cumulative backlog projection
- Years to clear calculation

✅ **Critical Recommendations**

- 🔴 CRITICAL findings
- 🟠 HIGH priority actions
- Actionable improvement strategies

### Dashboard Integration:

✅ Separate page accessible from navigation  
✅ Error handling with fallbacks  
✅ Cached data loading  
✅ Responsive layout  
✅ Color-coded severity indicators

### Validation:

✅ Funnel chart renders correctly  
✅ All 5 analysis sections working  
✅ Data validation in place  
✅ Error messages informative  
✅ Performance optimized with caching

**Status:** ✅ COMPLETE  
**Duration:** 4 hours

---

## Timeline Summary

| Phase                       | Estimated Duration | Target Completion   |
| --------------------------- | ------------------ | ------------------- |
| Phase 1: Setup              | 3 hours            | Day 1               |
| Phase 2: Data cleaning      | 7 hours            | Day 2               |
| Phase 3: KPI Calculation    | 5 hours            | Day 3               |
| Phase 4: EDA                | 6 hours            | Day 4               |
| Phase 5: Dashboard          | 15 hours           | Day 6               |
| Phase 6: Advanced Analytics | 4 hours            | Day 7               |
| Phase 7: Deployment         | 1.5 hours          | Day 7               |
| Phase 8: Documentation      | 4 hours            | Day 7               |
| Phase 9: Polish & Final     | 3 hours            | Day 8               |
| **TOTAL**                   | **~48 hours**      | **~1 week focused** |

---

## Execution Notes

✅ **Document-Driven Development:** Every step references PRD, APP_FLOW, BACKEND_STRUCTURE, FRONTEND_GUIDELINES  
✅ **Incremental Commits:** After each step, commit changes with descriptive message  
✅ **Progress Tracking:** Update `progress.txt` after completing each phase  
✅ **Validation Checkpoints:** Each step includes validation criteria  
✅ **Modularity:** Scripts are reusable, dashboard components are DRY  
✅ **Quality First:** Polish and attention to detail throughout

---

## Cross-References

- **PRD.md:** Project scope, KPIs, deliverables
- **APP_FLOW.md:** Data narrative, analysis logic
- **TECH_STACK.md:** Technology specifications
- **BACKEND_STRUCTURE.md:** Data schemas, validation rules
- **FRONTEND_GUIDELINES.md:** Visualization standards
- **CLAUDE.md:** AI assistant rules

---

**Document Owner:** Analytics Project Lead  
**Last Updated:** March 14, 2026  
**Status:** Ready for execution
