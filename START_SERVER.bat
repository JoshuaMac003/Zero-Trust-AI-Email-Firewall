@echo off
REM Start Backend Server for Zero-Trust AI Email Firewall

echo ========================================
echo Zero-Trust AI Email Firewall
echo Starting Backend Server...
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Dependencies are not installed
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Initialize database
echo.
echo Initializing database...
python backend/database/init_db.py

REM Check if dataset exists
if not exist "dataset\phishing_dataset.csv" (
    echo.
    echo WARNING: Dataset not found!
    echo Please create dataset/phishing_dataset.csv
    echo Or run: python prepare_dataset.py
    echo.
    pause
)

REM Check if model exists
if not exist "backend\model\calibrated_model.pkl" (
    echo.
    echo WARNING: Model not trained!
    echo Please train the model first:
    echo   python backend/model/train_model.py
    echo.
    echo Or the server will start but won't be able to scan emails.
    echo.
    pause
)

REM Start server
echo.
echo Starting backend server...
echo Server will be available at: http://localhost:8000
echo API docs will be available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python start_backend.py

pause


