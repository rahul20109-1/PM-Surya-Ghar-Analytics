# Graph review — Program snapshot pages

Date: 2026-05-27
Author: Assistant

This document lists the charts and tables shown on each dashboard page (top-to-bottom), what each visual is intended to communicate, and suggestions on whether a chart/table can be removed or replaced with a more insightful alternative.

---

## 1) Program snapshot (Overview)
Order (top → bottom)
- KPI row (4 cards): `Applications submitted`, `Installations completed`, `Inspections approved`, `Subsidy redeemed amount` (crore)
  - Purpose: Surface headline program scale (volume), execution, and finance in one glance.
  - Suggestion: Keep. Consider adding small change deltas (week/month) to show recent direction.

- KPI row (4 cards): `Application → Installation rate`, `Installation → Inspection rate`, `Application → Subsidy rate`, `Applications not yet installed`
  - Purpose: Present core conversion and backlog indicators.
  - Suggestion: Keep. Add short helper text on how each rate is calculated (tooltip or caption) to avoid confusion.

- Trend chart: cumulative/daily applications and installations (`create_adoption_trend`)
  - Purpose: Show program growth and execution over time; reveals intake vs delivery.
  - Suggestion: Keep. Consider allowing toggles for cumulative vs daily on the Overview (currently available on Trends page) — or add small sparklines per KPI for quick context.

- Conversion funnel (funnel chart for stages captured)
  - Purpose: Show stage-by-stage drop-off and cumulative % reaching each stage.
  - Suggestion: Keep. Consider adding a small numeric table below (already present in Bottleneck page) or a per-stage rate column. Optionally replace with a Sankey if there is data that shows multiple branch flows.

Can anything be removed/replaced?
- No immediate removals recommended — all visuals provide distinct, high-level signals. For tighter dashboards, consider converting the large trend chart into a smaller sparkline and keeping a detailed Trends page for full exploration.

---

## 2) State comparison (State Analysis)
Order
- Page header + description + filters (rank-by, top-N)
- Table: Top N states with columns `State`, `Applications submitted`, `Installations completed`, `Application → Installation (%)`
  - Purpose: A sortable list to prioritise states for further investigation.
  - Suggestion: Keep. Improve by adding `Installations per 1,000 applications` (normalized) or `Subsidy per installation` to compare financial efficiency. Consider adding a column with a small sparkline of recent trend for each state.

- Chart: Grouped bar chart `Applications and installations by state`
  - Purpose: Visual comparison of volume per state.
  - Suggestion: Replace or augment with stacked bars showing `applications` vs `installations` as absolute numbers and a line for conversion rate (combo chart), or show `installations per 1000 applications` (normalized) to reveal efficiency.

- Chart: Horizontal bar `Application → Installation rate by state`
  - Purpose: Rank states by conversion rate.
  - Suggestion: Keep. Consider adding conditional color thresholds (e.g., <20% red) and a target line representing national average.

Can anything be removed/replaced?
- The grouped bar and the horizontal conversion bar are complementary; if you must remove one, keep conversion rate and replace the grouped bar with a normalized measure (conversion per 1,000 applications) that highlights efficiency.

---

## 3) District comparison (District Analysis)
Order
- Filters: State select
- Summary metrics: `Applications submitted`, `Installations completed`, `Application → Installation rate`
  - Purpose: Quick state-level summary before district list.

- District-level table showing columns: `State`, `District`, `Applications submitted`, `Installations completed`, `Inspections approved`, `Subsidy redeemed`
  - Purpose: Full drilldown for operational teams to find districts with problems.
  - Suggestion: Keep but improve usability: add sorting, conditional formatting (highlight low conversion), and an inline `Details` link or small sparkline column. Consider showing only Top/Bottom N by default with an option to expand.

Can anything be removed/replaced?
- The raw full table is useful but heavy. Replace full table with a paginated or top-N view plus an `Export CSV` button for operational workflows.

