# 🧪 Testing Guide - Zero-Trust AI Email Firewall

Complete guide to test and verify the Zero-Trust AI Email Firewall is working correctly.

## 📋 Prerequisites

Before testing, ensure:
- ✅ Dependencies are installed: `pip install -r requirements.txt`
- ✅ spaCy model is downloaded: `python -m spacy download en_core_web_sm`
- ✅ Database is initialized: `python backend/database/init_db.py`
- ✅ Dataset exists: `dataset/phishing_dataset.csv`
- ✅ Model is trained: `python backend/model/train_model.py`

## 🚀 Quick Test (5 Minutes)

### Step 1: Start the Backend

```bash
cd ZeroTrust-AI-Email-Firewall
python start_backend.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify:** Open `http://localhost:8000/docs` in your browser - you should see the Swagger UI.

### Step 2: Test Health Endpoint

Open a new terminal and run:

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

### Step 3: Test Email Scanning

```bash
curl -X POST "http://localhost:8000/scan-email" \
     -H "Content-Type: application/json" \
     -d '{
       "email_text": "Subject: URGENT: Your Account Will Be Suspended\n\nDear Customer,\n\nYour account will be suspended. Click here to verify: http://fake-link.com",
       "sender": "noreply@suspicious.com",
       "subject": "URGENT: Your Account Will Be Suspended"
     }'
```

**Expected Response:**
```json
{
  "log_id": 1,
  "ai_prediction": "Phishing",
  "ai_confidence": 0.95,
  "trust_score": 0.25,
  "zero_trust_decision": "Phishing",
  "action": "Block",
  "domain": "suspicious.com",
  "spf_check": false,
  "dkim_check": false,
  "reasons": ["AI prediction: Phishing", "SPF check failed", "DKIM check failed"],
  "is_quarantined": false,
  "is_blocked": true,
  "timestamp": "2025-11-13T..."
}
```

### Step 4: Start the Frontend

Open a new terminal:

```bash
cd ZeroTrust-AI-Email-Firewall
python start_frontend.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Step 5: Test in Frontend

1. Open `http://localhost:8501` in your browser
2. Click "Load Model" in the sidebar (if needed)
3. Go to "Email Scanner" page
4. Paste a test email
5. Click "Scan Email"
6. Verify results are displayed

## 📧 Test Emails

### Test Case 1: Phishing Email

**Email:**
```
Subject: URGENT: Your Account Will Be Suspended

Dear Customer,

We have detected unusual activity on your account. To prevent suspension, please verify your account immediately by clicking the link below:

http://verify-account-now.com/urgent

If you do not verify within 24 hours, your account will be permanently suspended.

Best regards,
Security Team
```

**Expected Result:**
- AI Prediction: **Phishing**
- AI Confidence: **> 0.7** (high)
- Trust Score: **< 0.4** (low)
- Zero-Trust Decision: **Phishing**
- Action: **Block**
- Reasons: Should include "AI prediction: Phishing", "SPF check failed", etc.

### Test Case 2: Suspicious Email

**Email:**
```
Subject: Verify Your Account

Hello,

Please verify your account by clicking this link:
http://bit.ly/verify-account

Thank you,
Support Team
```

**Expected Result:**
- AI Prediction: **Suspicious** or **Phishing**
- AI Confidence: **0.4 - 0.7** (medium)
- Trust Score: **0.4 - 0.7** (medium)
- Zero-Trust Decision: **Suspicious**
- Action: **Quarantine**
- Reasons: Should include suspicious keywords or domain

### Test Case 3: Legitimate Email

**Email:**
```
Subject: Meeting Reminder - Project Update

Hi Team,

This is a reminder about our scheduled meeting tomorrow at 2 PM to discuss the project update.

Please review the attached documents before the meeting.

See you there!

Best regards,
John Doe
Project Manager
```

**Expected Result:**
- AI Prediction: **Safe**
- AI Confidence: **> 0.7** (high)
- Trust Score: **> 0.7** (high)
- Zero-Trust Decision: **Safe**
- Action: **Allow**
- Reasons: Should include "AI prediction: Safe", "SPF check passed", etc.

### Test Case 4: Email with Trusted Domain

**Email:**
```
Subject: Welcome to Our Service

Hello,

Welcome to our service! We're excited to have you on board.

Best regards,
Team
```

**Steps:**
1. Add sender domain to trusted list via API or Admin Panel
2. Scan the email
3. Verify trusted domain affects the decision

**Expected Result:**
- Domain should be in trusted list
- Trust score should be higher
- Decision may be more lenient

## 🔍 API Testing

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

**Verify:**
- Status: "healthy"
- Model loaded: true
- Database initialized: true

### Test 2: Scan Single Email

