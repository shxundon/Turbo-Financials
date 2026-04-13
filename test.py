"""
Test script to verify Turbo Financials Form Handler application
Run this after starting app.py to test all endpoints
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f'{BASE_URL}/api/health')
        print(f"OK Health check: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"FAIL Health check failed: {e}")

def test_tax_submission():
    """Test tax form submission"""
    print("\nTesting tax form submission...")
    try:
        data = {
            'full-name': 'Test User',
            'date-of-birth': '1990-01-01',
            'ssn': '123-45-6789',
            'email': 'test@example.com',
            'address': '123 Main St, City, ST 12345',
            'state-residence': 'ca',
            'filing-status': 'single',
            'w2-income': '50000',
            'dependents': '0',
            'total-withholding': '5000',
            'refund-method': 'direct-deposit'
        }
        response = requests.post(f'{BASE_URL}/api/submit/tax-info', data=data, allow_redirects=False)
        print(f"OK Tax submission: {response.status_code}")
        if response.status_code == 302:
            print(f"  Redirects to: {response.headers.get('Location')}")
        else:
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"FAIL Tax submission failed: {e}")

def test_bank_submission():
    """Test bank form submission"""
    print("\nTesting bank form submission...")
    try:
        data = {
            'acc-name': 'Test Bank User',
            'bank-name': 'Chase Bank',
            'acc-type': 'checking',
            'routing-number': '123456789',
            'account-number': '9876543210',
            'confirm-account': '9876543210'
        }
        response = requests.post(f'{BASE_URL}/api/submit/bank-info', data=data, allow_redirects=False)
        print(f"OK Bank submission: {response.status_code}")
        if response.status_code == 302:
            print(f"  Redirects to: {response.headers.get('Location')}")
        else:
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"FAIL Bank submission failed: {e}")

def test_direct_deposit_submission():
    """Test direct deposit form submission"""
    print("\nTesting direct deposit submission...")
    try:
        data = {
            'emp-name': 'Test Employee',
            'emp-id': 'EMP12345',
            'bank-name': 'Wells Fargo',
            'routing-number': '987654321',
            'account-number': '1234567890',
            'acc-type': 'savings',
            'deposit-amount': '100',
            'authorize': 'on'
        }
        response = requests.post(f'{BASE_URL}/api/submit/direct-deposit', data=data, allow_redirects=False)
        print(f"OK Direct deposit submission: {response.status_code}")
        if response.status_code == 302:
            print(f"  Redirects to: {response.headers.get('Location')}")
        else:
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"FAIL Direct deposit submission failed: {e}")

def test_admin_endpoints():
    """Test admin endpoints"""
    print("\nTesting admin endpoints...")
    
    endpoints = [
        '/admin/summary',
        '/admin/submissions',
        '/admin/submissions/tax_information',
        '/admin/submissions/bank_information',
        '/admin/submissions/direct_deposit'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'{BASE_URL}{endpoint}')
            response.json()
            print(f"OK {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"FAIL {endpoint}: {e}")

def main():
    print("="*60)
    print("Turbo Financials Form Handler - Endpoint Tests")
    print("="*60)
    
    print("\nMake sure the Flask app is running!")
    print("In another terminal, run: python app.py")
    print()
    
    input("Press Enter to start tests...")
    
    try:
        # Test connectivity
        print("\nChecking server connectivity...")
        requests.get(BASE_URL, timeout=2)
        print("✓ Server is running")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server")
        print(f"Make sure Flask app is running at {BASE_URL}")
        return
    
    # Run tests
    test_health()
    test_tax_submission()
    test_bank_submission()
    test_direct_deposit_submission()
    test_admin_endpoints()
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
    print("\nNext steps:")
    print("1. Check logs/submissions/ for saved data")
    print("2. Run: python manage.py summary")
    print("3. Run: python manage.py export --csv")
    print("="*60)

if __name__ == '__main__':
    main()
