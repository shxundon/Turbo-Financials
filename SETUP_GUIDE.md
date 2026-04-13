# TurboTax Form Handler - Setup & Usage Guide

## 📋 Overview

This Python Flask application logs all form submissions from your TurboTax website to JSON files with timestamps and metadata. It provides:

- ✅ **Form submission logging** - All three forms tracked
- ✅ **Data security** - Sensitive fields masked in logs
- ✅ **Admin panel** - View all submissions via API
- ✅ **JSON storage** - Easy to parse and backup
- ✅ **Timestamps** - Complete audit trail
- ✅ **Error handling** - Comprehensive logging

---

## 🚀 Quick Start

### Windows

1. **Open Terminal/PowerShell** in the `turbo-tax` directory
2. **Run the startup script:**
   ```powershell
   .\run.bat
   ```
3. **Open your browser** and go to: `http://localhost:5000/`

### macOS / Linux

1. **Open Terminal** in the `turbo-tax` directory
2. **Make script executable:**
   ```bash
   chmod +x run.sh
   ```
3. **Run the startup script:**
   ```bash
   ./run.sh
   ```
4. **Open your browser** and go to: `http://localhost:5000/`

---

## 📦 Manual Setup

If the startup scripts don't work:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Access the Application

- **Home Page:** http://localhost:5000/
- **Admin Panel:** http://localhost:5000/admin/summary

---

## 🔍 Admin Endpoints

### View All Submissions
```
http://localhost:5000/admin/submissions
```
Returns JSON of all form submissions

### View Submissions by Type
```
http://localhost:5000/admin/submissions/tax_information
http://localhost:5000/admin/submissions/bank_information
http://localhost:5000/admin/submissions/direct_deposit
```

### View Summary Statistics
```
http://localhost:5000/admin/summary
```
Shows total submissions by type and date range

### Health Check
```
http://localhost:5000/api/health
```

---

## 📂 Data Storage

All submissions are saved in:
```
logs/submissions/
├── tax_information_20260413_101523.json
├── bank_information_20260413_101524.json
├── direct_deposit_20260413_101525.json
└── ...
```

**Format:**
```json
{
  "timestamp": "2026-04-13T10:15:23.456789",
  "form_type": "tax_information",
  "data": {
    "full_name": "John Doe",
    "email": "john@example.com",
    ...
  }
}
```

---

## 🔒 Security Features

### Sensitive Data Masking

The application masks sensitive information:

- **Social Security Numbers** - Not stored (presence only)
- **Full Account Numbers** - Only last 4 digits stored
- **Full Routing Numbers** - Only last 4 digits stored
- **Passwords/Secrets** - Never logged

### Example Bank Submission
```json
{
  "account_holder_name": "John Doe",
  "bank_name": "Chase",
  "routing_number_masked": "4567",
  "account_number_masked": "8901",
  "account_confirmed": true
}
```

---

## 📊 What Gets Logged

### Tax Information Form
- Full name, date of birth, email, address
- Filing status, spouse info
- Income sources (W-2, self-employment, capital gains)
- Dependents and tax credits
- Deductions (mortgage, property taxes, charitable)
- Tax withholding and refund preferences
- **NOT logged:** Full SSN

### Bank Information Form
- Account holder name
- Bank name and account type
- **Masked:** Routing number (last 4 only)
- **Masked:** Account number (last 4 only)
- Account confirmation status

### Direct Deposit Form
- Employee name and ID
- Bank name and account type
- **Masked:** Routing number (last 4 only)
- **Masked:** Account number (last 4 only)
- Deposit amount preference
- Authorization confirmation

---

## 🛠️ Configuration

### Change Port

Edit `app.py` and change the port:
```python
app.run(
    host='0.0.0.0',
    port=8000,  # Change this
    debug=True
)
```

### Change Log Level

Edit `app.py` and modify logging:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG, INFO, WARNING, ERROR
    ...
)
```

---

## 📝 Logging Features

### Console Output
Real-time logs displayed in terminal:
```
2026-04-13 10:15:23,456 - __main__ - INFO - Tax submission from: John Doe
```

### File Logs
Persistent logs stored in `logs/app.log`:
- All form submissions
- Errors and exceptions
- Application startup/shutdown

### Submission Files
Individual JSON files per submission with full data

---

## 🐛 Troubleshooting

### "Python not found"
- Install Python from https://www.python.org/
- Add Python to your system PATH

### "Port 5000 already in use"
- Change the port in `app.py`
- Or kill the process using port 5000

### "Module not found"
- Run `pip install -r requirements.txt`
- Ensure virtual environment is activated

### "Permission denied" (macOS/Linux)
- Run: `chmod +x run.sh`

---

## 📈 Database Export

To export all submissions as CSV:

```python
import json
import csv
from pathlib import Path

submissions = []
for file in Path('logs/submissions').glob('*.json'):
    with open(file) as f:
        submissions.append(json.load(f))

# Export to CSV
with open('export.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[...])
    writer.writeheader()
    for sub in submissions:
        writer.writerow(sub['data'])
```

---

## 🔐 Production Deployment

For production use:

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set Flask to production mode:**
   ```bash
   export FLASK_ENV=production
   ```

3. **Use HTTPS/SSL certificate**

4. **Set up database instead of JSON files**

5. **Implement user authentication**

---

## 📞 Support

For issues or questions:
1. Check the logs in `logs/app.log`
2. Verify all dependencies are installed
3. Ensure port 5000 is available
4. Check file permissions in the `logs` directory

---

**Status:** ✅ Ready for use
**Version:** 1.0.0
**Last Updated:** April 13, 2026
