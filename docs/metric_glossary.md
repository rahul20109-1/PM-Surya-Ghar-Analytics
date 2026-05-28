# Metric Glossary

This file defines the main KPI terms used in the PM Surya Ghar Analytics dashboard.

## Core Program Metrics

| Metric | Definition | Source / Formula |
| --- | --- | --- |
| Applications submitted | Total number of applications recorded in the cleaned dataset. | `sum(application_status)` |
| Installations completed | Total number of completed installations. | `sum(installation)` |
| Inspections approved | Total number of installations that passed inspection. | `sum(inspection_approved)` |
| Subsidy redeemed amount | Total subsidy value redeemed by the program. | `sum(total_redeem)` or canonical subsidy field in `state_master_clean.csv` when validating |
| Application to installation rate | Share of submitted applications that reached installation. | `installations / applications * 100` |
| Installation to inspection rate | Share of installations that passed inspection. | `inspection_approved / installation * 100` |
| Application to subsidy rate | Share of submitted applications that reached subsidy redemption. | `total_redeem / applications * 100` |
| Applications not yet installed | Submitted applications that have not become installations yet. | `applications - installations` |

## Normalized Metrics

| Metric | Definition | Source / Formula |
| --- | --- | --- |
| Installations per 1,000 applications | Size-adjusted delivery rate used to compare states and districts. | `installations / applications * 1000` |
| Subsidy per installation | Average subsidy value per completed installation. | `subsidy_redeemed_amount / installations` |
| Installed capacity (kW) | Total installed solar capacity. | `sum(total_capacity_installed_kw)` |
| Average system size (kW) | Mean system size across installations. | `total_capacity_installed_kw / total_installations` |

## Bottleneck Metrics

| Metric | Definition | Source / Formula |
| --- | --- | --- |
| Stage drop-off % | Percent lost between one journey stage and the next. | `(previous_stage - current_stage) / previous_stage * 100` |
| Pending applications | Applications waiting between stages. | `previous_stage - current_stage` |
| Backlog growth | Daily growth in the applications minus installations gap. | `avg_daily_applications - avg_daily_installations` |
| Years to clear backlog | Estimated time to clear the backlog at the current pace. | `current_backlog / backlog_growth / 365` |

## Notes

- Values are based on cleaned CSV outputs in `data_cleaned/`.
- Ratios are shown as percentages unless otherwise stated.
- Normalized metrics are meant for comparison across states, districts, and time windows where raw counts alone are misleading.
