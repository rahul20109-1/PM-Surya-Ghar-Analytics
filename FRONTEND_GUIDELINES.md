# Frontend Guidelines (FRONTEND_GUIDELINES.md)

# PM Surya Ghar Analytics — Visualization Design Standards

**Purpose:** Establish consistent visualization design rules for all charts and dashboards.

---

## 1. Visualization Principles

### 1.1 Core Principles

✅ **Clarity:** Every chart should communicate one main insight immediately  
✅ **Accuracy:** Scales, proportions, and numbers must be mathematically correct  
✅ **Consistency:** Colors, fonts, styles remain uniform across all visualizations  
✅ **Interactivity:** Use hover to reveal details, zoom/pan for exploration  
✅ **Accessibility:** Color-blind compatible palettes, readable fonts, sufficient contrast  
✅ **Professional:** Polish and attention to detail signal competence

---

## 2. Color Palette (Locked)

### 2.1 Primary Colors

| Usage            | Hex     | RGB            | Name   |
| ---------------- | ------- | -------------- | ------ |
| Primary accent   | #1f77b4 | (31, 119, 180) | Blue   |
| Secondary accent | #ff7f0e | (255, 127, 14) | Orange |
| Tertiary accent  | #2ca02c | (44, 160, 44)  | Green  |
| Alert/Warning    | #d62728 | (214, 39, 40)  | Red    |

### 2.2 Neutral Colors

| Usage       | Hex     | RGB             | Name        |
| ----------- | ------- | --------------- | ----------- |
| Background  | #ffffff | (255, 255, 255) | White       |
| Grid/Border | #e8e8e8 | (232, 232, 232) | Light Gray  |
| Text        | #333333 | (51, 51, 51)    | Dark Gray   |
| Disabled    | #cccccc | (204, 204, 204) | Medium Gray |

### 2.3 Sequential Palette (for heatmaps, intensity)

```
Low intensity:  #ffffff (white)
                #e8e8e8 (light gray)
                #b3d9ff (light blue)
                #66b3ff (medium blue)
                #1f77b4 (dark blue)
High intensity: #003d66 (very dark blue)
```

### 2.4 Categorical Palette (for segments)

```
Category 1: #1f77b4 (Blue)
Category 2: #ff7f0e (Orange)
Category 3: #2ca02c (Green)
Category 4: #d62728 (Red)
Category 5: #9467bd (Purple)
Category 6: #8c564b (Brown)
```

---

## 3. Chart Types & Specifications

### 3.1 Funnel Charts

**Purpose:** Show progression through pipeline stages  
**When to Use:** Application → Vendor → Feasibility → Installation → Inspection → Subsidy

**Specifications:**

