# CLAUDE.md

# AI Assistant Operating Manual — PM Surya Ghar Analytics Project

**Purpose:** Define how GitHub Copilot and AI agents should work within this project.

This file contains rules, constraints, and workflows that AI assistants (Copilot, other agents) must follow.

---

## 1. Project Context

**Project Type:** Data Analytics Portfolio Project  
**Domain:** Government of India solar rooftop subsidy scheme analysis  
**Language:** Python (3.11)  
**Framework:** Streamlit (for dashboard)  
**Purpose:** Showcase analytics skills for hiring portfolio

---

## 2. Technology Constraints (DO NOT INVENT)

### 2.1 Allowed Libraries

✅ **Data Processing:** pandas (2.0.3), numpy (1.24.3), openpyxl (3.10.x)  
✅ **Visualization:** plotly (5.17.0), matplotlib (3.7.x), seaborn (0.12.x)  
✅ **Dashboard:** streamlit (1.28.1), streamlit-aggrid (0.3.x)  
✅ **Development:** jupyter, jupyterlab, ipython  
✅ **Code Quality:** black, pylint, flake8

### 2.2 NOT Allowed (Do not suggest these)

❌ **PyTorch, TensorFlow** (machine learning excluded from scope)  
❌ **scikit-learn** (predictive modeling out of scope)  
❌ **FastAPI, Flask** (no custom backend needed)  
❌ **SQLAlchemy, psycopg2** (no database, CSV-based analysis)  
❌ **Apache Spark** (overkill for this data volume)  
❌ **Docker, Kubernetes** (not needed for portfolio)

If AI assistant suggests an unlisted library, STOP and reference TECH_STACK.md.

---

## 3. Project Structure Rules

### 3.1 Folder Hierarchy (DO NOT CHANGE)

```
project_root/
├── raw_data/              (Read-only, git-ignored)
├── data_cleaned/          (Processed data, git-tracked)
├── notebooks/             (Jupyter analysis narratives)
├── scripts/               (Reusable Python modules)
│   ├── utils/
│   ├── 00_data_loader.py
│   ├── 01_data_cleaning.py
│   ├── 02_kpi_calculation.py
│   └── 03_visualization.py
├── dashboard/             (Streamlit app)
│   ├── streamlit_app.py
│   ├── pages/
│   ├── utils/
│   └── config.py
├── visualizations/        (Exported charts)
├── docs/                  (Supporting documentation)
├── PRD.md, APP_FLOW.md, TECH_STACK.md, etc.
├── README.md
└── requirements.txt
```

### 3.2 File Naming Conventions

- **Scripts:** Lowercase, underscore-separated: `01_data_cleaning.py`
- **Notebooks:** Descriptive, numbered: `01_Data_Understanding.ipynb`
- **Visualizations:** `YYYYMMDD_descriptive_name.png`
- **Commits:** Descriptive, past tense: "Completed data cleaning pipeline"

---

## 4. Coding Rules

### 4.1 Data Processing

✅ **DO:** Use pandas for all tabular transformations  
✅ **DO:** Use .copy() when modifying dataframes to avoid SettingWithCopyWarning  
✅ **DO:** Document all data type conversions  
✅ **DO:** Validate data after each transformation

❌ **DON'T:** Use loops when pandas vectorized operations exist  
❌ **DON'T:** Modify raw_data/ files directly  
❌ **DON'T:** Hardcode file paths (use relative paths or config)

### 4.2 Visualization

✅ **DO:** Follow FRONTEND_GUIDELINES.md strictly (colors, fonts, spacing)  
✅ **DO:** Always set title, axis labels, legend  
✅ **DO:** Test charts render in <2 seconds  
✅ **DO:** Make interactive (Plotly) where possible

❌ **DON'T:** Use colors outside approved palette  
❌ **DON'T:** Create clutter (overlapping text, too many subplots)  
❌ **DON'T:** Export static images without high DPI (≥300)

### 4.3 Streamlit Dashboard

✅ **DO:** Use @st.cache_data for data loading (performance)  
✅ **DO:** Create reusable utility functions in `utils/`  
✅ **DO:** Test filter combinations for edge cases  
✅ **DO:** Keep pages <500 lines each (modular)

❌ **DON'T:** Load data fresh on every filter change  
❌ **DON'T:** Use global variables (state management)  
❌ **DON'T:** Hard-code column names (reference config.py)

