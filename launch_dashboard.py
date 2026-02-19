#!/usr/bin/env python3
"""
Simple launcher script for the Financial Inclusion Dashboard
"""

import sys
import os
from pathlib import Path

# Add dashboard directory to path
dashboard_dir = Path(__file__).parent / "dashboard"
sys.path.insert(0, str(dashboard_dir))

# Change to dashboard directory
os.chdir(dashboard_dir)

# Import and run the app
try:
    from app import app

    print("\n" + "=" * 60)
    print("🚀 Financial Inclusion Dashboard")
    print("=" * 60)
    print("📊 Opening at: http://127.0.0.1:8050/")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")

    app.run(debug=True, host="127.0.0.1", port=8050)

except Exception as e:
    print(f"\n❌ Error launching dashboard: {e}")
    print("\nPlease ensure you have installed the required packages:")
    print("  pip install dash plotly dash-bootstrap-components")
    sys.exit(1)