---

## 4) Trends (Trend over time)
Order
- Chart type selector (`Cumulative` / `Daily`)
- Cumulative chart: cumulative applications and installations over time
- Daily chart: daily applications and installations (area lines)

Purpose
- Show program trajectory and recent momentum; identify dates with spikes or declines.

Suggestions
- Keep both views. Add a 7-day rolling average overlay for daily view to smooth noise. Allow selection of date range.
- Add annotations for major program events or policy changes (if known) to contextualize spikes.

---

## 5) Capacity and system size (Capacity Metrics)
Order
- KPI row: Installed capacity (kW), Average system size (kW), Installations completed
- Pie chart: Residential vs RWA share
- Bar chart: System size counts (Up to 10 kW vs Above 10 kW)

Purpose
- Show technical capacity distribution and main segment split.

Suggestions
- Keep. Consider adding median system size and a histogram of system sizes (small bins) to show distribution rather than just two buckets. For RWA vs Residential, add absolute counts alongside percentages.

---

## 6) Bottleneck Analysis (dashboard/pages/08_bottleneck_analysis.py)
Order (top → bottom)
- Title + explanatory text + data note
- Section 1: Stage-by-stage drop-off
  - KPI metrics row: Applications submitted, Reached final stage, Still in process, Largest drop-off stage
  - Table: Stage breakdown (counts, loss counts)
  - Funnel chart: Stage flow
  - Drop-off bar chart: Drop-off % by stage
  - Insight box: Key finding and suggested next step

- Section 2: Pending applications analysis
  - KPI metrics row: Total applications currently waiting, Stage with the most pending applications, Largest waiting share
  - Bar charts: Applications waiting by stage, Waiting share by stage

- Section 3: State comparison (geographic bottleneck analysis)
  - Table: Top N states by selected issue (Applications, Installations, Subsidy, metric)
  - Chart: Applications and installations by state (grouped bars)
  - Chart: Application → Installation rate by state (horizontal)

- Section 4: Time-based bottleneck analysis
  - Chart: 7-day average applications and installations (lines)
  - Chart: Backlog growth over time (cumulative gap)
  - Insight box: throughput metrics and estimated backlog clearance time

- Section 5: Approval rate anomalies
  - Chart: States with lower feasibility approval rates (horizontal bar)
  - Chart: States with lower inspection approval rates (horizontal bar)

- Section 6: Recommended actions (text cards)
- Executive summary (bulleted)

Purpose
- Diagnose where the process is losing volume, where applications pile up, which states are hotspots, and how throughput and backlog evolve over time. Provide prioritized, actionable recommendations.

Suggestions — what to remove or replace
- Keep most visuals — this page is intentionally diagnostic and detailed.
- Consider replacing the grouped state bars in Section 3 with a scatter plot where x=applications (volume), y=conversion rate, size=subsidy_redeemed — this reveals states that are high-volume and low-conversion at a glance.
- For the funnel, add per-stage conversion rates and a small table showing absolute loss and percent loss next to the funnel (if not already visible). Sankey is only useful if there are branching paths; otherwise funnel is fine.
- For approval rate anomalies, add a small table showing absolute counts behind the percentages (so users know whether low % is driven by small sample size).
- For backlog projection (estimated years to clear), guard against division by zero and surface the assumptions (e.g., "Assumes daily inflow equals recent 7-day average"). Consider replacing the single-year estimate with a small scenario table (current pace, +25% capacity, -25% intake).

---

## Final recommendations (global)
- Add consistent helper tooltips on each chart explaining the metric and the source column (e.g., "Applications submitted = state_master.application_status sum").
- Use consistent terminology: use `Applications submitted` across charts, tables, and docs. (Already standardized.)
- Convert large raw tables into paginated/top-N views with an `Export CSV` option for operational use.
- Add normalization options (per-application rates, installations per 1,000 applications) to reveal efficiency differences rather than only volumes.

---

End of review
