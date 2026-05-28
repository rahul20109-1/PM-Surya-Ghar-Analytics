import sys
from pathlib import Path

# Ensure project root is on sys.path so `dashboard` package can be imported
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dashboard.utils.data_loader import load_data

try:
	kpi_national,kpi_state,kpi_district,datewise,state_master,district = load_data()
	print('columns:', list(state_master.columns))
	print('has_cols:', all(c in state_master.columns for c in ['application_status','vendor_selected','installation','inspection_approved','total_redeem']))
	print(state_master.head().to_string())
except Exception as e:
	import traceback

	print('ERROR during load_data:')
	traceback.print_exc()
