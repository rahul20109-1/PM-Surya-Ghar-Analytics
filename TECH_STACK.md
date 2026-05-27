# Technology Stack

## PM Surya Ghar Analytics - Runtime and Tooling

Last Updated: May 27, 2026

## 1. Runtime

- Python 3.11.9 (see runtime.txt)

## 2. Dashboard Runtime Dependencies (requirements.txt)

- streamlit>=1.28,<2.0
- pandas>=2.3
- numpy>=2.0
- plotly>=5.17

## 3. Notebook and Analysis (local dev)

- matplotlib
- seaborn
- jupyter
- jupyterlab
- ipython

## 4. Data Processing (optional)

- openpyxl (only required for Excel ingestion; current pipeline uses CSV)

## 5. Code Quality (optional)

- black
- pylint
- flake8

## 6. Governance Rules

- requirements.txt is the runtime source of truth for Streamlit Cloud.
- If a new runtime dependency is added, update requirements.txt and this document together.
- Notebook-only packages can be installed locally without changing requirements.txt unless needed for deployment.
