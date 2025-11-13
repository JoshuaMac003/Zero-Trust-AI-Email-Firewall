"""
API Testing Script
Automated tests for the Zero-Trust AI Email Firewall API
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Test Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_test(test_name: str):
    """Print test name."""
    print(f"\n{YELLOW}Testing: {test_name}{RESET}")
    print("-" * 50)


def print_pass(message: str):
    """Print test pass."""
    print(f"{GREEN}✓ PASS: {message}{RESET}")


def print_fail(message: str):
    """Print test fail."""
    print(f"{RED}✗ FAIL: {message}{RESET}")


def test_health_check():
    """Test health check endpoint."""
    print_test("Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Health check successful: {data.get('status')}")
            print(f"  Model loaded: {data.get('model_loaded')}")
            print(f"  Database initialized: {data.get('database_initialized')}")
            return True
        else:
            print_fail(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Health check error: {e}")
        return False


def test_scan_email_phishing():
    """Test scanning a phishing email."""
    print_test("Scan Phishing Email")
    try:
        email_data = {
            "email_text": """Subject: URGENT: Your Account Will Be Suspended

Dear Customer,

We have detected unusual activity on your account. To prevent suspension, please verify your account immediately by clicking the link below:

http://verify-account-now.com/urgent

If you do not verify within 24 hours, your account will be permanently suspended.

Best regards,
Security Team""",
            "sender": "noreply@suspicious.com",
            "subject": "URGENT: Your Account Will Be Suspended"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/scan-email",
            json=email_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_pass("Phishing email scanned successfully")
            print(f"  AI Prediction: {data.get('ai_prediction')}")
            print(f"  AI Confidence: {data.get('ai_confidence'):.2%}")
            print(f"  Trust Score: {data.get('trust_score'):.2%}")
            print(f"  Zero-Trust Decision: {data.get('zero_trust_decision')}")
            print(f"  Action: {data.get('action')}")
            
            # Verify it's classified as phishing
            if data.get('zero_trust_decision') in ['Phishing', 'Suspicious']:
                print_pass("Email correctly classified as phishing/suspicious")
                return True
            else:
                print_fail("Email not classified as phishing")
                return False
        else:
            print_fail(f"Scan failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_fail(f"Scan error: {e}")
        return False


def test_scan_email_safe():
    """Test scanning a safe email."""
    print_test("Scan Safe Email")
    try:
        email_data = {
            "email_text": """Subject: Meeting Reminder - Project Update

Hi Team,

This is a reminder about our scheduled meeting tomorrow at 2 PM to discuss the project update.

Please review the attached documents before the meeting.

See you there!

