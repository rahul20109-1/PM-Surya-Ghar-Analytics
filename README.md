# PM Surya Ghar Analytics — Portfolio Project

## Government of India Rooftop Solar Scheme Data Analysis

**Status:** ✅ COMPLETE (All Phases 1-5 Finished)  
**Live Dashboard:** 🌐 http://localhost:8501 (Running Locally)  
**Documentation:** Complete (12+ comprehensive documentation files)

---

## 📋 Project Overview

This is a **professional end-to-end analytics portfolio project** analyzing the adoption and performance of **PM Surya Ghar – Muft Bijli Yojana** (Prime Minister Rooftop Solar Scheme), a Government of India initiative to accelerate rooftop solar adoption across India.

The project demonstrates:

- ✅ Data cleaning & preprocessing at scale
- ✅ SQL-like aggregations and transformations with pandas
- ✅ KPI design and metric calculation
- ✅ Exploratory data analysis with visual patterns
- ✅ Interactive web dashboard (Streamlit)
- ✅ Professional documentation & reproducible workflows
- ✅ Portfolio-ready GitHub repository

---

## 🎯 Problem Identification

**Why This Matters:**
The PM Surya Ghar initiative is one of India's largest renewable energy adoption programs. Understanding:

- **Where** adoption is happening (state & district level)
- **How FAST** installations are growing
- **What** bottlenecks slow down subsidy processing
- **Which** vendors dominate the market

...provides actionable insights for government stakeholders and demonstrates critical data analyst skills.

---

## 🔍 Core Analytics Questions

This analysis answers:

1. **Adoption Patterns:**
   - Which states have the highest rooftop solar adoption?
   - Which states convert applications to installations most effectively?
   - Which regions show fastest installation growth?

2. **Geographic Performance:**
   - Which districts are adoption leaders vs. underperformers?
   - What geographic disparities exist?
   - How does solar potential and population correlate with adoption?

3. **Operational Bottlenecks:**
   - Where do applications get stuck in the approval pipeline?
   - What percentage fail at each stage (vendor selection, feasibility, inspection)?
   - How long do typical approvals take?

4. **Vendor Market:**
   - Which vendors have highest approval rates?
   - Which vendors process most installations?
   - What is vendor coverage by geography?

5. **Financial Metrics:**
   - How much subsidy has been (redeemed/released)?
   - What is the subsidy per installation?
   - What is the cost efficiency (subsidy per kW)?

---

## 📊 Solution Approach

### Data Architecture

- **Raw Data:** 6 CSV datasets from Government of India (state, district, DISCOM, daily, subsidy, vendor levels)
- **Cleaned Data:** Standardized, validated datasets in `data_cleaned/`
- **KPIs:** Adoption metrics, geographic metrics, financial metrics, operational metrics, capacity metrics
- **Storage:** CSV-based (no database needed for portfolio)

### Analysis Pipeline

```
Raw Data (6 CSVs)
    ↓
[Data Cleaning]
Parse Indian numerics, standardize columns, validate hierarchies
    ↓
[KPI Calculation]
Conversion rates, approval rates, subsidy metrics, capacity metrics
    ↓
[Exploratory Analysis]
Distributions, trends, patterns, bottlenecks
    ↓
[Interactive Dashboard]
Streamlit app with State, District, DISCOM, Date, Metrics filters
    ↓
[Insights & Findings]
Top performers, bottleneck analysis, recommendations
```

### Key Metrics (KPIs)

**Adoption Funnel:**

- Applications → Vendor Selected → Feasibility Approved → Installed → Inspected → Subsidy Redeemed

**By State & District:**

- Application count, Installation count, Subsidy redeemed
- Conversion rates at each funnel stage
- Growth trends (daily, monthly)

**Financial:**

- Total subsidy distributed (₹)
- Subsidy per installation
- Subsidy per kW (cost efficiency)

**Operational:**

- Vendor approval rate, Feasibility approval rate, Inspection approval rate
- Pending applications by stage (bottleneck identification)

---

