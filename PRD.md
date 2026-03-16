# Product Requirements Document (PRD)

# PM Surya Ghar Analytics Portfolio Project

**Last Updated:** March 14, 2026  
**Project Status:** Initiating  
**Target Launch:** End of Month

---

## 1. Project Overview

This project is a comprehensive data analytics case study of the **PM Surya Ghar – Muft Bijli Yojana** (Prime Minister Rooftop Solar Scheme), a Government of India initiative to accelerate rooftop solar adoption across residential and RWA (Resident Welfare Association) segments.

The project demonstrates professional end-to-end analytics capabilities: from raw government data to actionable insights, interactive visualizations, and strategic recommendations.

**Purpose:** Create a portfolio-quality analytics project that showcases data analysis expertise to potential employers.

---

## 2. Project Objective

Build a **professional analytics system** that:

- **Understands**: Solar adoption patterns across Indian states and districts
- **Identifies**: Bottlenecks in the subsidy processing pipeline
- **Evaluates**: Vendor performance and selection effectiveness
- **Forecasts**: Future adoption trends and regional growth patterns
- **Demonstrates**: End-to-end analytics methodology suitable for modern data teams

---

## 3. Target Audience

**Primary:** Hiring managers and recruiters reviewing the analytics portfolio  
**Secondary:** Government policymakers (optional future use)  
**Context:** Hiring evaluation based on demonstrated expertise, code quality, and insight sophistication

---

## 4. Project Deliverables

### 4.1 GitHub Repository

- Clean, well-structured codebase
- Modular Python scripts (separate concerns)
- Jupyter notebooks with narrative analysis
- Professional documentation (this PRD + others)
- All data (raw and cleaned) with privacy safeguards
- `.gitignore` for sensitive or large files

### 4.2 Data Products

- **Raw datasets:** 6 CSV files from Government of India
- **Cleaned datasets:** Validated, standardized, ready for analysis
- **Derived metrics:** KPIs calculated from raw data

### 4.3 Interactive Dashboard

- Streamlit-based web application
- Multi-page interface (6+ analysis pages)
- Advanced filtering: State, District, DISCOM, Vendor, Date range, Metrics
- Responsive visualizations (Plotly charts)
- Deployed on Streamlit Cloud (publicly accessible)

### 4.4 Analysis Notebooks

1. **Data Understanding:** Dataset schema, quality, date ranges, hierarchies
2. **Data Cleaning:** Transformation steps, standardization, validation
3. **Exploratory Data Analysis:** Patterns, distributions, correlations
4. **KPI Calculation:** Metrics generation and validation
5. **Insights Report:** Key findings, visualizations, recommendations

### 4.5 Documentation

- `PRD.md` (this file) — Project scope and objectives
- `APP_FLOW.md` — Analysis narrative and workflow
- `TECH_STACK.md` — Technology choices and versions
- `BACKEND_STRUCTURE.md` — Data architecture and schemas
- `FRONTEND_GUIDELINES.md` — Dashboard design standards
- `IMPLEMENTATION_PLAN.md` — Step-by-step roadmap
- `CLAUDE.md` — AI assistant operating manual
- `README.md` — Project summary for GitHub

---

## 5. Key Features

### 5.1 Data Analysis

- **Adoption Funnel:** Track applications → vendor selection → feasibility → installation → inspection → subsidy redemption
- **Geographic Analysis:** State and district-level rankings, regional comparisons, adoption rates
- **Vendor Performance:** Selection approval rates, vendor rankings, rejection patterns
- **Subsidy Pipeline:** Current processing status, bottleneck identification, approval stage analysis
- **Time-Series Trends:** Daily/monthly growth rates, cumulative adoption curves
- **Enrichment:** External data (population, solar potential, climate) for deeper context

### 5.2 Interactive Dashboard

- **Multiple Filtering:** State (multi-select), District, DISCOM, Date range, Metrics
- **Dynamic Calculations:** KPIs update instantly based on filter selections
- **Professional Visualizations:** Heatmaps, funnels, bar charts, time-series, comparisons
- **Performance:** Responsive, cached data, <3 second page loads
- **Mobile-Ready:** Works on desktop and mobile browsers

### 5.3 Code Quality

- Modular architecture (scripts, utilities, notebooks)
- Reusable functions and components
- Clean variable naming and documentation
- Caching for performance optimization
- Error handling and data validation

---

## 6. Data Sources

### 6.1 Primary Data (Government of India)

