# 🛡️ Zero-Trust AI Email Firewall

A complete, production-ready **Zero-Trust AI Email Firewall** web application that uses Artificial Intelligence and Zero-Trust principles to detect, classify, and block phishing or suspicious emails in real-time.

## 🎯 Project Overview

**Name:** ZeroTrust-AI-Email-Firewall

**Goal:** Detect and block phishing or malicious emails using NLP + Zero-Trust verification

**Stack:**
- **Backend:** Python (FastAPI)
- **Frontend:** Streamlit
- **Model:** Scikit-learn (Logistic Regression with TF-IDF)
- **Database:** SQLite (for email logs + user data)
- **NLP:** spaCy (optimized preprocessing)

## ✨ Features

### 🤖 AI Email Classification
- Preprocess email text (subject, body, sender)
- Extract features using TF-IDF vectorization
- Train/test phishing detection model
- Output: "Safe", "Suspicious", or "Phishing"
- Confidence scores for predictions

### 🛡️ Zero-Trust Policy Engine
- Verify sender domain reputation
- SPF/DKIM checks (simulated)
- Apply access-control decision logic (never trust, always verify)
- Combine trust score + AI output for final verdict
- Trusted domain management

### 📊 Firewall Dashboard
- Show scanned emails with timestamps, sender, prediction, and confidence
- Upload sample emails (CSV or text)
- Show analytics: phishing percentage, accuracy, confidence distribution
- Real-time statistics and visualizations

### 🧪 Email Simulation Mode
- Test with custom email text input
- Live detection and explanation
- Example emails for testing

### ⚙️ Admin/Analyst Module
- Manage trusted senders/domains
- View logs of quarantined or flagged messages
- Analytics and reporting

### 🔍 Explainability
- Display why an email was flagged
- Show keywords, sender, or suspicious links
- Feature extraction and analysis
- Zero-Trust reasoning

## 📁 Project Structure

```
ZeroTrust-AI-Email-Firewall/
│
├── backend/
│   ├── app.py                 # FastAPI main application
│   ├── model/
│   │   ├── train_model.py     # Model training module
│   │   └── phishing_model.pkl # Trained model (generated)
│   ├── utils/
│   │   ├── preprocess.py      # Email preprocessing
│   │   └── zero_trust_policy.py # Zero-Trust policy engine
│   └── database/
│       ├── init_db.py         # Database initialization
│       └── firewall.db        # SQLite database (generated)
│
├── frontend/
│   └── streamlit_app.py       # Streamlit frontend
│
├── dataset/
│   └── phishing_dataset.csv   # Training dataset
│
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download

```bash
cd "E:\cybersecurity  phishing email detector\ZeroTrust-AI-Email-Firewall"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### Step 4: Prepare Dataset

Create a CSV file `dataset/phishing_dataset.csv` with the following columns:

- `text`: Email body/content
- `label`: 1 for phishing, 0 for legitimate (safe)

Example:
```csv
text,label
"Congratulations! You won $1,000,000. Click here to claim: http://fake-link.com",1
"Meeting reminder: Tomorrow at 2 PM in conference room",0
"Your account will be suspended. Verify now at http://suspicious.com",1
"Thanks for your order. Your package will arrive tomorrow",0
```

**Note:** You'll need hundreds/thousands of examples for a good model. Use Kaggle's "Phishing Email Detection" dataset or similar.

### Step 5: Initialize Database

```bash
python backend/database/init_db.py
```

### Step 6: Train the Model

```bash
python backend/model/train_model.py --dataset dataset/phishing_dataset.csv
```

Or use the API endpoint (after starting the server):

```bash
curl -X POST "http://localhost:8000/train-model"
```

## 💻 Usage

### Start the Backend API

```bash
cd ZeroTrust-AI-Email-Firewall
python backend/app.py
```

Or using uvicorn:

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base:** `http://localhost:8000`
- **Interactive Docs:** `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs:** `http://localhost:8000/redoc` (ReDoc)

### Start the Frontend

```bash
cd ZeroTrust-AI-Email-Firewall
streamlit run frontend/streamlit_app.py
```

The frontend will be available at:
- **Frontend:** `http://localhost:8501`

## 🔌 API Endpoints

### Email Scanning

**POST `/scan-email`**
- Scan a single email for phishing
- Request body: `{ "email_text": "...", "sender": "...", "recipient": "...", "subject": "..." }`
- Response: Prediction, confidence, trust score, decision, and action

**POST `/scan-batch`**
- Scan multiple emails in batch
- Request body: `{ "emails": [...] }`
- Response: List of scan results

### Zero-Trust Policy

**POST `/add-trusted-domain`**
- Add a domain to the trusted list
- Request body: `{ "domain": "example.com" }`

**DELETE `/remove-trusted-domain/{domain}`**
- Remove a domain from the trusted list

**GET `/trusted-domains`**
- Get list of all trusted domains

### Logs and Analytics

**GET `/logs`**
- Get email logs
- Query parameters: `limit`, `decision` (Safe, Suspicious, Phishing)

**GET `/analytics`**
- Get analytics data
- Response: Total emails, phishing percentage, average confidence, etc.

### Model Management

**POST `/train-model`**
- Train the phishing email detection model
- Query parameter: `perform_grid_search` (default: true)

### Health Check

