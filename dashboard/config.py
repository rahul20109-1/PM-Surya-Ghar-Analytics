"""
Dashboard Configuration
=======================
Settings and constants for the Streamlit dashboard.
"""

# Page Configuration
PAGE_TITLE = "PM Surya Ghar Analytics"
PAGE_ICON = "☀️"
LAYOUT = "wide"

# Color Palette (from FRONTEND_GUIDELINES.md)
COLORS = {
    'primary': '#1f77b4',      # Blue
    'secondary': '#ff7f0e',    # Orange
    'tertiary': '#2ca02c',     # Green
    'alert': '#d62728',        # Red
    'background': '#ffffff',   # White
    'grid': '#e8e8e8',         # Light Gray
    'text': '#333333',         # Dark Gray
    'disabled': '#cccccc',     # Medium Gray
}

# Categorical colors
CATEGORICAL_COLORS = [
    '#1f77b4',  # Blue
    '#ff7f0e',  # Orange
    '#2ca02c',  # Green
    '#d62728',  # Red
    '#9467bd',  # Purple
    '#8c564b',  # Brown
]

# Data Configuration
DATA_DIR = 'data_cleaned'
KPI_FILES = ['kpis_national.csv', 'kpis_state.csv', 'kpis_district.csv']
DETAIL_FILES = ['datewise_clean.csv', 'state_master_clean.csv', 'district_clean.csv']

# Dashboard Pages
PAGES = {
    'overview': 'Overview',
    'state': 'State Analysis',
    'district': 'District Analysis',
    'trends': 'Trends',
    'capacity': 'Capacity Metrics',
    'about': 'About'
}

# Font Settings
FONT_FAMILY = 'sans-serif'
FONT_SIZE_TITLE = 28
FONT_SIZE_HEADER = 24
FONT_SIZE_SUBHEADER = 20

# Chart Settings
CHART_HEIGHT = 500
CHART_TEMPLATE = 'plotly_white'
CHART_HOVERMODE = 'x unified'

# Display Settings
NUMBER_FORMAT = '{:,}'
PERCENT_FORMAT = '{:.1f}%'
DECIMAL_FORMAT = '{:.2f}'

# Data Refresh
CACHE_TIMEOUT = 3600  # 1 hour in seconds