1. **datewise.csv** — Daily aggregated metrics (time-series)
   - Columns: Date, applications, residential, RWA, installations, inspections, subsidy redeemed
   - Purpose: Track daily program progress

2. **state_master.csv** — State-level summary
   - Columns: State, application status, vendor selected, feasibility metrics, installation metrics, capacity (kW), loan data
   - Purpose: State-level overview and comparison

3. **district.csv** — District-level detail
   - Columns: State, District, application status, vendor selected, feasibility, installation, inspection, capacity metrics
   - Purpose: Granular geographic analysis

4. **discom_master.csv** — Electricity distribution company level
   - Columns: State, DISCOM, application status, vendor selected, subsidy metrics, loan data
   - Purpose: Utility-wise performance

5. **subsidy_status.csv** — Current pipeline snapshot
   - Columns: Status type, count of applications in each stage (Redeemed, Released, On Hold, Pending, etc.)
   - Purpose: Bottleneck identification

6. **vendor_selection.csv** — Vendor approval process
   - Columns: State, DISCOM, vendor requests received, pending, approved, rejected
   - Purpose: Vendor selection rate analysis

### 6.2 External Data (To Be Enriched)

- State/district population (for adoption per capita)
- Solar potential maps (for regional context)
- Climate/sunshine data (for feasibility)
- Urban/rural classification
- Any publicly available government statistics

### 6.3 Data Characteristics

- **Granularity:** Daily (datewise), State, State-District, State-DISCOM
- **Time Range:** February 1–9, 2026 (latest available)
- **Format:** CSV with Indian numeric formatting ("5,47,284")
- **Volume:** 6 files, ~10K–6M rows each
- **Quality:** Needs cleaning (numeric parsing, missing values, standardization)

---

## 7. Analytics Questions (Core)

The analysis is structured to answer these business questions:

### 7.1 Adoption Patterns

- **Q1:** Which states have the highest rooftop solar adoption (by application volume)?
- **Q2:** Which states have converted applications to installations most effectively (highest conversion rate)?
- **Q3:** Which regions show the fastest installation growth trends (day-over-day, month-over-month)?

### 7.2 Geographic Exclusions

- **Q4:** Which districts have low adoption despite vendor availability? (Underperforming)
- **Q5:** Which districts are adoption leaders? (Best performers)
- **Q6:** What is the geographic distribution of subsidy redemption?

### 7.3 Operational Bottlenecks

- **Q7:** Where are the largest bottlenecks in the subsidy processing pipeline? (Which stage has most pending?)
- **Q8:** What percentage of applications get stuck at each pipeline stage?
- **Q9:** How long does typical application stay in "pending" vs "approved" states?

### 7.4 Vendor Performance

- **Q10:** Which vendors have the highest approval rate for vendor selection requests?
- **Q11:** Which vendors process the most installations?

### 7.5 Temporal Trends

- **Q12:** What is the monthly trend in applications for rooftop solar installations?
- **Q13:** Are installations keeping pace with applications (funnel efficiency)?

---

## 8. KPIs to Generate

KPIs are ranked by importance. All must be calculated and visualized.

### 8.1 Adoption Metrics (Highest Priority)

- **Total Applications:** Current count and growth rate
- **Total Installations:** Current count, daily addition rate
- **Conversion Rate (L1):** Applications → Installations (%)
- **Conversion Rate (L2):** Applications → Subsidy Redeemed (%)
- **Conversion Rate (L3):** Installation → Inspection Approved (%)
- **Funnel Efficiency:** Multi-stage conversion cascade

### 8.2 Geographic Metrics

- **State Ranking:** By applications, installations, subsidy redeemed
- **District Ranking:** By applications, installations, capacity added (kW)
- **Adoption Per Capita:** Applications/population (requires enrichment)
- **Regional Comparison:** State-to-state performance index
- **Geographic Disparity:** Variance between top and bottom states

### 8.3 Financial Metrics

- **Total Subsidy Released:** Cumulative amount disbursed
- **Subsidy Per Installation:** Average subsidy value
- **Subsidy Per kW:** Cost efficiency metric
- **Subsidy Utilization Rate:** Released / Approved (%)
- **Cost Comparison:** By state, by vendor (if possible)

### 8.4 Operational Metrics

- **Vendor Selection Approval Rate:** Approved / Received (%)
- **Feasibility Approval Rate:** Feasibility Approved / Applications (%)
- **Inspection Approval Rate:** Inspection Approved / Installations (%)
- **Average Processing Time:** Days from application to installation (derived from datewise trends)
- **Pending Application Count:** By stage (vendor selection, feasibility, inspection)

