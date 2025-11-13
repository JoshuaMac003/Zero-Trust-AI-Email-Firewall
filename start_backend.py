"""
Start Backend Server
Convenience script to start the FastAPI backend server
"""

import os
import sys
import uvicorn

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    # Change to project root directory
    os.chdir(project_root)
    
    # Start server
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )


