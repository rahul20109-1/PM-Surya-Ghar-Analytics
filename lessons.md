# Lessons and Decisions Log

## PM Surya Ghar Analytics

Last Updated: March 17, 2026

## 1. Architectural Decisions

### Decision: Streamlit for Delivery Layer
Rationale:
- Fast path from analysis to interactive product
- Strong fit for Python-first analytics workflow
- Effective for portfolio demonstration without backend complexity

Trade-off:
- Less UI flexibility compared to custom frontend frameworks

### Decision: CSV-First Data Stack
Rationale:
- Suitable for project scope and reproducibility
- Simplifies setup for reviewers and interviewers

Trade-off:
- Not optimized for high-concurrency production workloads

### Decision: Modular Script Separation
Rationale:
- Cleaner maintainability and testability
- Easier review during hiring conversations

Trade-off:
- Slightly higher initial structure overhead

## 2. Execution Learnings

- Silent parsing defects can invalidate entire KPI narratives.
- Artifact-based validation prevents stale claims in documentation.
- Documentation quality materially affects portfolio credibility.
- A clear source-of-truth hierarchy is essential for consistency.

## 3. Process Improvements Applied

- KPI export designated as canonical reporting source.
- Documentation rewritten to reflect current repository facts.
- Legacy progress narrative replaced with concise portfolio communication.

## 4. Recent Fixes (2026-05-28)

- Added `scripts/validate_kpis.py` — automated validation comparing `kpis_national.csv` to cleaned artifacts.
- Fixed `pending_vendor_selection` calculation in `scripts/02_kpi_calculation.py` (was incorrectly subtracting sums from themselves).
- Validation logic updated to prefer `state_master_clean.csv.total_redeem_amt` for subsidy totals to avoid cross-source unit mismatches.

## 5. Recent Dashboard and Docs Learnings (2026-05-28)

- KPI deltas are most useful when they compare the selected window against the immediately preceding window of the same length.
- Normalized metrics like installations per 1,000 applications make state comparisons less misleading than raw counts alone.
- Bottleneck pages need explicit caveats when the source grain can produce approval rates above 100%.
- A metric glossary is worth keeping in the repository because it reduces repeated explanation work during interviews.
- Status docs should be updated after each batch so the next session can resume without re-reading the full history.