### 8.5 Capacity Metrics (Derived)

- **Total Capacity Installed:** kW (residential + RWA, ≤10kW + >10kW)
- **Residential vs RWA Split:** Adoption by segment
- **Capacity Distribution:** By state and district
- **Average System Size:** kW per installation (cumulative capacity / installation count)

---

## 9. Success Criteria

The project is **successful** if:

✅ All interrogation requirements are implemented and documented  
✅ Dashboard is interactive, responsive, and deployed publicly  
✅ All KPIs calculated correctly and match manual spot-checks  
✅ Cleanliness and quality of analysis impresses technical hiring managers  
✅ Code demonstrates modularity, reusability, and best practices  
✅ Visualizations are professional-grade and interactive  
✅ Documentation is thorough and follows consultant-style structure (Problem → Plan → Execute → Result)  
✅ Repository is well-organized and ready for portfolio review  
✅ Helps generate interview opportunities and hiring success

---

## 10. Project Scope

### 10.1 Included

✅ Adoption analysis (funnel, conversion rates)  
✅ Geographic analysis (state, district, DISCOM levels)  
✅ Vendor performance evaluation  
✅ Subsidy pipeline bottleneck identification  
✅ Time-series trend analysis  
✅ External data enrichment (population, solar potential, climate)  
✅ All visualization types (heatmaps, funnels, time-series, comparisons, bottleneck charts)  
✅ Interactive Streamlit dashboard  
✅ Deep data cleaning and validation  
✅ Jupyter notebooks with narrative analysis  
✅ Modular Python scripts  
✅ Professional documentation

### 10.2 Out of Scope

❌ Predictive modeling / forecasting (excluded per interrogation)  
❌ Loan portfolio deep-dive (insufficient detailed data)  
❌ Cost-benefit analysis (limited cost data available)  
❌ Household-level analysis (privacy concerns)  
❌ Real-time data pipeline (static analysis of snapshots)  
❌ Database backend (CSV-based analysis sufficient for portfolio)

---

## 11. Expected Insights & Outputs

### 11.1 Key Findings (Examples)

- Top 5 states by adoption, top 5 by installation conversion
- Bottleneck stage identification (where subsidy gets stuck)
- Vendor performance rankings
- Geographic disparities and possible root causes
- Trends: Application growth, installation pace, subsidy utilization
- Capacity distribution across regions

### 11.2 Visualization Outputs

- Geographic heatmaps (state and district adoption)
- Funnel charts (application → subsidy redeemed progression)
- Bar charts (state comparisons, vendor rankings)
- Time-series plots (daily/monthly trends)
- Bottleneck waterfall charts (application status distribution)
- Capacity distribution (pie/stacked bar charts)

### 11.3 Interactive Dashboard Pages

1. **Overview:** National KPIs, top states, funnel summary
2. **State Analysis:** Filtered state metrics, district breakdowns
3. **District Analysis:** District-level detail, DISCOM comparison
4. **Vendor Performance:** Vendor rankings and approval rates
5. **Subsidy Pipeline:** Current processing stage, bottleneck analysis
6. **Trends:** Time-series analysis with state filtering
7. **Insights Report:** Key findings with visualizations

---

## 12. Cross-References

- **APP_FLOW.md:** Data ingestion → cleaning → analysis workflow
- **TECH_STACK.md:** Python, pandas, Streamlit, Plotly dependencies
- **BACKEND_STRUCTURE.md:** Dataset schemas and transformation rules
- **FRONTEND_GUIDELINES.md:** Visualization design standards
- **IMPLEMENTATION_PLAN.md:** Phase-by-phase execution roadmap
- **CLAUDE.md:** AI assistant rules and workflow
- **README.md:** Project summary for GitHub

---

## 13. Success Metrics Timeline

| Milestone                 | Target Date | Status      |
| ------------------------- | ----------- | ----------- |
| Documentation complete    | Mar 15      | In Progress |
| Data cleaning pipeline    | Mar 20      | Not Started |
| Core KPIs calculated      | Mar 25      | Not Started |
| Dashboard deployed        | Mar 30      | Not Started |
| Insights report finalized | Apr 5       | Not Started |
| Portfolio ready           | Apr 10      | Not Started |

---

**Document Owner:** Analytics Project Lead  
**Last Reviewed:** March 14, 2026  
**Next Review:** Upon completion of Documentation Phase
