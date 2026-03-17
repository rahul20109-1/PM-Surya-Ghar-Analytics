# Technology Stack

## PM Surya Ghar Analytics - Locked Dependencies and Tooling

Last Updated: March 17, 2026

## 1. Runtime

- Python 3.11

## 2. Data Processing

- pandas==2.0.3
- numpy==1.24.3
- openpyxl==3.10.10

## 3. Visualization

- plotly==5.17.0
- matplotlib==3.7.2
- seaborn==0.12.2

## 4. Dashboard

- streamlit==1.28.1
- streamlit-aggrid==0.3.4

## 5. Notebook and Development

- jupyter==1.0.0
- jupyterlab==4.0.6
- ipython==8.14.0

## 6. Code Quality

- black==23.9.1
- pylint==2.17.5
- flake8==6.0.0

## 7. Utility

- requests==2.31.0

## 8. Governance Rules

- requirements.txt is the installation source of truth.
- Documentation must reference locked versions above, not ad-hoc local upgrades.
- Stack changes require synchronized updates in requirements.txt and this document.
