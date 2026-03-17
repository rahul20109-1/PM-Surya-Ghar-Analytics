# Frontend Guidelines

## PM Surya Ghar Analytics - Dashboard Design Standards

Last Updated: March 17, 2026

## 1. Design Goals

- Communicate key insights quickly
- Preserve metric accuracy and comparability
- Keep visual language consistent across pages
- Support analyst and non-technical stakeholder interpretation

## 2. Visual System

Primary palette:
- Primary: #1f77b4
- Secondary: #ff7f0e
- Positive: #2ca02c
- Alert: #d62728
- Text: #333333
- Grid: #e8e8e8

## 3. Charting Standards

### Funnel
- Use for stage progression and drop-off analysis
- Show both absolute values and conversion percentages

### Ranking Bars
- Horizontal orientation for readability
- Descending sort by selected metric

### Trend Lines
- Clear date axis and labeled values
- Limited concurrent series to avoid clutter

### Distribution Views
- Use donut or bar charts depending on category count
- Avoid over-segmentation in pie-style visuals

## 4. KPI Card Standards

- Use concise labels and consistent units
- Apply thousand separators for counts
- Use percentage symbols for rates
- Highlight only high-signal indicators

## 5. Interaction Standards

- Filters should be explicit and reversible
- Empty states should display informative guidance
- Tooltip content should include metric definition context when needed

## 6. Accessibility and Readability

- Maintain sufficient text contrast
- Avoid color-only encoding for critical status
- Keep font sizes readable on laptop screens

## 7. Performance Standards

- Data loading must be cached where appropriate
- Visual render should remain responsive during common filter changes