### 4.4 Documentation in Code

✅ **DO:** Add docstrings to all functions (3-line minimum)  
✅ **DO:** Comment non-obvious logic  
✅ **DO:** Include example usage in docstrings

❌ **DON'T:** Over-comment obvious code  
❌ **DON'T:** Leave TODO comments without resolution

**Example:**

```python
def calculate_conversion_rate(applications, installations):
    """
    Calculate application-to-installation conversion rate.

    Args:
        applications (int): Total application count
        installations (int): Total installation count

    Returns:
        float: Conversion rate as percentage (0-100)

    Example:
        >>> calculate_conversion_rate(1000, 500)
        50.0
    """
    if applications == 0:
        return 0.0
    return (installations / applications) * 100
```

---

## 5. Analytics & KPI Calculation

### 5.1 KPI Validation

✅ **DO:** Spot-check calculations against source data  
✅ **DO:** Validate KPI values are within expected ranges  
✅ **DO:** Document all formulas explicitly  
✅ **DO:** Cross-verify aggregations (national = sum of states)

❌ **DON'T:** Accept KPIs without validation  
❌ **DON'T:** Assume calculations are correct without testing

### 5.2 Metric Definitions

Reference PRD.md for official KPI definitions. All KPIs must:

1. Be defined in PRD.md
2. Have calculation formula documented
3. Be calculated in `scripts/02_kpi_calculation.py`
4. Be validated before use
5. Be displayed consistently across dashboard

---

## 6. AI Workflow (When Using Copilot)

### 6.1 Before Implementing Any Feature

**Step 1: Read Documentation**

```
Read and summarize:
- PRD.md (scope, objectives)
- IMPLEMENTATION_PLAN.md (what step are we on?)
- progress.txt (what's completed?)
- BACKEND_STRUCTURE.md (if data work)
- FRONTEND_GUIDELINES.md (if visualization work)
```

**Step 2: Identify Current Phase**

```
What is the current implementation phase?
What is the next step?
What inputs (data, functions) are required?
What should the output be?
```

**Step 3: Propose Approach**

```
Before coding, outline:
- What will be created
- What dependencies exist
- What validation is needed
- What edge cases to handle
```

**Step 4: Execute**

```
Write code following:
- Coding rules (Section 4)
- Data architecture (BACKEND_STRUCTURE.md)
- Tech stack (TECH_STACK.md)
```

**Step 5: Validate**

```
Test that:
- Code runs without errors
- Outputs match expected results
- Performance meets requirements
- Edge cases handled
```

**Step 6: Document**

```
Update:
- progress.txt (mark step complete)
- lessons.md (document learnings)
- Code comments (if non-obvious)
- Git commit with descriptive message
```

---

## 7. Common Tasks & Workflows

### 7.1 Task: Add a New KPI

1. **Define** it in PRD.md under "KPIs to Generate"
2. **Document** calculation formula in BACKEND_STRUCTURE.md
3. **Implement** function in `scripts/02_kpi_calculation.py`
4. **Validate** with spot-checks against raw data
5. **Test** in notebook (e.g., in `04_KPI_Creation.ipynb`)
6. **Integrate** into dashboard (add to relevant pages)
7. **Update** progress.txt and commit

### 7.2 Task: Add a New Visualization

1. **Decide** chart type (reference FRONTEND_GUIDELINES.md)
2. **Create** function in `scripts/03_visualization.py`
3. **Follow** color palette, fonts, styling rules
4. **Test** chart renders correctly
5. **Export** to `visualizations/` with naming convention
6. **Integrate** into dashboard page
7. **Commit** with message "Added [chart name] visualization"

### 7.3 Task: Create a New Dashboard Page

1. **Decide:** Purpose, filters, components
2. **Reference:** Section 5.2 of IMPLEMENTATION_PLAN.md for page specs
3. **Create:** File in `dashboard/pages/NN_name.py`
4. **Implement:**
   - Streamlit page setup
   - Filter widgets (using `utils/filters.py`)
   - Data loading (using `utils/data_loader.py`)
   - Chart rendering (using `utils/charts.py`)
   - KPI cards (using `utils/kpi_calculators.py`)
5. **Test:** All filters, edge cases, performance
6. **Update:** Main `streamlit_app.py` to add page to sidebar
7. **Commit:** "Added [page name] dashboard page"

---

## 8. Error Handling & Debugging

### 8.1 When an Error Occurs

