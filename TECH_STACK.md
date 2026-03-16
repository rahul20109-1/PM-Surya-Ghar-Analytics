# Technology Stack (TECH_STACK.md)

# PM Surya Ghar Analytics — Locked Dependencies

**Purpose:** Specify all technologies, lock versions, and enforce consistency across the project.

---

## 1. Core Language & Runtime

| Component            | Version                      | Rationale                                |
| -------------------- | ---------------------------- | ---------------------------------------- |
| **Python**           | 3.11.x                       | Latest stable, full pandas/numpy support |
| **Operating System** | Windows 10/11 or macOS/Linux | Cross-platform support                   |

---

## 2. Data Processing & Analysis

| Package      | Version | Purpose                                  | Why                                |
| ------------ | ------- | ---------------------------------------- | ---------------------------------- |
| **pandas**   | 2.0.3   | Data manipulation, cleaning, aggregation | Industry standard for tabular data |
| **numpy**    | 1.24.3  | Numerical computations, array operations | Fast, foundational for pandas      |
| **openpyxl** | 3.10.x  | Read/write Excel (if needed in future)   | For any Excel enrichment data      |

---

## 3. Data Visualization

| Package        | Version | Purpose                                      | Why                                         |
| -------------- | ------- | -------------------------------------------- | ------------------------------------------- |
| **plotly**     | 5.17.0  | Interactive charts, dashboard visualizations | Professional, interactive, Streamlit-native |
| **matplotlib** | 3.7.x   | Static plots, exports                        | Fallback for simple visualizations          |
| **seaborn**    | 0.12.x  | Statistical visualizations                   | Built on matplotlib, cleaner API            |

---

## 4. Web Dashboard

| Package              | Version | Purpose                                | Why                                                        |
| -------------------- | ------- | -------------------------------------- | ---------------------------------------------------------- |
| **streamlit**        | 1.28.1  | Interactive web app framework          | Fastest path to dashboard, Python-native, deployment-ready |
| **streamlit-aggrid** | 0.3.x   | Advanced tables/filtering in Streamlit | Enhanced data exploration                                  |

---

## 5. Jupyter Notebook & Development

| Package        | Version | Purpose                    | Why                                    |
| -------------- | ------- | -------------------------- | -------------------------------------- |
| **jupyter**    | 1.0.0   | Notebook runtime           | Narrative analysis, exploratory coding |
| **jupyterlab** | 4.0.x   | Enhanced notebook IDE      | Richer development experience          |
| **ipython**    | 8.14.x  | Enhanced interactive shell | Better notebook integration            |

---

## 6. Development & Code Quality

| Package    | Version | Purpose              | Why                            |
| ---------- | ------- | -------------------- | ------------------------------ |
| **black**  | 23.x    | Code formatter       | Enforce consistent style       |
| **pylint** | 2.17.x  | Code linter          | Catch errors, style violations |
| **flake8** | 6.0.x   | Style guide enforcer | PEP 8 compliance               |

---

## 7. Version Control

| Tool               | Version       | Purpose                              |
| ------------------ | ------------- | ------------------------------------ |
| **Git**            | Latest stable | Version control                      |
| **GitHub**         | N/A (Cloud)   | Remote repository, CI/CD integration |
| **GitHub Actions** | N/A (Cloud)   | Automated testing (future)           |

---

## 8. Deployment & Hosting

| Platform                             | Tier        | Purpose                         |
| ------------------------------------ | ----------- | ------------------------------- |
| **Streamlit Cloud**                  | Free tier   | Deploy dashboard publicly       |
| **GitHub**                           | Public repo | Store code, documentation       |
| **GitHub Student Developer Program** | Benefits    | Free/discounted cloud resources |

---

## 9. Development Environment

| Tool                            | Purpose                    |
| ------------------------------- | -------------------------- |
| **VS Code**                     | Code editor                |
| **GitHub Copilot**              | AI assistant for coding    |
| **Python Extension (VS Code)**  | Python IDE support         |
| **Jupyter Extension (VS Code)** | Notebook support in editor |

---

## 10. Data Storage Format

| Format      | Use Case                                         |
| ----------- | ------------------------------------------------ |
| **CSV**     | Raw data input, cleaned data export, KPI output  |
| **Parquet** | (Optional) Compressed storage for large datasets |
| **JSON**    | Dashboard configuration, metadata                |

---

## 11. Requirements.txt (Frozen Versions)

```
# Core Data Processing
pandas==2.0.3
numpy==1.24.3
openpyxl==3.10.10

# Visualization
plotly==5.17.0
matplotlib==3.7.2
seaborn==0.12.2

# Dashboard
streamlit==1.28.1
streamlit-aggrid==0.3.4

# Jupyter
jupyter==1.0.0
jupyterlab==4.0.6
ipython==8.14.0

# Code Quality
black==23.9.1
pylint==2.17.5
flake8==6.0.0

# Data Import (optional, for enrichment)
requests==2.31.0  # For fetching external data
```
