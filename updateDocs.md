## Core Thesis

Vibe coding fails not because AI is bad, but because developers provide vague intent, no structure, and no constraints. AI is a translator, not a mind reader. When fundamentals, documentation, and rules are missing, AI guesses—and those guesses compound into broken systems. Vibe coding works only when you supply clarity, locked constraints, and persistent context.

---

---

## Recent Documentation Activity (2026-05-28)

The following documentation and small code updates were applied to keep project artifacts and how-to steps synchronized with recent fixes:

- Added `scripts/validate_kpis.py` to automate KPI vs cleaned-source verification. The validator prefers `state_master_clean.csv.total_redeem_amt` for subsidy totals, filters `datewise` to the scheme launch date (2024-02-13), and tolerates very small application-count diffs.
- Fixed `pending_vendor_selection` calculation in `scripts/02_kpi_calculation.py` (now computed as `applications - vendor_selected`).
- Updated docs to reference the validation step and the small changes: `README.md`, `DATA_CLEANING_GUIDE.md`, `DASHBOARD_STATUS.md`, `BACKEND_STRUCTURE.md`, `VERIFICATION_REPORT.md`, `lessons.md`, `content_change.md`, and `progress.txt`.

## Recent Documentation Activity (2026-05-28 - Bottleneck refinement)

- Reworked the Bottleneck Analysis time controls so the throughput chart and backlog chart each have their own date range selector.
- Added a focused state multiselect on the Bottleneck state ranking table so users can compare states like Chandigarh, Uttar Pradesh, and Nagaland directly.
- Removed the page-wide bottleneck date selector so the controls sit closer to the charts they affect.

## Recent Dashboard Activity (2026-05-28)

- Added a state comparison chart toggle in `dashboard/streamlit_app.py` so users can switch between grouped bars and a scatter plot of volume vs conversion.
- Added `dashboard.utils.charts.create_state_scatter_chart()` to visualize state volume, conversion, and subsidy size in one view.
- Updated dashboard docs and status notes after the Batch 2 change.

## Recent Dashboard Activity (2026-05-28 - Funnel Update)

- Replaced the Overview funnel with a date-filtered funnel driven by `datewise_clean.csv`.
- Kept the funnel date selector separate from the Overview snapshot so KPI cards stay cumulative.
- Added a note that the daily-grain funnel only includes stages that are present in `datewise_clean.csv`.

## Recent Dashboard Activity (2026-05-28 - Trend Heatmap)

- Added a weekly seasonality heatmap to the Trends page so weekday and week-level traffic patterns are easier to inspect.
- Kept the heatmap scoped to `datewise_clean.csv` daily application counts and the selected date range.

## Recent Dashboard Activity (Batch 3)

- Moved the State Analysis chart toggle next to the graph so the chart mode control sits with the visual it affects.
- Added paginated/top-N district table controls in `dashboard/streamlit_app.py` with rank-by, top/bottom view, rows-per-page, and CSV export.
- Kept the district table focused on the currently selected state while allowing the filtered dataset to be downloaded for offline review.

## Recent Dashboard Activity (Batch 4)

- Added a bucketed system-size distribution chart on Capacity Metrics using the available `upto_10_kw` and `above_10_kw` counts.
- Added a median size band label so the page surfaces the bucket containing the midpoint of system-size counts.
- Kept the wording explicit that the distribution is bucketed because the cleaned data does not expose per-installation system-size bins.

## Recent Dashboard Activity (Batch 5)

- Added reusable chart captions and helper tooltips to improve chart clarity across the dashboard.
- Updated the bottleneck analysis page with source notes for stage drop-off, backlog, state ranking, and approval-gap charts.
- Kept the control text close to the visuals so users can interpret each chart without guessing.

## Recent Documentation Activity (Batch 6)

- Strengthened `README.md`, `resume_present.md`, and `PROJECT_COMPLETION_SUMMARY.md` with resume-ready impact statements.
- Kept the wording focused on scale, validation, and dashboard outcomes so the project reads well in hiring contexts.
- Matched the portfolio summary to the current implemented dashboard features and verified metrics.

## Recent UI Cleanup (2026-05-28)

- Collapsed the sidebar by default to improve the first-view dashboard layout.
- Migrated the dashboard away from deprecated Streamlit width usage.
- Added a validation note on bottleneck approval-rate charts so impossible-looking percentages are interpreted correctly.

## Recent Dashboard + Content Upgrade (2026-05-28)

- Added KPI delta badges on the Overview so the headline numbers show direction as well as scale.
- Added normalized efficiency metrics to the state and district tables so comparisons are less volume-biased.
- Added backlog scenario planning and chart callouts on bottleneck analysis to make the page more decision-oriented.
- Added `docs/metric_glossary.md` and linked it from the README and dashboard About page.

## Recent Documentation Sync (Batch 7)

- Refreshed the project status and supporting docs so future sessions start from the current checkpoint instead of old notes.
- Kept the next actionable step focused on deployment/portfolio packaging rather than re-litigating completed dashboard work.
- Synchronized the README, verification notes, completion summary, lessons, and dashboard status with the latest implemented features.

