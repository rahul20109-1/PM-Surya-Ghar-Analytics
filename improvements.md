## Progress checklist

Use the check marks to quickly see what's complete and what's pending.

- [x] Shift Overview date selector to sit with the adoption-trend chart (adoption-trend has its own date selector)
- [x] Add date-range selector for the Overview funnel (uses `datewise_clean.csv` daily grain)
- [x] Fix custom date behavior so a single start date defaults end date to dataset max
- [x] State Comparison: fix column headings and add explicit multi-select for targeted comparisons
- [x] Trends: add weekday seasonality curve
- [x] Trends: remove installation-lag proxy distribution (removed 2026-05-28)
- [x] Capacity: bucketed system-size view and median size band (fallback buckets used where per-installation sizes absent)
- [x] Bottleneck Analysis: per-chart date selectors added and approval-rate chart removed
- [x] Colocate backlog scenarios with backlog chart
- [x] Reframe approval-rate wording to "processing ratio (diagnostic hotspot)"
- [x] Add Trends CSV export for filtered time-series
- [ ] Make Overview KPI cards reflect selected date range (DEFERRED — snapshot KPIs remain cumulative by design)
- [ ] Add additional, data-backed Trend visualizations (pending further specification)


---

On program snapshot page, shift the date range option of "Applications and installations over time" near the graph. Currently it is above the cumulative values of the scheme like applications submitted, installations etc. So shift the time selector. Or add a time selector for specifically the cumulative values where the values will change depending upon the time. So like if I select last 30 days, I will see the applications submitted in last 30 days, installations completed in last 30 days etc. The cumulative values of the scheme in the time range we select. Additionally add a time selector for "How applications move through journey stages captured in the data" graph. Also in the custom date selectors, when I add start date, the system throws error till I select last date. We don't want the error. Take a default last date. If user sumbits a last date then ok, otherwise go with the default last date, which is the last date in our data. This applicable on all custome date option.

In State Comparison page, In top states graph, column headings need to be fixed. "Application ÔåÆ Installation (%)" needs to be in english characters. Additionally "Application ÔåÆ Installation (%)" and "Installations per 1,000 applications" are basically the same thing. So keep the % only. And remove "Subsidy per installation (₹)" or suggest other columns that we can add for a state. Also remove source from the graphs. Also come up with the solution if I want to compare specific states performance. Like I want to see performance of Chandigarh, UP and Nagaland only. How can I do that?

In Trend over time page, We have to check if we can add other useful graphs or visualizations.

In Capacity and system size, show number of system size in ranges of system size of 0-1 kw, 1-2 kw... more than 10kw. Also add time filter in this graph.

In bottleneck analysis, remove this "Date range (Bottleneck analysis)" time selector. Add individual time range selector for every graph(if relevant). Fix "Process bottlenecks ÔÇö where applications stall" content. Add states filter if possible and adds value. Remove the Approval rate chart, since all application are auto approved for feasibilty.