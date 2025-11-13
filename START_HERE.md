# 🚀 START HERE - Quick Setup Guide

## Problem: Backend Not Running

If you see `curl: (7) Failed to connect to localhost port 8000`, the backend server is not running.

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

### Step 3: Prepare Dataset (If Not Done)

Create `dataset/phishing_dataset.csv` with columns: `text`, `label`

**Example:**
```csv
text,label
"Congratulations! You won $1,000,000. Click here to claim: http://fake-link.com",1
"Meeting reminder: Tomorrow at 2 PM in conference room",0
"Your account will be suspended. Verify now at http://suspicious.com",1
"Thanks for your order. Your package will arrive tomorrow",0
```

### Step 4: Train the Model

```bash
python backend/model/train_model.py
```

**Note:** This may take 5-15 minutes depending on your dataset size.

**Expected Output:**
```
INFO - Model training completed!
INFO - Models saved successfully!
```

### Step 5: Start the Backend Server

```bash
python start_backend.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 6: Test the API (New Terminal)

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

## 🎯 Quick Start (If Everything is Ready)

If database and model are already set up, just start the server:

```bash
cd "E:\cybersecurity  phishing email detector\ZeroTrust-AI-Email-Firewall"
python start_backend.py
```

## 🐛 Troubleshooting

### Issue: "Model not found"

**Solution:**
```bash
python backend/model/train_model.py
```

### Issue: "Database not initialized"

**Solution:**
```bash
python backend/database/init_db.py
```

### Issue: "Dataset not found"

**Solution:**
1. Create `dataset/phishing_dataset.csv`
2. Add columns: `text`, `label`
3. Add sample emails

### Issue: "Port 8000 already in use"

**Solution:**
1. Find process using port 8000:
   ```bash
   netstat -ano | findstr :8000
   ```
2. Kill the process or change port in `start_backend.py`

## 📝 Next Steps

After backend is running:

1. **Test API:** `curl http://localhost:8000/health`
2. **Start Frontend:** `python start_frontend.py`
3. **Open Browser:** `http://localhost:8501`
4. **Run Tests:** `python test_api.py`

## ✅ Verification Checklist

- [ ] Database initialized
- [ ] Dataset exists
- [ ] Model trained
- [ ] Backend started
- [ ] Health check passes
- [ ] API responds

## 🎉 Success!

If you see the health check response, the backend is running correctly!

---

For more details, see:
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `TESTING_GUIDE.md` - Testing instructions


