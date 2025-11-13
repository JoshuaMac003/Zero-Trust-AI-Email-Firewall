# 🧪 How to Test the Zero-Trust AI Email Firewall

Quick guide to test if the system is working correctly.

## 🚀 Quick Start Testing (5 Minutes)

### Step 1: Start the Backend

```bash
cd ZeroTrust-AI-Email-Firewall
python start_backend.py
```

**Wait for:** `INFO: Application startup complete.`

### Step 2: Test Health Check (New Terminal)

```bash
curl http://localhost:8000/health
```

**Expected:** JSON response with `"status": "healthy"`

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

**Expected:** JSON response with prediction, confidence, and trust score

### Step 4: Start the Frontend (New Terminal)

```bash
cd ZeroTrust-AI-Email-Firewall
python start_frontend.py
```

### Step 5: Test in Browser

1. Open `http://localhost:8501`
2. Go to "Email Scanner"
3. Paste a test email
4. Click "Scan Email"
5. Verify results are displayed

## 🧪 Automated Testing

### Run Automated Tests

```bash
cd ZeroTrust-AI-Email-Firewall
python test_api.py
```

**Expected:** All tests pass (✓)

## 📧 Test Emails

### Phishing Email (Should be Blocked)

```
Subject: URGENT: Your Account Will Be Suspended

Dear Customer,
We have detected unusual activity on your account. To prevent suspension, please verify your account immediately:
http://verify-account-now.com/urgent
```

**Expected Result:**
- Decision: **Phishing**
- Action: **Block**
- Confidence: **High (> 0.7)**

### Safe Email (Should be Allowed)

```
Subject: Meeting Reminder - Project Update

Hi Team,
This is a reminder about our scheduled meeting tomorrow at 2 PM.
See you there!
Best regards,
John Doe
```

**Expected Result:**
- Decision: **Safe**
- Action: **Allow**
- Confidence: **High (> 0.7)**

## 🔍 Manual Testing Checklist

### Backend Tests

- [ ] Backend starts without errors
- [ ] Health endpoint returns "healthy"
- [ ] Email scanning works
- [ ] Batch scanning works
- [ ] Trusted domains management works
- [ ] Logs are retrieved
- [ ] Analytics are calculated

### Frontend Tests

- [ ] Frontend starts without errors
- [ ] Dashboard displays metrics
- [ ] Email scanner works
- [ ] Batch upload works
- [ ] Analytics are displayed
- [ ] Logs are displayed
- [ ] Admin panel works

## 🎯 Expected Results

### Successful Test Results

1. **Health Check:**
   - Status: "healthy"
   - Model loaded: true
   - Database initialized: true

2. **Email Scanning:**
   - Returns prediction (Safe/Suspicious/Phishing)
   - Returns confidence score (0-1)
   - Returns trust score (0-1)
   - Returns action (Allow/Quarantine/Block)
   - Returns reasons for decision

3. **Frontend:**
   - Dashboard shows metrics
   - Email scanner displays results
   - Charts render correctly
   - Logs are displayed

## 🐛 Troubleshooting

### Issue: "API is not running"

**Solution:**
```bash
python start_backend.py
```

### Issue: "Model not loaded"

**Solution:**
```bash
python backend/model/train_model.py
```

### Issue: "Database not initialized"

**Solution:**
```bash
python backend/database/init_db.py
```

### Issue: "Frontend not connecting"

**Solution:**
1. Check if backend is running
2. Verify API URL in frontend
3. Check browser console for errors

## 📝 Test Results

After testing, you should see:

- ✅ Backend responds to requests
- ✅ Email scanning returns predictions
- ✅ Zero-Trust decisions are made
- ✅ Logs are stored in database
- ✅ Analytics are calculated
- ✅ Frontend displays results
- ✅ Admin panel manages domains

## 🎉 Success!

If all tests pass, the system is working correctly!

For detailed testing, see `TESTING_GUIDE.md`.


