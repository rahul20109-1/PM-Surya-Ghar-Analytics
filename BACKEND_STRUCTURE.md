# Backend Structure (BACKEND_STRUCTURE.md)

# PM Surya Ghar Analytics — Data Architecture & Schemas

**Purpose:** Define all datasets, their schemas, transformations, and relationships.

---

## 1. Raw Datasets Inventory

### 1.1 datewise.csv

**Purpose:** Daily aggregated program metrics (time-series)

| Column          | Type | Description                          | Example    |
| --------------- | ---- | ------------------------------------ | ---------- |
| rptdate         | date | Report date (DD-MM-YYYY)             | 09-02-2026 |
| applications    | int  | Total applications received          | 6          |
| residential     | int  | Residential category applications    | 1          |
| rwa             | int  | RWA category applications            | 0          |
| totalhouseholds | int  | Total households (RWA segment)       | 0          |
| upto_10_kw      | int  | ≤10 kW capacity segment applications | 1          |
| above_10_kw     | int  | >10 kW capacity segment applications | 0          |
| installations   | int  | Total installations completed        | 1          |
| inspection      | int  | Inspections approved                 | 37         |
| subsidyredeemed | int  | Subsidy redempted count              | 6          |

**Hierarchies:** Temporal (one row per day)  
**Date Range:** 2026-02-01 to 2026-02-09  
**Row Count:** ~300 rows (daily data)  
**Quality Issues:** Trailing empty columns, comma-formatted numbers

---

### 1.2 state_master.csv

**Purpose:** State-level aggregated summary with capacity metrics

| Column                                      | Type   | Description                            |
| ------------------------------------------- | ------ | -------------------------------------- |
| state                                       | string | State name (full)                      |
| application_status                          | int    | Total applications                     |
| vendor_selected                             | int    | Applications with vendor assigned      |
| vendor_selection_pending_gt_180_days        | int    | Vendor selection delayed >180 days     |
| feasibility_approved                        | int    | Applications with feasibility approved |
| feasibility_approved_capacity               | float  | Capacity (kW) approved for feasibility |
| feasibility_rejected                        | int    | Feasibility rejections                 |
| feasibility_pending                         | int    | Pending feasibility review             |
| residential_installation                    | int    | Residential installations              |
| residential_capacity                        | float  | Residential capacity (kW)              |
| rwa_installation                            | int    | RWA installations                      |
| rwa_capacity                                | float  | RWA capacity (kW)                      |
| no_of_houses                                | int    | Total houses in RWA installations      |
| upto_10_kw                                  | int    | ≤10 kW segment count                   |
| above_10_kw                                 | int    | >10 kW segment count                   |
| installation                                | int    | Total installations                    |
| loan_disbursed                              | int    | Loan disbursement count                |
| installed_capacity                          | float  | Total installed capacity (kW)          |
| inspection_approved                         | int    | Inspections approved                   |
| inspection_approved_capacity                | float  | Inspected capacity (kW)                |
| inspection_rejected                         | int    | Inspections rejected                   |
| inspection_pending                          | int    | Pending inspections                    |
| total_redeem                                | int    | Subsidy redemptions                    |
| total_redeem_amt                            | float  | Total subsidy redeemed (₹)             |
| total_released                              | int    | Subsidy released count                 |
| total_released_amt                          | float  | Total subsidy released (₹)             |
| active_vendors                              | int    | Active vendor count                    |
| no_of_vendors                               | int    | Total vendors                          |
| Applications Submitted for Loan             | int    | Loan applications                      |
| Applications where Loan Sanction is Pending | int    | Pending loan sanctions                 |
| Applications in which Loan is sanctioned    | int    | Sanctioned loans                       |
| Applications where Loan is Disbursed        | int    | Disbursed loans                        |
| Applications where Loan is rejected         | int    | Rejected loans                         |

**Hierarchies:** State level (one row per state)  
**Row Count:** 36 rows (states + UTs)  
**Quality Issues:** Numeric with commas, trailing columns, many financial metrics

---

### 1.3 district.csv

**Purpose:** Most granular geographic breakdown (State × District)

| Column                                      | Type   | Description            |
| ------------------------------------------- | ------ | ---------------------- |
| state                                       | string | State name             |
| district                                    | string | District name          |
| application_status                          | int    | Total applications     |
| vendor_selected                             | int    | Vendor assignments     |
| vendor_selection_pending_gt_180_days        | int    | >180 day delays        |
| feasibility_approved                        | int    | Feasibility approvals  |
| feasibility_rejected                        | int    | Feasibility rejections |
| feasibility_pending                         | int    | Pending feasibility    |
| residential_installation                    | int    | Residential installs   |
| rwa_installation                            | int    | RWA installs           |
| no_of_houses                                | int    | Houses in RWA          |
| upto_10_kw                                  | int    | ≤10 kW count           |
| above_10_kw                                 | int    | >10 kW count           |
| installation                                | int    | Total installations    |
| installation_against_loan                   | int    | Installs with loan     |
| inspection_approved                         | int    | Inspections approved   |
| inspection_rejected                         | int    | Inspections rejected   |
| inspection_pending                          | int    | Pending inspections    |
| total_redeem                                | int    | Subsidy redemptions    |
| total_redeem_amt                            | float  | Redeemed amount (₹)    |
| total_released                              | int    | Released count         |
| total_released_amt                          | float  | Released amount (₹)    |
| Applications Submitted for Loan             | int    | Loan applications      |
| Applications where Loan Sanction is Pending | int    | Pending sanctions      |
| Applications in which Loan is sanctioned    | int    | Sanctioned             |
| Applications where Loan is Disbursed        | int    | Disbursed              |
| Applications where Loan is rejected         | int    | Rejected loans         |
| active_vendor                               | int    | Active vendors         |