Best regards,
John Doe
Project Manager""",
            "sender": "john.doe@company.com",
            "subject": "Meeting Reminder - Project Update"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/scan-email",
            json=email_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_pass("Safe email scanned successfully")
            print(f"  AI Prediction: {data.get('ai_prediction')}")
            print(f"  AI Confidence: {data.get('ai_confidence'):.2%}")
            print(f"  Trust Score: {data.get('trust_score'):.2%}")
            print(f"  Zero-Trust Decision: {data.get('zero_trust_decision')}")
            print(f"  Action: {data.get('action')}")
            
            # Verify it's classified as safe
            if data.get('zero_trust_decision') == 'Safe':
                print_pass("Email correctly classified as safe")
                return True
            else:
                print_fail(f"Email classified as {data.get('zero_trust_decision')}")
                return False
        else:
            print_fail(f"Scan failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_fail(f"Scan error: {e}")
        return False


def test_batch_scan():
    """Test batch email scanning."""
    print_test("Batch Email Scan")
    try:
        emails = [
            {
                "email_text": "Subject: Test 1\n\nThis is test email 1.",
                "sender": "test1@example.com",
                "subject": "Test 1"
            },
            {
                "email_text": "Subject: Test 2\n\nThis is test email 2.",
                "sender": "test2@example.com",
                "subject": "Test 2"
            }
        ]
        
        response = requests.post(
            f"{API_BASE_URL}/scan-batch",
            json={"emails": emails},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Batch scan successful: {data.get('total_processed')} emails processed")
            print(f"  Blocked: {data.get('total_blocked')}")
            print(f"  Quarantined: {data.get('total_quarantined')}")
            return True
        else:
            print_fail(f"Batch scan failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_fail(f"Batch scan error: {e}")
        return False


def test_trusted_domains():
    """Test trusted domains management."""
    print_test("Trusted Domains Management")
    try:
        # Add trusted domain
        response = requests.post(
            f"{API_BASE_URL}/add-trusted-domain",
            json={"domain": "test.com", "added_by": "admin"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass("Trusted domain added successfully")
            else:
                print_fail("Failed to add trusted domain")
                return False
        else:
            print_fail(f"Add domain failed: {response.status_code}")
            return False
        
        # Get trusted domains
        response = requests.get(f"{API_BASE_URL}/trusted-domains", timeout=5)
        if response.status_code == 200:
            data = response.json()
            domains = data.get('trusted_domains', [])
            if 'test.com' in domains:
                print_pass("Trusted domain retrieved successfully")
            else:
                print_fail("Trusted domain not in list")
                return False
        else:
            print_fail(f"Get domains failed: {response.status_code}")
            return False
        
        # Remove trusted domain
        response = requests.delete(
            f"{API_BASE_URL}/remove-trusted-domain/test.com",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_pass("Trusted domain removed successfully")
                return True
            else:
                print_fail("Failed to remove trusted domain")
                return False
        else:
            print_fail(f"Remove domain failed: {response.status_code}")
            return False
            
    except Exception as e:
        print_fail(f"Trusted domains error: {e}")
        return False


def test_logs():
    """Test logs endpoint."""
    print_test("Email Logs")
    try:
        response = requests.get(f"{API_BASE_URL}/logs?limit=10", timeout=5)
        if response.status_code == 200:
            data = response.json()
            logs = data.get('logs', [])
            print_pass(f"Logs retrieved successfully: {len(logs)} logs")
            return True
        else:
            print_fail(f"Logs failed: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Logs error: {e}")
        return False


def test_analytics():
    """Test analytics endpoint."""
    print_test("Analytics")
    try:
        response = requests.get(f"{API_BASE_URL}/analytics", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_pass("Analytics retrieved successfully")
            print(f"  Total Emails: {data.get('total_emails')}")
            print(f"  Phishing Emails: {data.get('phishing_emails')}")
            print(f"  Safe Emails: {data.get('safe_emails')}")
            print(f"  Phishing Percentage: {data.get('phishing_percentage'):.2f}%")
            return True
        else:
            print_fail(f"Analytics failed: {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Analytics error: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print(f"\n{YELLOW}{'='*50}{RESET}")
    print(f"{YELLOW}Zero-Trust AI Email Firewall - API Tests{RESET}")
    print(f"{YELLOW}{'='*50}{RESET}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Scan Phishing Email", test_scan_email_phishing),
        ("Scan Safe Email", test_scan_email_safe),
        ("Batch Scan", test_batch_scan),
        ("Trusted Domains", test_trusted_domains),
        ("Logs", test_logs),
        ("Analytics", test_analytics),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            time.sleep(1)  # Small delay between tests
        except Exception as e:
            print_fail(f"{test_name} exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print(f"\n{YELLOW}{'='*50}{RESET}")
    print(f"{YELLOW}Test Summary{RESET}")
    print(f"{YELLOW}{'='*50}{RESET}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"{GREEN}All tests passed! ✓{RESET}")
    else:
        print(f"{RED}Some tests failed. Please check the output above.{RESET}")
    
    return passed == total


if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"{RED}API is not running. Please start the backend first.{RESET}")
            print(f"Run: python start_backend.py")
            exit(1)
    except Exception as e:
        print(f"{RED}Cannot connect to API. Please start the backend first.{RESET}")
        print(f"Run: python start_backend.py")
        print(f"Error: {e}")
        exit(1)
    
    # Run tests
    success = run_all_tests()
    exit(0 if success else 1)


