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
