# 🔧 Fix Connection Error - Backend Not Running

## Problem
```
curl: (7) Failed to connect to localhost port 8000
```

This means the backend server is not running.

## ✅ Solution: Follow These Steps

### Step 1: Navigate to Project Directory

```bash
cd "E:\cybersecurity  phishing email detector\ZeroTrust-AI-Email-Firewall"
```

### Step 2: Initialize Database

```bash
python backend/database/init_db.py
```

**Expected Output:**
```
INFO - Database initialized successfully at backend/database/firewall.db
```

### Step 3: Prepare Dataset

You have dataset files in the parent directory. Let's prepare them:

```bash
python prepare_dataset.py
```

This will:
- Look for CSV files in `phishing_email_dataset.csv/` directory
- Combine them into `dataset/phishing_dataset.csv`
- Create a sample dataset if none found

### Step 4: Train the Model

```bash
python backend/model/train_model.py
```

**Note:** This may take 5-15 minutes. For faster training (without grid search):

```bash
python backend/model/train_model.py --no-grid-search
```

**Expected Output:**
```
INFO - Model training completed!
INFO - Models saved successfully!
```

### Step 5: Start the Backend Server

**Option A: Using Python script**
```bash
python start_backend.py
```

**Option B: Using batch file (Windows)**
```bash
START_SERVER.bat
```

**Option C: Using uvicorn directly**
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 6: Test the Connection

**In a new terminal:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_initialized": true,
  "message": "Service is operational"
}
```

## 🚀 Quick Start (All in One)

If you want to do everything at once, use the quick start script:

```bash
cd "E:\cybersecurity  phishing email detector\ZeroTrust-AI-Email-Firewall"
python quick_start.py
```

This will:
1. Check dependencies
2. Initialize database
3. Prepare dataset
4. Train model (if needed)
5. Start the server

## 🎯 Manual Setup (Step by Step)

### 1. Check Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Initialize Database

```bash
python backend/database/init_db.py
```

### 3. Prepare Dataset

```bash
python prepare_dataset.py
```

Or create manually: `dataset/phishing_dataset.csv` with columns: `text`, `label`

### 4. Train Model

```bash
python backend/model/train_model.py
```

### 5. Start Server

```bash
python start_backend.py
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Dataset not found"

**Solution:**
```bash
python prepare_dataset.py
```

Or create `dataset/phishing_dataset.csv` manually.

### Issue: "Model not found"

**Solution:**
```bash
python backend/model/train_model.py
```

### Issue: "Port 8000 already in use"

**Solution:**
1. Find process using port 8000:
   ```bash
   netstat -ano | findstr :8000
   ```
2. Kill the process or change port in `start_backend.py`

### Issue: "Database error"

**Solution:**
```bash
python backend/database/init_db.py
```

## ✅ Verification

After starting the server, verify it's running:

1. **Check health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check API docs:**
   Open `http://localhost:8000/docs` in browser

3. **Test email scan:**
   ```bash
   curl -X POST "http://localhost:8000/scan-email" \
        -H "Content-Type: application/json" \
        -d '{"email_text": "Subject: Test\n\nThis is a test email."}'
   ```

## 📝 Next Steps

After the server is running:

1. **Start Frontend:**
   ```bash
   python start_frontend.py
   ```

2. **Open Browser:**
   `http://localhost:8501`

3. **Run Tests:**
   ```bash
   python test_api.py
   ```

## 🎉 Success!

If you see the health check response, the backend is running correctly!

---

**Quick Reference:**
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:8501`
- Health Check: `curl http://localhost:8000/health`