**Hierarchies:** State × District combination  
**Row Count:** ~700+ rows  
**Join Key:** state + district → unique identifier  
**Quality Issues:** Numeric commas, many columns

---

### 1.4 discom_master.csv

**Purpose:** Electricity Distribution Company (DISCOM) level metrics

| Column                                      | Type   | Description           |
| ------------------------------------------- | ------ | --------------------- |
| state                                       | string | State name            |
| discom                                      | string | DISCOM name           |
| application_status                          | int    | Applications          |
| vendor_selected                             | int    | Vendor selections     |
| feasibility_approved                        | int    | Feasibility approvals |
| feasibility_rejected                        | int    | Rejections            |
| feasibility_pending                         | int    | Pending               |
| residential_installation                    | int    | Residential installs  |
| rwa_installation                            | int    | RWA installs          |
| no_of_houses                                | int    | Houses                |
| upto_10_kw                                  | int    | ≤10 kW count          |
| above_10_kw                                 | int    | >10 kW count          |
| installation                                | int    | Total installs        |
| inspection_approved                         | int    | Inspections approved  |
| inspection_rejected                         | int    | Inspections rejected  |
| inspection_pending                          | int    | Pending inspections   |
| total_redeem                                | int    | Subsidy redemptions   |
| total_redeem_amt                            | float  | Redeemed amount (₹)   |
| total_released                              | int    | Released count        |
| total_released_amt                          | float  | Released amount (₹)   |
| Applications Submitted for Loan             | int    | Loan applications     |
| Applications where Loan Sanction is Pending | int    | Pending sanctions     |
| Applications in which Loan is sanctioned    | int    | Sanctioned            |
| Applications where Loan is Disbursed        | int    | Disbursed             |
| Applications where Loan is rejected         | int    | Rejected loans        |

**Hierarchies:** State × DISCOM combination  
**Row Count:** ~300+ rows  
**Join Key:** state + discom → unique identifier

---

### 1.5 subsidy_status.csv

**Purpose:** Snapshot of subsidy processing pipeline (current state)

| Column     | Type   | Description                               |
| ---------- | ------ | ----------------------------------------- |
| Statuses   | string | Pipeline stage name                       |
| Count      | int    | Number of applications in stage           |
| Difference | int    | Delta from previous report (if available) |

**Rows:**

1. Redeemed till date
2. Released till date
3. Subsidy released till date (₹ amount)
4. On Hold
5. Return to consumer / discom
6. Pending for verification at maker
7. Pending for verification at checker
8. Maker and checker approved

**Purpose:** Bottleneck identification  
**Quality Issues:** Mix of count and amount metrics in same column

---

### 1.6 vendor_selection.csv

**Purpose:** Vendor selection request approval process

| Column                                               | Type   | Description       |
| ---------------------------------------------------- | ------ | ----------------- |
| Sl. No.                                              | int    | Serial number     |
| State                                                | string | State name        |
| Discom                                               | string | DISCOM name       |
| No. of Vendor Selection Requests Received (Nos.) (A) | int    | Total requests    |
| Vendor Selection Requests Pending (Nos.) (B)         | int    | Pending requests  |
| Vendor Selection Requests Approved (Nos.) (C)        | int    | Approved requests |
| Vendor Selection Requests Rejected (Nos.) (D)        | int    | Rejected requests |

**Hierarchy:** State × DISCOM  
**Key Metric:** Approval Rate = (C) / (A) _ 100  
**Key Metric:** Pending Rate = (B) / (A) _ 100  
**Row Count:** ~250+ rows

---

## 2. Data Cleaning Rules

### 2.1 Numeric Format Conversion

**Problem:** Numbers stored as strings with commas ("5,47,284")  
**Solution:**

```python
value = value.replace(",", "")  # Remove commas
value = int(value)               # Convert to integer
```

### 2.2 Column Naming Standardization

**Problem:** Inconsistent column names (spaces, hyphens, mixed case)  
**Solution:**

```python
columns = [col.lower().strip().replace(" ", "_").replace("-", "_") for col in df.columns]
```

### 2.3 Missing Value Strategy

- Numeric columns with NaN → Fill with 0 (represents no activity)
- String columns with NaN → Keep as-is or fill "Unknown"
- Document all assumptions

