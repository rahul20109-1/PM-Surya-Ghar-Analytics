"""
PM Surya Ghar Analytics Dashboard
==================================
Interactive dashboard for analyzing India's solar rooftop subsidy program.

Package Contents:
- streamlit_app.py: Main dashboard application
- config.py: Configuration and constants
- utils/: Utility modules (data loading, components, charts)
"""

__version__ = '1.0.0'
__author__ = 'Analytics Team'
__date__ = 'March 15, 2026'

from .config import COLORS, PAGES, CATEGORICAL_COLORS

__all__ = ['COLORS', 'PAGES', 'CATEGORICAL_COLORS']