**GET `/health`**
- Check API health and model status

## 📊 Features Explained

### AI Email Classification

The system uses:
- **TF-IDF Vectorization** with n-grams (1,2)
- **Logistic Regression** with balanced class weights
- **Model Calibration** for reliable probability estimates
- **Hyperparameter Tuning** with GridSearchCV

### Zero-Trust Policy Engine

The Zero-Trust engine evaluates:
1. **Domain Reputation:** Trusted domains, TLD analysis
2. **SPF Check:** Sender Policy Framework verification (simulated)
3. **DKIM Check:** DomainKeys Identified Mail verification (simulated)
4. **AI Confidence:** Machine learning model confidence
5. **Trust Score:** Weighted combination of all factors

**Final Decision:**
- **Safe** (trust_score ≥ 0.7): Allow
- **Suspicious** (0.4 ≤ trust_score < 0.7): Quarantine
- **Phishing** (trust_score < 0.4): Block

### Explainability

The system provides:
- **Reasons for Decision:** Why an email was flagged
- **Feature Extraction:** Keywords, URLs, suspicious patterns
- **Trust Components:** SPF, DKIM, domain reputation breakdown
- **AI Confidence:** Model prediction confidence

## 🧪 Testing

### Test with Example Emails

1. **Phishing Email:**
```
Subject: URGENT: Your Account Will Be Suspended

Dear Customer,
We have detected unusual activity on your account. To prevent suspension, please verify your account immediately:
http://verify-account-now.com/urgent
```

2. **Legitimate Email:**
```
Subject: Meeting Reminder - Project Update

Hi Team,
This is a reminder about our scheduled meeting tomorrow at 2 PM.
See you there!
Best regards,
John Doe
```

### Test API with cURL

```bash
# Scan email
curl -X POST "http://localhost:8000/scan-email" \
     -H "Content-Type: application/json" \
     -d '{
       "email_text": "Subject: URGENT: Your Account Will Be Suspended\n\nDear Customer,\n\nYour account will be suspended...",
       "sender": "noreply@suspicious.com",
       "subject": "URGENT: Your Account Will Be Suspended"
     }'

# Get analytics
curl http://localhost:8000/analytics

# Get logs
curl http://localhost:8000/logs?limit=10
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (or use `.env.example`):

```env
DATASET_PATH=dataset/phishing_dataset.csv
DB_PATH=backend/database/firewall.db
MODEL_PATH=backend/model/calibrated_model.pkl
API_BASE_URL=http://localhost:8000
```

### Model Configuration

Edit `backend/model/train_model.py` to customize:
- Hyperparameter grid
- Model parameters
- Training settings

### Zero-Trust Configuration

Edit `backend/utils/zero_trust_policy.py` to customize:
- Trust score weights
- Domain reputation rules
- SPF/DKIM simulation logic

## 📈 Performance

### Model Metrics

The model is evaluated using:
- **Accuracy:** Overall correctness
- **Precision:** True positives / (True positives + False positives)
- **Recall:** True positives / (True positives + False negatives)
- **F1-Score:** Harmonic mean of precision and recall
- **ROC-AUC:** Area under the ROC curve

### Optimization

- **Lightweight Model:** Fast inference (< 100ms per email)
- **Batch Processing:** Efficient batch scanning
- **Database Indexing:** Fast log retrieval
- **Caching:** Model and preprocessing caching

## 🐛 Troubleshooting

### Issue: "Model not found"

**Solution:** Train the model first:
```bash
python backend/model/train_model.py --dataset dataset/phishing_dataset.csv
```

### Issue: "Database not initialized"

**Solution:** Initialize the database:
```bash
python backend/database/init_db.py
```

### Issue: "spaCy model not found"

**Solution:** Download the spaCy model:
```bash
python -m spacy download en_core_web_sm
```

### Issue: "API not connected"

**Solution:** Ensure the backend is running:
```bash
python backend/app.py
```

### Issue: "Port already in use"

**Solution:** Change the port:
```bash
# For FastAPI
uvicorn backend.app:app --port 8001

# For Streamlit
streamlit run frontend/streamlit_app.py --server.port 8502
```

## 📚 Documentation

### Code Documentation

- All functions have docstrings
- Type hints for better code clarity
- Comprehensive error handling
- Logging for debugging

### API Documentation

- Interactive API docs at `/docs`
- OpenAPI/Swagger specification
- Request/Response models documented

## 🎓 Academic Submission

This project is designed for final-year cybersecurity projects with:
- **Modular Architecture:** Clean, organized code structure
- **Production-Ready:** Error handling, logging, validation
- **Well-Commented:** Extensive comments and docstrings
- **Comprehensive Documentation:** README, API docs, code comments
- **Real-World Practicality:** Usable in production environments

## 🔒 Security Considerations

- **Input Validation:** All inputs are validated
- **SQL Injection Prevention:** Parameterized queries
- **CORS Configuration:** Configure for production
- **Error Handling:** No sensitive information leaked
- **Logging:** Secure logging practices

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

- Kaggle for phishing email datasets
- spaCy for NLP preprocessing
- FastAPI for API framework
- Streamlit for frontend framework
- Scikit-learn for machine learning

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Check the logs for error messages
4. Open an issue on GitHub

---

**Built with ❤️ for cybersecurity education and research**


