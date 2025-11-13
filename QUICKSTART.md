# 🚀 Quick Start Guide

Get up and running with Zero-Trust AI Email Firewall in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Step 2: Initialize Database

```bash
python backend/database/init_db.py
```

## Step 3: Prepare Dataset

Create `dataset/phishing_dataset.csv` with columns: `text`, `label`

Example:
```csv
text,label
"Congratulations! You won $1,000,000. Click here...",1
"Meeting reminder: Tomorrow at 2 PM",0
```

## Step 4: Train Model

```bash
python backend/model/train_model.py --dataset dataset/phishing_dataset.csv
```

## Step 5: Start Backend

```bash
python backend/app.py
```

API will be available at: `http://localhost:8000/docs`

## Step 6: Start Frontend

```bash
streamlit run frontend/streamlit_app.py
```

Frontend will be available at: `http://localhost:8501`

## 🎉 Done!

You're ready to scan emails! Try the example emails in the frontend or test the API directly.

## 📝 Notes

- Ensure the backend is running before starting the frontend
- The model must be trained before scanning emails
- Use the interactive API docs at `/docs` for testing

## 🐛 Troubleshooting

**Model not found?**
- Train the model: `python backend/model/train_model.py`

**Database error?**
- Initialize database: `python backend/database/init_db.py`

**API not connecting?**
- Ensure backend is running: `python backend/app.py`

## 📚 More Information

See `README.md` for detailed documentation.