## 🏗️ Project Structure

```
PM-Surya-Ghar-Analysis/
│
├── 📄 Documentation (Canonical)
│   ├── PRD.md                      (Product Requirements)
│   ├── APP_FLOW.md                 (Data narrative & workflow)
│   ├── TECH_STACK.md               (Technology inventory, locked versions)
│   ├── BACKEND_STRUCTURE.md        (Data schemas, validation rules)
│   ├── FRONTEND_GUIDELINES.md      (Visualization design standards)
│   ├── IMPLEMENTATION_PLAN.md      (Step-by-step roadmap)
│   ├── CLAUDE.md                   (AI assistant operating manual)
│   ├── progress.txt                (Current project status)
│   └── lessons.md                  (Learnings & decisions log)
│
├── 🗂️ Data
│   ├── raw_data/                   (Read-only, local only)
│   │   ├── datewise.csv
│   │   ├── state_master.csv
│   │   ├── district.csv
│   │   ├── discom_master.csv
│   │   ├── subsidy_status.csv
│   │   └── vendor_selection.csv
│   │
│   └── data_cleaned/               (Processed, validated datasets)
│       ├── datewise_clean.csv
│       ├── state_master_clean.csv
│       ├── district_clean.csv
│       ├── kpis.csv
│       └── README.md (data dictionary)
│
├── 📓 Analysis (Jupyter Notebooks)
│   ├── notebooks/01_Data_Understanding.ipynb
│   ├── notebooks/02_Data_Cleaning.ipynb
│   ├── notebooks/03_EDA.ipynb
│   ├── notebooks/04_KPI_Creation.ipynb
│   ├── notebooks/05_Visualizations.ipynb
│   └── notebooks/06_Insights_Report.ipynb
│
├── 🐍 Reusable Scripts
│   ├── scripts/00_data_loader.py
│   ├── scripts/01_data_cleaning.py
│   ├── scripts/02_kpi_calculation.py
│   ├── scripts/03_visualization.py
│   └── scripts/utils/
│       ├── parser.py (Indian number parsing)
│       └── validators.py
│
├── 📊 Dashboard (Streamlit)
│   ├── dashboard/streamlit_app.py
│   ├── dashboard/pages/
│   │   ├── 01_overview.py
│   │   ├── 02_state_analysis.py
│   │   ├── 03_district_analysis.py
│   │   ├── 04_vendor_performance.py
│   │   ├── 05_subsidy_pipeline.py
│   │   ├── 06_trends.py
│   │   └── 07_insights_report.py
│   ├── dashboard/utils/
│   │   ├── filters.py
│   │   ├── charts.py
│   │   ├── kpi_calculators.py
│   │   └── data_loader.py
│   └── dashboard/config.py
│
├── 📈 Visualizations (Exports)
│   ├── visualizations/eda/
│   ├── visualizations/kpis/
│   └── visualizations/dashboard_screenshots/
│
├── 📚 Documentation
│   ├── docs/FINDINGS.md (Detailed findings)
│   ├── docs/METHODOLOGY.md (Analysis approach)
│   └── docs/DATA_QUALITY.md (Data cleaning decisions)
│
├── ⚙️ Configuration
│   ├── requirements.txt
│   ├── .gitignore
│   └── README.md (This file)
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (tested on 3.14.3)
- Virtual Environment (.venv recommended)

### Local Setup

**1. Clone/Navigate to Repository**

```bash
cd "c:\Users\Rahul\Desktop\Data Analysis\Suryaghar_Data Analysis Project"
```

**2. Verify Virtual Environment**

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Verify Dependencies Installed**

```bash
pip list | grep -E "streamlit|pandas|plotly"
# Should show: streamlit 1.55.0+, pandas 2.3.3+, plotly 6.6.0+
```

**4. Run Streamlit Dashboard (RECOMMENDED)**

```bash
# Windows
.venv\Scripts\python -m streamlit run dashboard/streamlit_app.py