```bash
curl -X POST "http://localhost:8000/scan-email" \
     -H "Content-Type: application/json" \
     -d '{
       "email_text": "Subject: Test\n\nThis is a test email.",
       "sender": "test@example.com",
       "subject": "Test"
     }'
```

**Verify:**
- Response contains: `ai_prediction`, `ai_confidence`, `trust_score`, `zero_trust_decision`, `action`
- Log ID is returned
- Timestamp is included

### Test 3: Scan Batch Emails

```bash
curl -X POST "http://localhost:8000/scan-batch" \
     -H "Content-Type: application/json" \
     -d '{
       "emails": [
         {
           "email_text": "Subject: Test 1\n\nThis is test email 1.",
           "sender": "test1@example.com"
         },
         {
           "email_text": "Subject: Test 2\n\nThis is test email 2.",
           "sender": "test2@example.com"
         }
       ]
     }'
```

**Verify:**
- Response contains: `results` array
- `total_processed` matches number of emails
- Each result has prediction and confidence

### Test 4: Add Trusted Domain

```bash
curl -X POST "http://localhost:8000/add-trusted-domain" \
     -H "Content-Type: application/json" \
     -d '{
       "domain": "example.com",
       "added_by": "admin"
     }'
```

**Verify:**
- Response: `{"success": true, "message": "Domain example.com added to trusted list"}`
- Domain appears in trusted domains list

### Test 5: Get Trusted Domains

```bash
curl http://localhost:8000/trusted-domains
```

**Verify:**
- Response contains: `trusted_domains` array
- Previously added domains are listed

### Test 6: Get Logs

```bash
curl http://localhost:8000/logs?limit=10
```

**Verify:**
- Response contains: `logs` array
- Logs include scanned emails
- Logs are sorted by timestamp (newest first)

### Test 7: Get Analytics

```bash
curl http://localhost:8000/analytics
```

**Verify:**
- Response contains: `total_emails`, `phishing_emails`, `safe_emails`, etc.
- Statistics match scanned emails
- Percentages are calculated correctly

## 🎨 Frontend Testing

### Test 1: Dashboard

1. Open `http://localhost:8501`
2. Navigate to "Dashboard"
3. **Verify:**
   - Metrics are displayed (Total Emails, Phishing, Blocked, etc.)
   - Charts are rendered
   - Statistics are accurate

### Test 2: Email Scanner - Single Email

1. Navigate to "Email Scanner"
2. Select "Single Email" mode
3. Enter test email text
4. Click "Scan Email"
5. **Verify:**
   - Results are displayed
   - Prediction box shows correct color (green/yellow/red)
   - Confidence and trust scores are shown
   - Explainability section shows reasons
   - Zero-Trust analysis is displayed

### Test 3: Email Scanner - Batch Upload

1. Create a CSV file with test emails:
   ```csv
   text,label
   "Subject: Test 1\n\nThis is test email 1.",1
   "Subject: Test 2\n\nThis is test email 2.",0
   ```
2. Navigate to "Email Scanner"
3. Select "Batch Upload (CSV)" mode
4. Upload the CSV file
5. Click "Scan Batch"
6. **Verify:**
   - Results are displayed in a table
   - Download button is available
   - All emails are processed

### Test 4: Analytics

1. Navigate to "Analytics"
2. **Verify:**
   - Metrics are displayed
   - Charts are rendered
   - Statistics are accurate
   - Average scores are shown

### Test 5: Logs

1. Navigate to "Logs"
2. **Verify:**
   - Logs are displayed in a table
   - Filters work (limit, decision)
   - Download button is available
   - Logs are sorted by timestamp

### Test 6: Admin Panel

1. Navigate to "Admin Panel"
2. **Verify:**
   - Trusted domains are listed
   - Add domain functionality works
   - Remove domain functionality works
   - Changes are reflected immediately

## 🔬 Advanced Testing

### Test 1: Model Accuracy

1. Prepare a test dataset with known labels
2. Scan each email via API
3. Compare predictions with actual labels
4. Calculate accuracy, precision, recall, F1-score

**Expected:**
- Accuracy: > 0.85 (85%)
- Precision: > 0.80
- Recall: > 0.80
- F1-Score: > 0.80

### Test 2: Zero-Trust Policy

1. Test with trusted domains
2. Test with suspicious domains
3. Test with blocked domains
4. Verify trust scores reflect domain reputation

**Expected:**
- Trusted domains: Higher trust scores
- Suspicious domains: Lower trust scores
- Blocked domains: Lowest trust scores (0.0)

### Test 3: Performance Testing

1. Scan 100 emails in batch
2. Measure response time
3. Check database performance
4. Monitor memory usage

**Expected:**
- Average response time: < 1 second per email
- Batch processing: < 2 seconds per 10 emails
- Memory usage: < 500MB

