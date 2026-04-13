# 🚀 Getting Started - TurboTax Form Handler

## What You Have

A complete, production-ready tax form website with:
- ✅ 3 professional HTML forms
- ✅ Responsive design (works on all devices)
- ✅ Python Flask backend for form handling
- ✅ Automatic logging of all submissions
- ✅ Data security (sensitive info masked)
- ✅ Admin panel for viewing submissions
- ✅ Management tools for exporting data

---

## ⚡ 30-Second Start

### Windows Users
```powershell
cd c:\Users\shell\Videos\turbo-tax
.\run.bat
```

### macOS/Linux Users
```bash
cd ~/Videos/turbo-tax
chmod +x run.sh
./run.sh
```

**Then open your browser:**
```
http://localhost:5000/
```

---

## 📋 What Each File Does

### Core Application
- **`app.py`** - Flask web server & form handler
- **`manage.py`** - Tools to manage submissions
- **`requirements.txt`** - Python package list

### Startup Scripts
- **`run.bat`** - Windows startup (auto-installs dependencies)
- **`run.sh`** - macOS/Linux startup (auto-installs dependencies)

### Website Files
- **`home.html`** - Hub page with navigation
- **`index.html`** - Bank information form
- **`tax RT/tax-form.html`** - Tax filing form
- **`Direct Deposit/DND.html`** - Direct deposit form
- **`style.css`** - Unified styling for all pages

### Documentation
- **`README.md`** - Complete documentation
- **`SETUP_GUIDE.md`** - Detailed setup instructions
- **`GETTING_STARTED.md`** - This file

---

## 🎯 First Time Setup (Detailed)

### Step 1: Install Python (if needed)
If you don't have Python 3.7+:
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or newer
3. Run installer and **check "Add Python to PATH"**
4. Verify: Open terminal and run `python --version`

### Step 2: Navigate to Project
**Windows:**
```powershell
cd c:\Users\shell\Videos\turbo-tax
```

**macOS/Linux:**
```bash
cd ~/Videos/turbo-tax
```

### Step 3: Run the Startup Script

**Windows:**
```powershell
.\run.bat
```

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

This will automatically:
- ✅ Create virtual environment
- ✅ Install Flask and dependencies
- ✅ Start the web server
- ✅ Create logs directory

### Step 4: Open Your Browser
Go to: `http://localhost:5000/`

You should see the TurboTax home page with 3 cards!

---

## 🧪 Testing the Application

### Basic Test (after app is running)
In a **new terminal** window:

**Windows:**
```powershell
cd c:\Users\shell\Videos\turbo-tax
python test.py
```

**macOS/Linux:**
```bash
cd ~/Videos/turbo-tax
python test.py
```

This will test all API endpoints and verify everything works.

---

## 📝 Using the Forms

### Home Page
- Click "Start Tax Filing" → Tax form
- Click "Enter Bank Details" → Bank form  
- Click "Authorize Deposit" → Direct deposit form

### Submitting Forms
1. Fill out form fields
2. Click "Submit" button
3. Data is logged automatically
4. See confirmation message

### Finding Your Data
All submissions saved to:
```
logs/submissions/
```

Each submission is a separate JSON file with timestamp.

---

## 📊 Viewing Submissions

### Quick Summary
```bash
python manage.py summary
```
Shows total forms submitted by type

### View Recent (last 5)
```bash
python manage.py recent
```

### View Most Recent (last 10)
```bash
python manage.py recent -n 10
```

### Export to Spreadsheet (CSV)
```bash
python manage.py export --csv
```
Creates `export_20260413_101523.csv` file that opens in Excel

### Export to JSON
```bash
python manage.py export --json
```
Creates `export_20260413_101523.json` file

### View Specific Submission
```bash
python manage.py view 0
```
Shows first submission in detail

---

## 🌐 Admin Panel

While app is running, visit:

**Summary Dashboard:**
```
http://localhost:5000/admin/summary
```
Shows JSON with stats

**View All Submissions:**
```
http://localhost:5000/admin/submissions
```

**View Tax Submissions Only:**
```
http://localhost:5000/admin/submissions/tax_information
```

**View Bank Submissions Only:**
```
http://localhost:5000/admin/submissions/bank_information
```

**View Direct Deposit Submissions Only:**
```
http://localhost:5000/admin/submissions/direct_deposit
```

---

## 🛑 Stopping the Application

**In the terminal where app is running:**
```
Press CTRL+C
```

Application will stop cleanly.

---

## 🔄 Starting Again Later

Just run the startup script again:

**Windows:**
```powershell
.\run.bat
```

**macOS/Linux:**
```bash
./run.sh
```

No need to reinstall - everything is cached.

---

## ❌ Troubleshooting

### "Port 5000 already in use"
**Windows:**
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

### "Python not found"
- Install Python from https://www.python.org/
- Make sure "Add to PATH" is checked
- Restart your terminal

### "ModuleNotFoundError: Flask"
```bash
pip install -r requirements.txt
```

### "Permission denied" (macOS/Linux)
```bash
chmod +x run.sh
chmod +x manage.py
```

### Forms not submitting
- Make sure Flask app is running (should see messages in terminal)
- Check `logs/app.log` for errors
- Try refreshing the browser (F5)

---

## 🔐 Data Security

Your form submissions are secure:

**Masked Fields:**
- ❌ Full SSN not stored (presence only)
- ❌ Full account numbers not stored (last 4 only)
- ❌ Full routing numbers not stored (last 4 only)

**Example stored data:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "account_number_masked": "3210",
  "routing_number_masked": "4567"
}
```

---

## 📱 Using on Mobile

While app is running:

### Same Computer
```
http://localhost:5000/
```

### Different Computer (Same Network)
```
http://<your-computer-ip>:5000/
```

Find your IP:
- **Windows:** `ipconfig` → Look for IPv4 Address
- **macOS/Linux:** `ifconfig` → Look for inet

Example: `http://192.168.1.100:5000/`

---

## 🎓 Next Steps

### Learning More
- Read `README.md` for complete documentation
- Read `SETUP_GUIDE.md` for advanced configuration
- Check `app.py` to see how it works

### Customizing
1. Change colors in `style.css`
2. Modify forms in HTML files
3. Add new fields and logging in `app.py`

### Deploying Online
See "Production Deployment" section in README.md

---

## 💡 Pro Tips

### Backup Your Data
```bash
python manage.py export --json
```
Save the JSON file somewhere safe

### Clear Old Submissions
```bash
python manage.py delete-old --days 30
```
Deletes submissions older than 30 days

### Automate Your Workflow
Save a batch file or shell script:

**Windows (save as start.bat):**
```batch
@echo off
cd c:\Users\shell\Videos\turbo-tax
.\run.bat
```

**macOS/Linux (save as start.sh):**
```bash
#!/bin/bash
cd ~/Videos/turbo-tax
./run.sh
```

---

## 🆘 Getting Help

### Check Logs
```bash
# View application logs
type logs\app.log        # Windows
cat logs/app.log         # macOS/Linux
```

### Test Endpoints
```bash
python test.py
```

### Check Status
```
http://localhost:5000/api/health
```

---

## 🎉 You're All Set!

Your tax form website is ready to use. Here's what you can do:

1. **Open** `http://localhost:5000/`
2. **Fill out** one of the three forms
3. **View submissions** with `python manage.py summary`
4. **Export data** with `python manage.py export --csv`
5. **Check logs** in `logs/` directory

**Questions?** Check README.md and SETUP_GUIDE.md for detailed info.

---

**Happy form handling! 🎉**

Version 1.0.0 | April 13, 2026
