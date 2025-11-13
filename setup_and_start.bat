@echo off
REM Setup and Start Script for Zero-Trust AI Email Firewall

echo ========================================
echo Zero-Trust AI Email Firewall
echo Setup and Start Script
echo ========================================
echo.

cd /d "%~dp0"

REM Step 1: Initialize Database
echo [1/4] Initializing database...
python backend/database/init_db.py
if errorlevel 1 (
    echo ERROR: Database initialization failed
    pause
    exit /b 1
)
echo.

REM Step 2: Prepare Dataset (if needed)
echo [2/4] Preparing dataset...
if not exist "dataset\phishing_dataset.csv" (
    echo Dataset not found, preparing...
    python prepare_dataset.py
    if errorlevel 1 (
        echo ERROR: Dataset preparation failed
        pause
        exit /b 1
    )
) else (
    echo Dataset already exists
)
echo.

REM Step 3: Train Model (if needed)
echo [3/4] Checking model...
if not exist "backend\model\calibrated_model.pkl" (
    echo Model not found, training model...
    echo This may take 10-15 minutes...
    python backend/model/train_model.py --no-grid-search
    if errorlevel 1 (
        echo ERROR: Model training failed
        echo You can train it later manually
        pause
    )
) else (
    echo Model already trained
)
echo.

REM Step 4: Start Server
echo [4/4] Starting backend server...
echo.
echo Server will be available at: http://localhost:8000
echo API docs will be available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python start_backend.py

pause


