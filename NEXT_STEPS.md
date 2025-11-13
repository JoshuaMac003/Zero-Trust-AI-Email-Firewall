# ✅ Next Steps - Your Dataset is Ready!

## 🎉 Great News!

Your dataset has been successfully prepared:
- **82,481 rows** combined from 6 CSV files
- **52% phishing** (42,886 rows)
- **48% legitimate** (39,595 rows)
- Dataset saved to: `dataset/phishing_dataset.csv`

## 🚀 Next Steps

### Step 1: Train the Model

```bash
cd "E:\cybersecurity  phishing email detector\ZeroTrust-AI-Email-Firewall"
python backend/model/train_model.py --no-grid-search
```

**Note:** 
- This will take **10-15 minutes** (without grid search)
- With grid search: **30-60 minutes** (more accurate)
- The `--no-grid-search` flag makes training faster

**Expected Output:**
```
INFO - Model training completed!
INFO - Models saved successfully!
```

### Step 2: Start the Backend Server

```bash
python start_backend.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 3: Test the Connection

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

## 🎯 Quick Start (All in One)

You can also use the batch file:

```bash
setup_and_start.bat
```

This will:
1. Initialize database
2. Prepare dataset (if needed)
3. Train model (if needed)
4. Start the server

## 📝 What Happens During Training

1. **Data Loading:** Loads 82,481 emails from dataset
2. **Preprocessing:** Cleans and normalizes text
3. **Training:** Trains Logistic Regression model
4. **Evaluation:** Tests on 20% of data
5. **Calibration:** Calibrates model for better probabilities
6. **Saving:** Saves model to `backend/model/`

## 🧪 After Server Starts

1. **Test API:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **View API Docs:**
   Open `http://localhost:8000/docs` in browser

3. **Start Frontend:**
   ```bash
   python start_frontend.py
   ```

4. **Open Browser:**
   `http://localhost:8501`

## 🐛 Troubleshooting

### Issue: "Model training takes too long"

**Solution:** Use `--no-grid-search` flag:
```bash
python backend/model/train_model.py --no-grid-search
```

### Issue: "Out of memory"

**Solution:** Reduce dataset size or use smaller model parameters

### Issue: "Port 8000 already in use"

**Solution:**
1. Find process: `netstat -ano | findstr :8000`
2. Kill process or change port in `start_backend.py`

## ✅ Success Checklist

- [x] Dataset prepared (82,481 rows)
- [ ] Model trained
- [ ] Backend server started
- [ ] Health check passes
- [ ] API docs accessible
- [ ] Frontend running
- [ ] Tests pass

## 📊 Expected Model Performance

With 82,481 rows:
- **Accuracy:** > 85%
- **Precision:** > 80%
- **Recall:** > 80%
- **F1-Score:** > 80%

## 🎉 You're Almost There!

Just train the model and start the server, then you're ready to go!

---

**Quick Commands:**
```bash
# Train model (fast)
python backend/model/train_model.py --no-grid-search

# Start backend
python start_backend.py

# Test connection
curl http://localhost:8000/health
```