Instruction: After running cleaning and KPI regeneration, run:

```bash
python scripts/validate_kpis.py
```

Address any reported failures before publishing or demoing artifacts. These additions are committed to `main` for traceability.

## Most Important Ideas

### 1. Documentation Is the Real Product

Code is a downstream artifact. The real foundation is a **documentation-first system** that defines scope, flows, tech, design, data, and execution order before coding begins. Without this, AI hallucinates architecture, UI, and logic.

### 2. Six Canonical Docs Define Everything

A complete project requires six markdown files as immutable sources of truth:

- **PRD.md** – What is being built, for whom, success criteria, scope, and non-goals.
- **APP_FLOW.md** – Pages, routes, navigation paths, success/error states.
- **TECH_STACK.md** – Exact frameworks, tools, and versions.
- **FRONTEND_GUIDELINES.md** – Design system, tokens, responsive rules.
- **BACKEND_STRUCTURE.md** – Database schema, APIs, auth rules.
- **IMPLEMENTATION_PLAN.md** – Step-by-step build order.

These documents cross-reference each other and eliminate ambiguity.

### 3. AI Needs Persistent Memory

AI has no session memory. Two files solve this:

- **CLAUDE.md** – Global rules, constraints, patterns, forbidden actions.
- **progress.txt** – What’s done, in progress, next, and broken.

Together, they prevent context loss and repeated mistakes.

### 4. Interrogation Before Building

Before documentation, AI must aggressively question the idea to expose assumptions. Clear answers become raw inputs for the canonical docs. Clarity ends hallucinations.

### 5. Fundamentals Matter More Than Prompts

Key concepts you must understand to communicate with AI:

- Components
- Layout
- State
- Styling and design tokens
- Responsive design
- Pages vs routes
- Frontend vs backend
- APIs, databases, authentication

Prompt quality depends on conceptual understanding, not clever wording.

### 6. UI ≠ UX

- **UI**: visual appearance.
- **UX**: usability and flow.
  AI must be told explicitly which one to improve. Visual references (screenshots) outperform verbal descriptions.

### 7. Consistency Comes From Locked Rules

Design tokens, component patterns, folder structure, and dependency versions must be fixed in documentation. Consistency collapses if AI is allowed to improvise.

### 8. Tooling Is Phase-Specific

Different tools excel at different stages:

- **Claude**: thinking, interrogation, documentation.
- **Cursor (Ask → Plan → Agent → Debug)**: implementation workflow.
- **Kimi K2.5**: pixel-accurate frontend from visuals.
- **Codex**: debugging, refactoring, stabilization.
- **GitHub + Vercel + Supabase**: version control, deployment, backend.

### 9. Markdown Is a Control Mechanism

Markdown files are not for humans—they are constraints for AI. More markdown = less guessing = fewer failures.

---

## High-Level Summary

The document presents a complete operating system for AI-assisted software development. It argues that “vibe coding” fails when developers skip fundamentals and documentation, forcing AI to guess. The solution is a rigid, documentation-first workflow where canonical markdown files define product scope, user flows, tech stack, design system, backend schema, and build order. Persistent context files (CLAUDE.md and progress.txt) replace AI memory. Clear conceptual understanding (components, state, layout, UX/UI) enables precise instructions. Proper tool usage by phase and strict version control complete the system. When constraints are explicit, AI stops hallucinating and becomes a reliable builder.

---

## Actionable Steps

### Before Any Coding

1. Run an **AI interrogation** of your idea until no assumptions remain.
2. Answer explicitly: users, core action, data, success/failure states, auth, mobile needs.
3. Generate and manually review the six canonical markdown docs.
4. Lock all docs as the single source of truth.

### Project Setup

5. Create the standard folder structure.
6. Add **CLAUDE.md** with rules, conventions, and references.
7. Create **progress.txt** and update it continuously.
8. Initialize Git and commit documentation first.

### During Development

9. Follow the sequence: **Interrogation → Documentation → Code**.
10. Build only one step at a time from **IMPLEMENTATION_PLAN.md**.
11. Always specify:
    - Components to build
    - Layout rules
    - State changes
    - Routes and pages

12. Reference the relevant markdown file in every AI request.
13. Update **progress.txt** after every completed feature.

### Design & UI

14. Define design tokens (colors, spacing, typography) upfront.
15. Choose 1–2 design styles and document them.
16. Use screenshots as visual references instead of descriptions.
17. Design mobile-first and define breakpoints explicitly.

### Backend & Data

18. Define database schema before writing backend code.
19. Use managed auth (Clerk or Supabase Auth).
20. Never hardcode secrets; use `.env` and environment configs.

### Debugging & Shipping

21. Commit frequently with clear messages.
22. Use Codex or Debug mode for systematic bug fixing.
23. Deploy via GitHub → Vercel.
24. Fix deploy issues using logs, not guesses.

### Continuous Improvement

25. When AI makes a mistake, update **CLAUDE.md** to prevent repetition.
26. Maintain a **lessons.md** file for recurring patterns and fixes.
27. Optionally adopt parallel git worktrees for faster builds once experienced.

---}
