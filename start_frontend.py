"""
Start Frontend Server
Convenience script to start the Streamlit frontend
"""

import os
import sys
import subprocess

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    # Change to project root directory
    os.chdir(project_root)
    
    # Start Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "frontend/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])


