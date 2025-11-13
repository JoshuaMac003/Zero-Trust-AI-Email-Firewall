# 🚀 Execution Guide - Phishing Email Detection System

Complete step-by-step guide to run the phishing email detection system.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🎯 Step-by-Step Execution

### Step 1: Install Dependencies

Open your terminal/command prompt and navigate to the project directory:

```bash
cd "E:\cybersecurity  phishing email detector"
```

Install required packages:

```bash
pip install -r requirements.txt
```

**Expected output:** All packages will be installed (pandas, numpy, scikit-learn, etc.)

---

### Step 2: Download spaCy Language Model (Recommended)

For optimized preprocessing:

```bash
python -m spacy download en_core_web_sm
```

**Note:** This step is optional. The system will work without it but with basic preprocessing.

**Expected output:**
```
✔ Download and installation successful
```

---

### Step 3: Prepare Your Dataset

Create a CSV file named `phishing_email_dataset.csv` in the project directory with the following format:

```csv
text,label
"Congratulations! You won $1,000,000. Click here to claim...",1
"Meeting reminder: Tomorrow at 2 PM in conference room",0
"Your account will be suspended. Verify now at...",1
"Thanks for your order. Your package is on the way.",0
```

**Columns:**
- `text`: Email body/content
- `label`: 1 for phishing, 0 for legitimate

---

### Step 4: Train the Model

Train the machine learning model:

```bash
python phishing_detector.py
```

**What happens:**
1. Loads the dataset
2. Preprocesses emails (using spaCy if available)
3. Performs hyperparameter tuning (may take 5-15 minutes)
4. Trains the model
5. Evaluates on test set
6. Saves model files:
   - `vectorizer.joblib`
   - `phishing_model.joblib`
   - `calibrated_model.joblib`

**Expected output:**
```
INFO - Loading dataset from phishing_email_dataset.csv...
INFO - Starting data preprocessing...
INFO - Preprocessed X samples
INFO - Starting model training...
INFO - Performing hyperparameter tuning with GridSearchCV...
INFO - Best parameters: {...}
INFO - Best CV score (ROC-AUC): 0.XXXX
INFO - Calibrating model...
INFO - Model training completed!
INFO - Evaluating model on test set...
INFO - Accuracy: 0.XXXX
...
```

**⚠️ Important:** Wait for this to complete before proceeding to next steps.

---

### Step 5: Choose Your Interface

You have **3 options** to use the trained model:

---

## 🎨 Option A: Streamlit Web UI (Easiest)

### Start the Streamlit Server

```bash
streamlit run streamlit_app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Use the Interface

1. **Open your browser** to `http://localhost:8501`
2. **In the sidebar**, click "Load Model" button
3. **Wait for confirmation** - should see "Model loaded successfully!"
4. **Paste an email** in the text area
5. **Click "Analyze Email"** button
6. **View results** - prediction and confidence score

**To stop:** Press `Ctrl+C` in the terminal

---

## 🔌 Option B: FastAPI REST API (For Integration)

### Start the API Server

```bash
python api.py
```

Or using uvicorn directly:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Access the API

1. **Interactive API Docs:** Open `http://localhost:8000/docs` in your browser
2. **Test the API:**
   - Click on `/predict` endpoint
   - Click "Try it out"
   - Enter email text in the JSON body
   - Click "Execute"

### Use with cURL

**Single Prediction:**
```bash
curl -X POST "http://localhost:8000/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"text\": \"Congratulations! You won $1,000,000. Click here...\"}"
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

**To stop:** Press `Ctrl+C` in the terminal

---

## 🐍 Option C: Python Script (Programmatic)

### Create a Python Script

Create a file `test_prediction.py`:

```python
from phishing_detector import PhishingEmailDetector

# Initialize detector
detector = PhishingEmailDetector()

# Load trained model
print("Loading model...")
detector.load_model()
print("Model loaded!")

# Test email
email_text = "Congratulations! You have won $1,000,000. Click here to claim your prize: http://fake-link.com/claim"

# Make prediction
result, confidence = detector.predict(email_text)

print(f"\nEmail: {email_text[:80]}...")
print(f"Prediction: {result}")
print(f"Confidence: {confidence:.2%}")
```

### Run the Script

```bash
python test_prediction.py
```

**Expected output:**
```
Loading model...
Model loaded!

Email: Congratulations! You have won $1,000,000. Click here to claim your prize...
Prediction: Phishing
Confidence: 95.23%
```

---

## 📊 Quick Reference Commands

### Training Only
```bash
python phishing_detector.py
```

### Streamlit UI
```bash
streamlit run streamlit_app.py
```

### FastAPI Server
```bash
python api.py
# or
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Test API (Windows PowerShell)
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/predict" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"text": "Your email text here"}'
```

---

## 🔍 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'X'"
**Solution:** Install missing package
```bash
pip install X
# or reinstall all
pip install -r requirements.txt
```

### Issue: "Dataset not found"
**Solution:** Ensure `phishing_email_dataset.csv` exists in the project directory

### Issue: "Model files not found"
**Solution:** Train the model first using `python phishing_detector.py`

### Issue: "spaCy model not found"
**Solution:** 
```bash
python -m spacy download en_core_web_sm
```
Or ignore - the system will use basic preprocessing

### Issue: Port already in use
**Solution:** Change port
```bash
# For FastAPI
uvicorn api:app --port 8001

# For Streamlit
streamlit run streamlit_app.py --server.port 8502
```

### Issue: Training takes too long
**Solution:** Disable grid search in `phishing_detector.py`:
```python
detector.train_model(X_train, y_train, perform_grid_search=False)
```

---

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] spaCy model downloaded (optional but recommended)
- [ ] Dataset file exists (`phishing_email_dataset.csv`)
- [ ] Model trained successfully (`python phishing_detector.py`)
- [ ] Model files created (`.joblib` files in directory)
- [ ] One of the interfaces is running (Streamlit/FastAPI/Python)

---

## 🎯 Typical Workflow

1. **First Time Setup:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Train Model (One Time):**
   ```bash
   python phishing_detector.py
   ```

3. **Use the System:**
   - **For testing:** `streamlit run streamlit_app.py`
   - **For production:** `python api.py`
   - **For scripts:** Import and use `PhishingEmailDetector` class

---

## 📝 Example Dataset

If you need a quick test, create `phishing_email_dataset.csv`:

```csv
text,label
"Congratulations! You won $1,000,000. Click here to claim: http://fake.com",1
"Your account will be suspended. Verify now at http://suspicious.com",1
"URGENT: Click this link immediately to prevent account closure",1
"Meeting reminder: Tomorrow at 2 PM in conference room",0
"Thanks for your order. Your package will arrive tomorrow",0
"Team meeting scheduled for next week. Please confirm attendance",0
```

**Note:** You'll need more data (hundreds/thousands of examples) for a good model!

---

## 🚀 Next Steps

After successful execution:
- Experiment with different emails
- Analyze the model's performance metrics
- Integrate the API into your applications
- Customize hyperparameters for better results

Happy phishing detection! 🎉


