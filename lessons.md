# Project Learnings & Technical Decisions

# PM Surya Ghar Analytics — Lessons Log

**Purpose:** Document learnings, decisions, and trade-offs throughout development.

---

## March 14, 2026

### Decision: Documentation-First Approach

**Rationale:** Creating comprehensive canonical docs (PRD, APP_FLOW, TECH_STACK, etc.) before implementation ensures:

- Clear scope definition (no scope creep)
- Aligned team/AI assistant workflow
- Reusable reference materials
- Professional portfolio presentation
  **Trade-off:** More upfront documentation time, but faster execution later
  **Reversibility:** High — Can adjust docs as implementation reveals issues

---

### Decision: Streamlit for Dashboard (NOT custom web app)

**Rationale:**

- Fastest path to interactive web app (Python-native)
- Free deployment on Streamlit Cloud
- Sufficient for portfolio demonstration
- No complex backend needed
  **Alternative Considered:** Flask/FastAPI (more control but slower to build)
  **Trade-off:** Less UI customization vs. speed of execution
  **Reversibility:** Medium — Would need to rebuild dashboard in Flask if scaling further

---

### Decision: Modular Architecture for Scripts

**Rationale:**

- Separation of concerns (loading, cleaning, KPI calc, viz)
- Reusable across notebooks and dashboard
- Easier to test individual functions
- Professional signal for hiring
  **Trade-off:** More initial code boilerplate vs. long-term maintainability
  **Reversibility:** High — Can reorganize if needed

---

### Decision: CSV-Based Analysis (NO database)

**Rationale:**

- Data volume manageable with pandas (~6M rows max)
- No need for complex queries
- Simpler deployment (no DB setup)
- Portfolio focus, not production system
  **Assumption:** Data fits in memory; if not, refactor to chunks later
  **Reversibility:** High — Can add database layer later if needed

---

### Decision: External Data Enrichment (Population, Solar Potential)

**Rationale:**

- Provides richer context for adoption analysis
- Allows per-capita metrics (benchmark against local population)
- Stronger insights (adoption gap identification)
  **Implementation:**
- Gather from public sources (Census, NREL solar atlas)
- Join to state/district level
- Document sources in README
  **Timeline Impact:** +2-4 hours for data sourcing and integration
  **Priority:** Medium — Nice to have, not critical for MVP

---

---

## March 15, 2026

### Critical Discovery: Data Corruption in Original Cleaning Pipeline

**Problem:** KPI metrics didn't align with raw CSV totals

- Reported: 377,056 applications
- Actual (raw): 6,021,455 applications
- Data loss: 93.7% of records

**Root Cause:** Indian number format parser failing silently

- Code attempted to parse "9,017" directly to float
- Conversion failed, returning NaN → filled with 0.0
- Only first row parsed correctly (value "6")
- **Impact:** Only ~17K records actually processed instead of 6M+

**Solution Approach:**

1. Created `01_data_cleaning_v2.py` with robust dual-fallback number parser
2. Created standalone `clean_data_direct.py` (no module dependencies)
3. Verified output: 6,021,455 applications ✓
4. Cross-checked against raw CSV sums

**Key Learning:** Always validate data at multiple levels

- Spot-check raw files
- Compare totals before/after cleaning
- Never assume single-point calculations are correct
- Silent failures in data pipelines are dangerous

**Process Improvement:** Added comprehensive data quality checks

- Null value counts per file
- Duplicate row detection
- Negative value detection in numeric columns
- Final verification against known totals

---

### Decision: Remove Garbage Footer Rows from Datasets

**Rationale:** Analysis revealed state_master, district, and discom files had 2-3 footer rows with null IDs

- These appeared to be total/aggregate rows
- Would skew geographic analysis if included
- Clean boundary between valid records and totals is clear

**Action:** Removed null-ID rows

- state_master: 38→36 rows (2 removed)
- district: 794→792 rows (2 removed)
- discom_master: 87→84 rows (3 removed)

**Result:** Clean data boundaries, proper hierarchical structure maintained

---

## Implementation Notes — Phase Completions

### Phase 1: Foundation ✅

- Documentation structure created (10+ detailed guides)
- Directory hierarchy established
- Git repository initialized
- Complete environment setup

### Phase 2: Data Cleaning ✅ (COMPLETED WITH CORRECTIONS)

- Original: Discovered and fixed critical data corruption
- Cleaned all 6 source datasets
- Removed garbage footer rows
- Regenerated all KPI files from corrected data
- All cleaned files verified: 0 nulls, 0 duplicates (main files)
- **Status: READY FOR ANALYSIS**

### Phase 3: KPI Calculation ✅

- Recalculated all 21+ national KPIs with corrected data
- Generated state-level KPIs (36 states)
- Generated district-level KPIs (792 districts)
- All KPIs verified and documented

### Phase 4: EDA ✅

- Fixed notebook path resolution issues
- EDA notebook now loads all data correctly
- Visualizations rendered with corrected metrics
- State rankings updated (Andhra Pradesh now #1)

---

## March 15, 2026 (Afternoon) — Phase 5: Dashboard Implementation

### Issue: Streamlit and Dependencies Not Installed

**Problem:**

- Attempted to run Streamlit dashboard but got `ModuleNotFoundError: No module named 'streamlit'`
- All required packages from requirements.txt failed to install

**Root Cause:**

- Python 3.14 compatibility issue
- Missing `pkg_resources` module (part of setuptools)
- Initial pip install -r requirements.txt failed silently without proper error handling

**Solution Applied:**

1. Used `install_python_packages()` tool to install setuptools and wheel first
2. Installed streamlit and core packages separately
3. Installed remaining packages (streamlit-aggrid, jupyter, visualization libraries)
4. All packages installed into virtual environment (.venv)
5. Verified installation: 170+ packages successfully installed

**Key Learning:**

- Python 3.14 has breaking changes with certain package managers
- Always install build tools (setuptools, wheel) before other packages
- Virtual environments are crucial for isolation (packages installed in .venv/Scripts/python.exe, NOT system Python)
- Different Python interpreters in same system can cause confusion

**Resolution Timeline:**

- Detected issue: Package import failed
- Root cause identified: setuptools missing
- Fixed: 2-3 minutes to install all dependencies
- Dashboard now running successfully

**Technical Decision: Virtual Environment Strategy**

- Virtual environment auto-created during early setup
- All packages installed to .venv (not system Python)
- Dashboard must be run via `.venv/Scripts/python -m streamlit run`
- Eliminates conflicts with system Python packages

---

## Phase Completions (Updated)

### Phase 5: Streamlit Dashboard ✅ COMPLETE

- Dashboard structure created (streamlit_app.py + utilities)
- Connected to cleaned data (all 6 source files + 3 KPI files)
- Components implemented:
  - KPI card displays with formatted metrics
  - Adoption trend charts
  - State ranking visualizations
  - Conversion funnel analysis
  - Interactive filters
- Error handling: Proper messages if data not found
- Performance: Data caching enabled with @st.cache_data
- **Status:** Running on http://localhost:8501

### Next Phases:

- Phase 6: Performance optimization & multi-page testing
- Phase 7: Deployment (Streamlit Cloud)
- Phase 8: Final documentation & portfolio presentation

- _To be updated during development_

### Phase 6: Deployment

- _To be updated after deployment_

### Phase 7: Documentation

- _To be updated during final phase_

---

## Technical Debts & Future Work

| Debt       | Severity | Fix | Timeline |
| ---------- | -------- | --- | -------- |
| (None yet) | -        | -   | -        |

---

**Last Updated:** March 14, 2026