- Vertical orientation (top-to-bottom funnel)
- Width decreases proportionally with stage progression
- Color: Primary blue (#1f77b4) for all sections
- Hover tooltip: Stage name, count, % of total, % of previous stage
- Title: "Adoption Funnel: [Analysis Context]"
- Subtitle: "Total applications: X"

**Example:**

```
Applications: 100
├─ Vendor Selected: 80 (80%)
├─ Feasibility Approved: 70 (87.5% of vendor, 70% of apps)
├─ Installations: 60 (85.7% of feasibility, 60% of apps)
├─ Inspections: 55 (91.7% of install, 55% of apps)
└─ Subsidy Redeemed: 50 (90.9% of inspect, 50% of apps)
```

---

### 3.2 Geographic Heatmaps

**Purpose:** Show adoption rate by state/district  
**When to Use:** State-wise adoption ranking, regional disparities, geographic clusters

**Specifications:**

- State/District boundaries (if map available; else table heatmap)
- Color intensity: Light (low adoption) → Dark (high adoption)
- Sequential palette: White → Light Blue → Blue → Dark Blue
- Hover tooltip: State/District name, adoption metric, value, rank
- Title: "Rooftop Solar Adoption Heatmap: [Metric]"
- Legend: Show scale from 0 to max value

---

### 3.3 Bar Charts (Rankings)

**Purpose:** Compare states, districts, or vendors  
**When to Use:** Top 10 states by installations, top vendors, regional comparisons

**Specifications:**

- Horizontal bars (easier label reading)
- Sorted descending (highest to lowest)
- Color: Primary blue (#1f77b4) for all bars
- Hover tooltip: Category name, exact value, rank
- X-axis label: Metric name and unit ("Installations (Count)")
- Y-axis label: Category type ("State" or "District" or "Vendor")
- Title: "Top 10 [Category] by [Metric]"
- Include value labels on bars (optional if not cluttered)

**Example Row:**

```
Andhra Pradesh | ████████████████████ | 97,371 installations
```

---

### 3.4 Time-Series Line Charts

**Purpose:** Show trends over time  
**When to Use:** Daily application growth, installation pace, adoption acceleration

**Specifications:**

- X-axis: Date (auto-range based on data)
- Y-axis: Metric value (applications, installations, subsidy amount)
- Line color: Primary blue (#1f77b4)
- Markers: Small dots at each data point
- Hover tooltip: Date, exact value, change from previous day
- Title: "[Metric] Trend Over Time"
- Subtitle: "Date range: [Start Date] to [End Date]"
- Grid: Light gray (#e8e8e8) for readability
- Multiple lines (if comparing):
  - Line 1: Blue (#1f77b4)
  - Line 2: Orange (#ff7f0e)
  - Line 3: Green (#2ca02c)
  - Max 3-4 lines per chart (avoid clutter)

---

### 3.5 Pie/Donut Charts

**Purpose:** Show segment breakdown (whole-to-part)  
**When to Use:** Residential vs RWA split, capacity distribution by segment

**Specifications:**

- Segments: Use categorical palette colors
- Segment labels: Category name + percentage
- Hover tooltip: Category name, value, percentage
- Title: "[Category] Distribution"
- Donut format (center hole) preferred for visual relief
- Legend: Outside the chart, not overlapping
- Max 5 segments (more segments → bar chart instead)

---

### 3.6 Waterfall Charts

**Purpose:** Show how values combine to reach total  
**When to Use:** Bottleneck analysis (applications → pending → approved), subsidy pipeline stages

**Specifications:**

- Vertical waterfall orientation
- Starting value: First stage (applications)
- Intermediate stages: Blue bars (for flow progression)
- Negative values: Red (#d62728) if applicable (rejections)
- Ending total: Darker blue
- Hover tooltip: Stage name, value, cumulative total
- Title: "Subsidy Pipeline Waterfall: [Analysis Context]"

---

### 3.7 Scatter Plots

**Purpose:** Correlation analysis (future use)  
**When to Use:** Adoption vs population, vendor performance vs district size

**Specifications:**

- X-axis, Y-axis: Two metrics
- Points: Primary blue (#1f77b4), size proportional to value
- Hover tooltip: Labels for both axes + third metric (category)
- Trend line: Optional (if correlation exists)
- Title: "[Metric 1] vs [Metric 2]"

---

## 4. Chart Styling Rules

### 4.1 Typography

- **Font Family:** System default (Arial, Helvetica, sans-serif)
- **Title Font Size:** 16-18px, bold, dark gray (#333333)
- **Subtitle Font Size:** 12-14px, regular, medium gray (#666666)
- **Axis Labels:** 11-12px, regular, dark gray (#333333)
- **Hover Tooltip:** 11-12px, regular, on dark background
- **Legend:** 10-12px, regular, dark gray

### 4.2 Axis & Scale

- **Number Formatting:** Use thousand separators (1,000 not 1000)
- **Currency Formatting:** Rupees (₹) with thousands separator (₹10,00,000)
- **Percentage Formatting:** 0-100%, no decimals unless significant
- **Date Formatting:** DD-MM-YYYY format for "rptdate"
- **Scale Type:** Linear (not log) unless data spans huge range

### 4.3 Gridlines & Borders

- **Horizontal Gridlines:** Light gray (#e8e8e8), 1px, optional for readability
- **Vertical Gridlines:** Usually off (clutter)
- **Chart Border:** None (cleaner look)
- **Facet Borders:** Light gray (#e8e8e8), 1px between subplots

### 4.4 Spacing & Margins

- **Chart Margin:** 40px top, 30px bottom, 60px left, 20px right
- **Legend Margin:** 10px from chart edge
- **Hover Tooltip Margin:** 5px from cursor
- **Between Subplots:** 20px horizontal, 30px vertical

---

## 5. Dashboard Layout Rules (Streamlit)

### 5.1 Page Structure

```
┌─────────────────────────────────────────┐
│  Page Title & Description               │
├─────────────────────────────────────────┤
│  Filter Row (State, Date, Metrics, etc.)│
├─────────────────────────────────────────┤
│                                         │
│  Main Visualization (Full Width)        │
│                                         │
├─────────────────────────────────────────┤
│  Metric Cards (KPI Summary)             │
├─────────────────────────────────────────┤
│  Secondary Charts (2 or 3 per row)      │
│                                         │
├─────────────────────────────────────────┤
│  Detailed Data Table (if exploration)   │
│                                         │
└─────────────────────────────────────────┘
```

### 5.2 Metric Card Design

**For KPI Summary Cards:**

```
┌──────────────────┐
│ Metric Label     │
│                  │
│   999,999        │  ← Large bold value
│                  │
│ +5.2% vs prev    │  ← Trend indicator
└──────────────────┘
```

- Background: Light gray (#f2f2f2) or white
- Value: 24-28px font, bold
- Label: 12px, medium gray
- Trend: 11px, green (#2ca02c) if positive, red (#d62728) if negative

### 5.3 Column Layout

- **Full Width:** Main funnel, main heatmap (takes entire dashboard width)
- **Two Columns:** Secondary insights, side-by-side comparisons
- **Three Columns:** Metric cards, small multiples
- **Responsive:** Stack to single column on mobile

---

## 6. Labeling Standards

### 6.1 Chart Titles

**Format:** "[Noun] Analysis: [Context]" or "[Metric] by [Dimension]"

**Examples:**

- ✅ "Adoption Funnel: State-Level Conversion"
- ✅ "Top 10 States by Installation Count"
- ✅ "Subsidy Pipeline Bottleneck Analysis"
- ❌ "Chart 1" (vague)
- ❌ "Data Visualization" (non-descriptive)

### 6.2 Axis Labels

**Format:** "[Metric Name] ([Unit])"

**Examples:**

- ✅ "Applications (Count)"
- ✅ "Subsidy Amount (₹ Crores)"
- ✅ "Date (DD-MM-YYYY)"
- ❌ "Values"
- ❌ "Axis X"

### 6.3 Hover Tooltip Format

**Format:** Show label + value + context

**Example:**

```
State: Andhra Pradesh
Applications: 1,324,472
Installations: 97,371
Conversion Rate: 7.35%
```

---

## 7. File Naming Conventions

### 7.1 Visualization Exports

**Format:** `YYYYMMDD_descriptive_name.png`

**Examples:**

- `20260314_adoption_funnel_state.png`
- `20260314_top10_states_installations.png`
- `20260314_subsidy_pipeline_waterfall.png`
- `20260314_state_heatmap_adoption_rate.png`

### 7.2 Chart Data Files

**Format:** `[chart_type]_[dimension]_[metric].csv`

**Examples:**

- `funnel_state_conversions.csv`
- `barchart_state_installations.csv`
- `timeseries_daily_application_growth.csv`

---

## 8. Grid & Responsive Design

### 8.1 Streamlit Grid System

- **Full Width:** `st.columns(1)` or default full
- **Two Columns:** `col1, col2 = st.columns(2)`
- **Three Columns:** `col1, col2, col3 = st.columns(3)`
- **Ratio Columns:** `col1, col2 = st.columns([2, 1])` (2:1 split)

### 8.2 Responsive Behavior

- Charts scale automatically with container width
- On mobile: Single column layout
- Avoid fixed pixel widths (use proportional)

---

## 9. Accessibility

### 9.1 Color-Blind Compatibility

- Test color palette with tools like Color Oracle
- Primary colors: Blue (#1f77b4) and Orange (#ff7f0e) are distinguishable for deuteranopia/protanopia
- Add patterns/textures for additional distinction (optional)

### 9.2 Contrast

- Text on background: Minimum 4.5:1 contrast ratio
- Dark text (#333333) on white (#ffffff): ✅ 12:1 (excellent)
- Light text on blue background: Test and adjust

### 9.3 Font & Size

- Minimum font size: 11px (readable without zoom)
- Labels: Clear, no abbreviations unless explained
- Tooltips: Appear on hover, no essential info hidden

---

## 10. Interaction & Interactivity

### 10.1 Hover Behavior

- Hover tooltip appears within 200ms
- Shows all relevant metrics
- Cursor changes to pointer on clickable elements

### 10.2 Click Actions

- Filter updates: <500ms response time
- Chart re-render: Plotly handles auto-smoothing
- No full page reload (slow)

### 10.3 Zoom & Pan

- Plotly default zoom (box select or wheel)
- Pan with drag enabled
- Double-click to reset zoom

---

## 11. Quality Checklist

Before publishing any visualization:

- [ ] Chart has clear, descriptive title
- [ ] All axes labeled with units
- [ ] Colors match approved palette
- [ ] No overlapping text or labels
- [ ] Tooltip shows all relevant metrics
- [ ] Numbers formatted correctly (thousands, currency, %)
- [ ] Legend is present and clear (if multiple categories)
- [ ] Chart renders in <2 seconds
- [ ] Looks professional and cohesive
- [ ] Tested on both desktop and mobile
- [ ] Color-blind tested (if using multi-color)

---

## 12. Library-Specific Rules

### 12.1 Plotly

- Always set `title`, `xaxis.title`, `yaxis.title`
- Use `hovertemplate` for custom tooltips
- Set `showlegend=True` for categorical data
- Use `height=500` for consistency

### 12.2 Matplotlib/Seaborn

- Use `plt.title()`, `plt.xlabel()`, `plt.ylabel()`
- Set style: `seaborn.set_style("whitegrid")`
- Tight layout: `plt.tight_layout()` before save
- DPI for export: `dpi=300` for high quality

---

**Document Owner:** Analytics Project Lead  
**Last Updated:** March 14, 2026