**Step 1: Identify Context**

- Which phase/step is failing?
- What is the error message?
- What data/input caused it?

**Step 2: Review Code**

- Is it following coding rules?
- Are dependencies imported correctly?
- Are edge cases handled?

**Step 3: Validate Input Data**

- Are input files present?
- Are data types correct?
- Are numerics parsed correctly (Indian format)?

**Step 4: Debug with Spots-Checks**

- Print sample data
- Verify intermediate calculations
- Check for NaN or inf values

**Step 5: Fix & Test**

- Implement fix
- Test with sample data
- Run full workflow
- Commit fix with explanation

### 8.2 Common Issues & Fixes

**Issue:** `ValueError: No columns to parse from file`  
**Cause:** File path incorrect or file missing  
**Fix:** Verify file exists, check relative path from working directory

**Issue:** `TypeError: unsupported operand type(s) for +: 'str' and 'int'`  
**Cause:** Numeric string not parsed (commas still present)  
**Fix:** Use parser from `scripts/utils/parser.py` before arithmetic

**Issue:** Streamlit app hangs on filter change  
**Cause:** Data being reloaded without caching  
**Fix:** Add `@st.cache_data` to data loading function

---

## 9. Progress Tracking

### 9.1 Updating progress.txt

After completing each phase/step:

```
COMPLETED
- [Step name] — Brief description

IN PROGRESS
- [Current step] — Current status

NEXT
- [Next step] — What comes after

BLOCKERS
- [If any] — Known issues
```

### 9.2 Updating lessons.md

Document:

- What was learned
- What would be done differently
- What took longer than expected
- What went smoothly

---

## 10. Git Workflow

### 10.1 Commit Messages

**Format:** `[Phase] [Task]: Brief description`

**Examples:**

- `Phase 2: Complete data cleaning pipeline`
- `Phase 5: Add state analysis dashboard page`
- `Phase 4: Fix applicaton funnel calculation`
- `Phase 7: Update README with findings`

### 10.2 Frequency

- Commit after completing each step (at minimum)
- Commit after fixing bugs
- Never commit broken code

---

## 11. Decision Log

When making architectural or design decisions, document:

1. **Decision:** What choice was made?
2. **Rationale:** Why was this chosen?
3. **Alternatives:** What other options existed?
4. **Trade-offs:** What was gained/lost?
5. **Reversibility:** How hard would it be to undo?

Example:

```
Decision: Use Streamlit instead of custom Flask app
Rationale: Faster to development, free deployment on Streamlit Cloud
Alternatives: Flask (more control, slower to build), Dash (more complex)
Trade-offs: Less customization, but faster to market
Reversibility: High (can migrate to Flask later if needed)
```

---

## 12. Reference Quick Links

When implementing any feature, reference:

- **Project Goals:** PRD.md (Section 2, 4, 5)
- **Data Schema:** BACKEND_STRUCTURE.md (Section 1-5)
- **UI/UX Rules:** FRONTEND_GUIDELINES.md (Section 2-8)
- **Implementation Steps:** IMPLEMENTATION_PLAN.md (Phase X, Step Y.Z)
- **Tech Choices:** TECH_STACK.md (Section 1-11)
- **Current Status:** progress.txt (updated after each step)

---

## 13. When to Break These Rules

Rules are made to be followed, but exceptions exist:

✅ **Exception:** Use a different library if PRD/TECH_STACK conflicts with reality

- **Condition:** Must document decision in lessons.md
- **Condition:** Must update TECH_STACK.md with new library

✅ **Exception:** Take a shortcut if deadline requires it

- **Condition:** Document in lessons.md as "Technical Debt"
- **Condition:** Note when/how to pay back the debt

✅ **Exception:** Deviate from folder structure if it makes sense

- **Condition:** Update this CLAUDE.md with new structure
- **Condition:** Update IMPLEMENTATION_PLAN.md accordingly

❌ **Exception:** Modify raw_data files

- **No conditions:** Never do this
- **Always:** Work on copies in data_cleaned/

---

## 14. Sign-Off

By following this manual:
✅ Code will be consistent and maintainable  
✅ Project will align with documented goals  
✅ Portfolio will showcase professional practices  
✅ Future developers (or hiring managers) can understand decisions

---

**Document Owner:** Analytics Project Lead  
**Last Updated:** March 14, 2026  
**Next Review:** After Phase 1 completion
