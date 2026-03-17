# Product Requirements Document

## PM Surya Ghar Analytics

Last Updated: March 17, 2026  
Document Status: Final (Portfolio Release)

## 1. Product Summary

PM Surya Ghar Analytics is a portfolio-grade analytics project that evaluates program adoption, conversion efficiency, and operational bottlenecks in the PM Surya Ghar rooftop solar subsidy initiative.

The product combines:
- Data cleaning and quality validation pipeline
- KPI engineering for national, state, and district views
- Exploratory analytics for pattern and bottleneck analysis
- Interactive Streamlit dashboard for stakeholder consumption

## 2. Portfolio Objective

Demonstrate end-to-end analytics capability expected in professional data teams:
- Structured problem framing
- Reliable data preparation and verification
- Metric design and interpretation
- Dashboard productization and communication quality

## 3. Intended Audience

Primary audience:
- Hiring managers
- Analytics and data engineering interview panels
- Technical reviewers evaluating implementation quality

Secondary audience:
- Policy and operations stakeholders interested in program analytics workflows

## 4. In-Scope Deliverables

- Reproducible cleaning scripts and utilities in scripts/
- Verified KPI outputs in data_cleaned/
- Analysis notebooks documenting logic and validation
- Streamlit dashboard with core and advanced analysis views
- Professional project documentation set

## 5. Out-of-Scope Items

- Predictive machine learning models
- Production backend services or APIs
- Database migration architecture
- Real-time streaming ingestion

## 6. Core Analytics Questions

- What is the national application-to-installation conversion level?
- Which geographies are over- or under-performing?
- Where are the largest stage-level drop-offs in the process funnel?
- How does processing behavior vary over time?
- Which operational metrics best explain backlog and throughput risk?

## 7. KPI Requirements

Priority KPIs include:
- Total applications
- Total installations
- Total inspections
- Conversion rate: applications to installations
- Conversion rate: applications to subsidy stage
- Conversion rate: installations to inspections
- Total states, districts, and DISCOMs represented

KPIs must be:
- Reproducible from cleaned sources
- Documented with explicit formulas
- Aligned with exported KPI artifacts

## 8. Success Criteria

The portfolio release is considered successful when:
- Documentation is coherent, concise, and reviewer-friendly
- KPI outputs can be traced to cleaned data artifacts
- Dashboard experience is operational and interpretable
- Code organization reflects professional modular structure
- Major analytical claims are verifiable from repository data

## 9. Constraints

- Locked technology stack defined in TECH_STACK.md and requirements.txt
- CSV-based workflow (no external database dependency)
- Raw source files remain read-only

## 10. Acceptance Checklist

- Data pipeline artifacts present and readable
- KPI outputs generated and validated
- Dashboard starts with documented command
- Documentation reflects current repository state
- Portfolio narrative is suitable for interview discussion