# macOS/Linux
python -m streamlit run dashboard/streamlit_app.py
```

**Dashboard opens at:** `http://localhost:8501`

**5. Explore Analysis Notebooks (Optional)**

```bash
jupyter notebook
# Open notebooks/01_Data_Understanding.ipynb through notebooks/05_EDA.ipynb
```

**6. Dashboard Features**

The Streamlit dashboard provides 7 interactive analytics pages:

**Core Pages (6):**

- **Overview Page:** National KPIs, adoption trends, state rankings
- **State Analysis:** Filter by state, explore state-level metrics
- **District Analysis:** Drill down to district level performance
- **Vendor Performance:** Vendor rankings and approval analysis
- **Trends Page:** Temporal adoption patterns
- **About:** Project methodology, data quality, technology stack

**Advanced Analytics (1):**

- **🚨 Bottleneck Analysis:** Operational deep-dive (NEW - Phase 6)
  - Application funnel with 6-stage flow and dropout analysis
  - Pending applications tracking by pipeline stage
  - Geographic bottleneck mapping showing state performance
  - Processing speed analysis with backlog projections
  - Critical findings: 61% loss Feasibility→Installation, 5,000+/day deficit

**Dashboard Status:** ✅ Live and operational at http://localhost:8501

---

## 📋 Key Findings (Executive Summary)

### Core Metrics (VERIFIED)

- **Total Applications:** 6,021,455 ✅
- **Total Installations:** 2,329,634 ✅
- **Overall Conversion Rate:** 38.69% ✅
- **Total Subsidy Redeemed:** ₹2,201,659 Million ✅

### Geographic Coverage

- **States Analyzed:** 36 Union Territories + States
- **Districts Analyzed:** 792 Districts
- **DISCOMs (Distribution Companies):** 84 Utility Partners
- **Time Period:** Daily time-series with 795+ data points

### Analysis Insights

- Full adoption funnel analysis (Applications → Installations → Subsidies)
- State-level ranking and performance comparison
- District-level deep-dive analysis capability
- Vendor and operational bottleneck identification
- Financial subsidy metrics (per unit, per kW analysis)

### Operational Insights (Phase 6 Advanced Analytics)

- **🔴 CRITICAL:** 61% of feasibility-approved applications never reach installation stage
- **🔴 CRITICAL:** Daily deficit of 5,000+ applications (received > completed installations)
- **🟠 HIGH:** Geographic variance in conversion rates (3% - 65% across states)
- **🟠 HIGH:** Inspection processing delays creating pipeline backlog
- **Backlog Status:** Growing unsustainably; years to clear at current processing rate

---

## 📊 Key Metrics & KPIs

| Category        | Metric                        | Value       | Status      |
| --------------- | ----------------------------- | ----------- | ----------- |
| **Adoption**    | Total Applications            | 6,021,455   | ✅ Complete |
|                 | Total Installations           | 2,329,634   | ✅ Complete |
|                 | Conversion Rate (App→Install) | 38.69%      | ✅ Complete |
| **Geographic**  | States Analyzed               | 36          | ✅ Complete |
|                 | Districts Analyzed            | 792         | ✅ Complete |
|                 | DISCOMs Analyzed              | 84          | ✅ Complete |
| **Financial**   | Total Subsidy Redeemed        | ₹2,201,659M | ✅ Complete |
|                 | Subsidy Per Installation      | ₹945,341    | ✅ Complete |
| **Operational** | Inspections Completed         | 2,267,907   | ✅ Complete |
|                 | Inspection Approval Rate      | 97.3%       | ✅ Complete |

---

## 🛠️ Technology Stack

**Language:** Python 3.11  
**Data Processing:** pandas, numpy  
**Visualization:** Plotly, Matplotlib, Seaborn  
**Dashboard:** Streamlit  
**Notebooks:** Jupyter  
**Deployment:** Streamlit Cloud  
**Version Control:** Git, GitHub  
**Code Quality:** Black, Pylint, Flake8

---

## 📈 Execution Roadmap

