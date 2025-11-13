# Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download spaCy Language Model (Recommended)

For optimized preprocessing with spaCy:

```bash
python -m spacy download en_core_web_sm
```

**Note:** The system will work without spaCy, but preprocessing will be less optimized.

### 3. Train the Model

Ensure you have `phishing_email_dataset.csv` with 'text' and 'label' columns, then:

```bash
python phishing_detector.py
```

This will:
- Preprocess the data using spaCy (if available)
- Perform hyperparameter tuning
- Train and calibrate the model
- Evaluate on test set
- Save models to disk

### 4. Use the System

#### Option A: Streamlit Web UI

```bash
streamlit run streamlit_app.py
```

Open your browser to `http://localhost:8501`

#### Option B: FastAPI REST API

```bash
python api.py
```

Or using uvicorn directly:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

API will be available at:
- API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

#### Option C: Python Script

```python
from phishing_detector import PhishingEmailDetector

detector = PhishingEmailDetector()
detector.load_model()

result, confidence = detector.predict("Your email text here...")
print(f"Prediction: {result}, Confidence: {confidence:.2%}")
```

## API Endpoints

### POST `/predict`
Predict a single email:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your email text here..."}'
```

### POST `/predict/batch`
Predict multiple emails:
```bash
curl -X POST "http://localhost:8000/predict/batch" \
     -H "Content-Type: application/json" \
     -d '{"emails": ["Email 1...", "Email 2..."]}'
```

### GET `/health`
Check API health and model status

### GET `/model/info`
Get information about the loaded model

## Troubleshooting

### spaCy Model Not Found
If you see warnings about spaCy model:
```bash
python -m spacy download en_core_web_sm
```

### Model Files Not Found
Train the model first:
```bash
python phishing_detector.py
```

### Port Already in Use
Change the port in `api.py` or use:
```bash
uvicorn api:app --port 8001
```