### 2.4 Date Format Standardization

**Problem:** Dates in DD-MM-YYYY format  
**Solution:**

```python
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
```

### 2.5 Type Conversion

- All count columns → integer (no decimals)
- All capacity columns → float (kW precision)
- All amount columns → float (₹ precision)
- All percentage columns → float (0-100)

---

## 3. Data Validation Rules

### 3.1 Range Validation

- All counts ≥ 0 (no negative applications)
- Capacity (kW) ≥ 0
- Subsidy amounts ≥ 0
- Percentages (approval rates) 0-100

### 3.2 Hierarchy Validation

- State × District: Every district must belong to exactly one state
- State × DISCOM: Every DISCOM must belong to exactly one state
- No orphaned districts or DISCOMs

### 3.3 Funnel Validation

- Applications ≥ Vendor Selected ≥ Feasibility Approved ≥ Installations ≥ Inspections ≥ Redeemed
- Each stage should be ≤ previous stage (progression)

### 3.4 Capacity Validation

- Installed Capacity ≤ Feasibility Approved Capacity
- Residential + RWA installations = Total installations
- ≤10kW + >10kW count = Total count

---

## 4. Derived Metrics (Calculated)

### 4.1 Conversion Rates

```
conv_l1_app_to_install = (installations / applications) * 100
conv_l2_app_to_subsidy = (total_redeem / applications) * 100
conv_l3_install_to_inspect = (inspection_approved / installations) * 100
```

### 4.2 Approval Rates

```
vendor_approval_rate = (vendor_selected / applications) * 100
feasibility_approval_rate = (feasibility_approved / applications) * 100
inspection_approval_rate = (inspection_approved / installations) * 100
```

### 4.3 Financial Metrics

```
subsidy_per_installation = total_redeem_amt / installations
subsidy_per_kw = total_redeem_amt / installed_capacity
subsidy_utilization_rate = (total_released / total_redeem) * 100
```

### 4.4 Capacity Metrics

```
avg_system_size_kw = installed_capacity / installations
residential_vs_rwa_ratio = residential_installation / rwa_installation
capacity_growth_pct = ((capacity_day_n - capacity_day_0) / capacity_day_0) * 100
```

---

## 5. Hierarchical Aggregation

| Level    | Unique Keys | Aggregation                   |
| -------- | ----------- | ----------------------------- |
| National | 1           | SUM all states                |
| State    | 36          | Raw data (per state)          |
| District | ~700        | Raw data (per state-district) |
| DISCOM   | ~300        | Raw data (per state-discom)   |
| Daily    | ~9          | Raw datewise data             |

---

## 6. Join Keys & Relationships

```
state_master
    │
    ├─ field: state
    │
    └─> LEFT JOIN district on (state_master.state = district.state)
    └─> LEFT JOIN discom_master on (state_master.state = discom_master.state)

district
    │
    ├─ fields: state, district
    │
    └─> Can join to state_master on state (for state-level metrics)

datewise (time-series)
    │
    ├─ fields: date
    │
    └─> Left outer join to others on date (limited matching period)

vendor_selection
    │
    ├─ fields: state, discom
    │
    └─> LEFT JOIN discom_master on (state, discom)
```

---

## 7. Data Dictionary (Complete)

### Key Buckets

**Application Pipeline:**

- application_status → vendor_selected → feasibility_approved → installation → inspection_approved → total_redeem

**Segment Breakdown:**

- residential_installation + rwa_installation = total installation
- upto_10_kw + above_10_kw = total count

**Capacity Tracking:**

- feasibility_approved_capacity → installed_capacity → inspection_approved_capacity

**Financial Tracking:**

- total_redeem_amt (subsidy redeemed) → total_released_amt (subsidy released)

**Loan Tracking:**

- Applications Submitted for Loan → Loan Sanction Pending → Loan Sanctioned → Loan Disbursed vs Rejected

---

## 8. External Data Integration (For Enrichment)

### 8.1 Population Data

**Source:** Government of India Census data  
**Join:** state, district  
**Usage:** Calculate adoption per capita (applications/population)

### 8.2 Solar Potential Data

**Source:** NREL/Government solar atlases  
**Join:** state, district  
**Usage:** Context for adoption expectations by region

### 8.3 Climate Data

**Source:** India Meteorological Department  
**Join:** state, district  
**Usage:** Sunshine hours, temperature context for feasibility

---

## 9. Quality Control Checklist

- [ ] All numeric columns parsed (no commas)
- [ ] All dates converted to datetime format
- [ ] Column names standardized (lowercase, underscores)
- [ ] No NaN values without documentation
- [ ] All hierarchies validated (no orphaned records)
- [ ] Funnel logic verified (each stage ≤ previous)
- [ ] Row counts match source data
- [ ] Spot-check KPI calculations
- [ ] All derived metrics calculated correctly
- [ ] Output saved to `data_cleaned/` folder

---

**Document Owner:** Analytics Project Lead  
**Last Updated:** March 14, 2026