| Phase                               | Duration | Status         |
| ----------------------------------- | -------- | -------------- |
| **Phase 1:** Foundation & Setup     | 3h       | ✅ COMPLETE    |
| **Phase 2:** Data Cleaning          | 7h       | ✅ COMPLETE    |
| **Phase 3:** KPI Calculation        | 5h       | ✅ COMPLETE    |
| **Phase 4:** Exploratory Analysis   | 6h       | ✅ COMPLETE    |
| **Phase 5:** Dashboard Development  | 15h      | ✅ COMPLETE    |
| **Phase 6:** Testing & Optimization | 2h       | ✅ COMPLETE    |
| **Phase 7:** Documentation & Polish | 3h       | 🔄 IN PROGRESS |
| **Total Actual Time**               | ~41h     | 95% COMPLETE   |

**Completion Status:** March 15, 2026 — All Core Phases Finished, Final Documentation Underway

#### Phase Details & Completion

- **Phase 1 (Foundation):** ✅ 10+ documentation files, project structure, git setup
- **Phase 2 (Data Cleaning):** ✅ Fixed 93.7% data corruption, parser robustness, garbage row removal
- **Phase 3 (KPI Calculation):** ✅ 21+ verified metrics, state-level analysis, district-level analysis
- **Phase 4 (EDA):** ✅ Adoption pattern analysis, trend identification, bottleneck mapping
- **Phase 5 (Dashboard):** ✅ Streamlit app operational at http://localhost:8501 with 170+ dependencies installed
- **Phase 6 (Testing):** ✅ All pages verified, filters tested, data caching optimized
- **Phase 7 (Documentation):** 🔄 Final README/IMPLEMENTATION_PLAN updates in progress

---

## 📖 Documentation Reference

For detailed information, see:

- **Project Scope:** Read [PRD.md](PRD.md)
- **Data Architecture:** Read [BACKEND_STRUCTURE.md](BACKEND_STRUCTURE.md)
- **Analysis Workflow:** Read [APP_FLOW.md](APP_FLOW.md)
- **Implementation Steps:** Read [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
- **Tech Specifications:** Read [TECH_STACK.md](TECH_STACK.md)
- **Dashboard Design:** Read [FRONTEND_GUIDELINES.md](FRONTEND_GUIDELINES.md)
- **Execution Progress:** See [progress.txt](progress.txt)
- **Learnings & Decisions:** See [lessons.md](lessons.md)

---

## 👤 About This Project

**Purpose:** Professional analytics portfolio project demonstrating end-to-end data analysis capabilities for Data Analyst / Data Engineering roles.

**Showcase Value:**

- ✅ Real government dataset (credible source)
- ✅ Professional code organization and documentation
- ✅ Interactive visualizations with filtering
- ✅ SQL-like data transformations with pandas
- ✅ Reproducible, well-documented workflow
- ✅ Scalable dashboard architecture

**Portfolio Impact:**
This project demonstrates to hiring managers:

1. **Technical Skills:** Python, pandas, Streamlit, data processing
2. **Analytical Thinking:** Asking right questions, deriving metrics
3. **Communication:** Explaining complex analysis to non-technical audience
4. **Attention to Detail:** Professional code, documentation, visualization polish
5. **Self-Direction:** End-to-end project autonomy and delivery

---

## 🤝 Contributing

This is a personal portfolio project. For feedback or suggestions:

- Open an issue describing improvements
- Submit pull request with enhancements
- Share insights or findings

---

## 📝 License

This project is open source. Feel free to fork and adapt for your own portfolio.

---

## 📞 Contact & Questions

For questions or feedback about the analysis, reach out via GitHub issues.

---

## 🔗 Deployment & Live Links

**GitHub Repository:** [Link]  
**Live Dashboard:** [Coming Soon — Streamlit Cloud]  
**Project Blog Post:** [Coming Soon]

---

**Last Updated:** March 14, 2026  
**Project Status:** 🚀 In Active Development  
**Next Milestone:** Complete Phase 2 (Data Cleaning) by March 20, 2026
