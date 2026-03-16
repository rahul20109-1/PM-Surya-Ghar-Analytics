"""
Data Loading and Caching Utilities
===================================
Handles loading and caching of cleaned data files with error handling.
"""

import pandas as pd
from pathlib import Path
import streamlit as st

@st.cache_data
def load_data():
    """
    Load all cleaned data files with error handling.
    
    Returns:
        tuple: (kpi_national, kpi_state, kpi_district, datewise, state_master, district)
    """
    
    # Determine data directory
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data_cleaned'
    
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    try:
        # Load KPI files
        kpi_national = pd.read_csv(data_dir / 'kpis_national.csv')
        kpi_state = pd.read_csv(data_dir / 'kpis_state.csv')
        kpi_district = pd.read_csv(data_dir / 'kpis_district.csv')
        
        # Load detail data files
        datewise = pd.read_csv(data_dir / 'datewise_clean.csv')
        state_master = pd.read_csv(data_dir / 'state_master_clean.csv')
        district = pd.read_csv(data_dir / 'district_clean.csv')
        
        return kpi_national, kpi_state, kpi_district, datewise, state_master, district
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Failed to load data files: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")