### Test 4: Error Handling

1. Test with invalid input (empty email, malformed JSON)
2. Test with missing model
3. Test with database errors
4. Verify error messages are clear

**Expected:**
- Appropriate error messages
- HTTP status codes: 400, 500, 503
- No crashes or exceptions

## 📊 Verification Checklist

### Backend Verification

- [ ] Backend starts without errors
- [ ] Health endpoint returns "healthy"
- [ ] Model loads successfully
- [ ] Database initializes correctly
- [ ] All API endpoints respond
- [ ] Email scanning works
- [ ] Batch scanning works
- [ ] Trusted domains management works
- [ ] Logs are stored correctly
- [ ] Analytics are calculated correctly

### Frontend Verification

- [ ] Frontend starts without errors
- [ ] Dashboard displays metrics
- [ ] Email scanner works
- [ ] Batch upload works
- [ ] Analytics are displayed
- [ ] Logs are displayed
- [ ] Admin panel works
- [ ] Explainability features work
- [ ] Visualizations render correctly
- [ ] Download functionality works

### Model Verification

- [ ] Model trains successfully
- [ ] Model saves correctly
- [ ] Model loads correctly
- [ ] Predictions are reasonable
- [ ] Confidence scores are between 0 and 1
- [ ] Three-class output works (Safe, Suspicious, Phishing)

### Zero-Trust Verification

- [ ] Domain reputation checking works
- [ ] SPF/DKIM simulation works
- [ ] Trust score calculation works
- [ ] Access control decisions are correct
- [ ] Trusted domains affect decisions
- [ ] Reasons are provided for decisions

## 🐛 Troubleshooting

### Issue: "Model not loaded"

**Solution:**
1. Train the model: `python backend/model/train_model.py`
2. Verify model files exist: `backend/model/*.pkl`
3. Check model path in configuration

### Issue: "Database not initialized"

**Solution:**
1. Initialize database: `python backend/database/init_db.py`
2. Verify database file exists: `backend/database/firewall.db`
3. Check database path in configuration

### Issue: "API not responding"

**Solution:**
1. Check if backend is running: `curl http://localhost:8000/health`
2. Check logs for errors
3. Verify port 8000 is not in use
4. Restart the backend

### Issue: "Frontend not connecting"

**Solution:**
1. Check if backend is running
2. Verify API URL in frontend: `API_BASE_URL = "http://localhost:8000"`
3. Check CORS configuration
4. Check browser console for errors

### Issue: "Predictions are inaccurate"

**Solution:**
1. Verify dataset quality
2. Retrain model with more data
3. Check model evaluation metrics
4. Adjust hyperparameters

## 📝 Test Results Template

```
Test Date: ___________
Tester: ___________

Backend Tests:
- [ ] Health check: PASS / FAIL
- [ ] Email scanning: PASS / FAIL
- [ ] Batch scanning: PASS / FAIL
- [ ] Trusted domains: PASS / FAIL
- [ ] Logs: PASS / FAIL
- [ ] Analytics: PASS / FAIL

Frontend Tests:
- [ ] Dashboard: PASS / FAIL
- [ ] Email scanner: PASS / FAIL
- [ ] Batch upload: PASS / FAIL
- [ ] Analytics: PASS / FAIL
- [ ] Logs: PASS / FAIL
- [ ] Admin panel: PASS / FAIL

Model Tests:
- [ ] Training: PASS / FAIL
- [ ] Prediction: PASS / FAIL
- [ ] Accuracy: _____%
- [ ] Precision: _____%
- [ ] Recall: _____%
- [ ] F1-Score: _____%

Zero-Trust Tests:
- [ ] Domain reputation: PASS / FAIL
- [ ] SPF/DKIM: PASS / FAIL
- [ ] Trust score: PASS / FAIL
- [ ] Access control: PASS / FAIL

Notes:
___________
___________
```

## ✅ Success Criteria

The system is working correctly if:

1. ✅ Backend starts without errors
2. ✅ Frontend connects to backend
3. ✅ Email scanning returns predictions
4. ✅ Zero-Trust decisions are made
5. ✅ Logs are stored in database
6. ✅ Analytics are calculated correctly
7. ✅ Admin panel manages trusted domains
8. ✅ Explainability features work
9. ✅ Visualizations render correctly
10. ✅ All API endpoints respond

## 🎉 Next Steps

After testing:

1. **Document Results:** Record test results
2. **Fix Issues:** Address any failures
3. **Optimize Performance:** Improve response times
4. **Enhance Features:** Add new functionality
5. **Deploy:** Prepare for production

---

**Happy Testing! 🧪**

For more information, see `README.md` and `QUICKSTART.md`.


