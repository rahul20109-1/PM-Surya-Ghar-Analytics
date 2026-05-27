# Content changes made (summary)

Date: 2026-05-27
Author: GitHub Copilot (assistant)

This document lists all content (UI copy, chart titles/labels, table headings, captions, and insight/summary text) changes made in the repository during the current work session.

---

1. dashboard/streamlit_app.py

- Improved the main sub-header to: "Clear, unambiguous view of program scale, progress, and operational bottlenecks".
- Rewrote Overview intro paragraph to explain purpose and how to read KPIs.
- Formatted `Subsidy redeemed amount` to display in `crore` and updated label to `Subsidy redeemed amount` (formatted value suffix).
- Replaced the State table with a clear, unambiguous table and column headings:
  - `State`, `Applications submitted`, `Installations completed`, `Application → Installation (%)` with formatted numbers and percent strings.
- Improved captions and funnel explanatory text to clarify which journey steps are captured.
- Edited several small headings and captions for clarity and recruiter-friendly language.

2. dashboard/pages/08_bottleneck_analysis.py

- Rewrote page title and description to: "Process bottlenecks — where applications stall" and added an explanatory paragraph describing how to use the page.
- Replaced the original critical insight wording with a clearer "Key insight" box that includes the stage names, percentage drop, application loss, and a suggested next step.
- Improved metric labels in pending section to:
  - `Total applications currently waiting` (was: "Total waiting applications")
  - `Stage with the most pending applications` (was: "Stage with the most waiting applications")
  - `Largest waiting share` now shows "Share of applications pending at this stage" explanation
- Reworked the State comparison section copy to explain what the table shows, how to prioritise metrics, and tips for drilling down.
- Changed table column names and formatting in the State comparison table for readability (formatted numbers, percent strings).
- Replaced the long summary with an executive-style "Executive summary" outlining priority issue, backlog risk, uneven delivery, approval variability, and recommended next steps.
- Reworded several section headers and captions to be concise and action-oriented.

3. dashboard/utils/charts.py

- Improved chart titles and axis labels across functions:
  - `create_adoption_trend`: title clarified; y-axis labelled "Cumulative applications / installations"; improved hover formatting (dates & thousands separators).
  - `create_state_ranking_chart`: y-axis label now clarifies counts as "Count (number of applications/installations)"; hover templates formatted with thousands separators; legend titled "Metric".
  - `create_conversion_rate_chart`: title changed to "Application → Installation rate by state"; x-axis labelled "Conversion rate (%)"; hover template shows percent with one decimal.
  - `create_district_heatmap`: added hover template and ensured axis label clarity.
- Added hover templates to make values easier to read and to show context (e.g., "12,345 applications — 2026-05-01").

4. dashboard/pages/08_bottleneck_analysis.py (charts & tables tweaks)

- (Content-focused changes retained) Funnel, drop-off, pending, time-series, backlog and approval charts had their titles, axis labels, hover texts and legend titles improved for clarity and recruiter-facing presentation.

Notes / scope

- These edits focused on textual content and presentation (labels, headings, captions, table column names, and chart hover/axis text). They do not change core calculations or data logic.
- All changes committed to `main` branch with descriptive commit messages.

Commits (representative)

- "Phase 5: Improve copy on State Comparison page"
- "Phase 5: Improve copy on State Analysis (Overview) page"
- "Phase 5: Improve chart labels, axis titles, and hover text across charts"
- "Phase 5: Rewrite UI copy and table labels for clearer, recruiter-friendly language"

If you want, I can:

- Add standardized number formatting (crore/lakh) to all tables and chart tick labels.
- Produce a short changelog with exact diff snippets for each edit.
- Run the Streamlit app and capture screenshots of the updated pages.

---

End of content_change.md
