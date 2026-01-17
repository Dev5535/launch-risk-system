import os
import shutil
import json
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_DIR = os.path.join(BASE_DIR, 'tests', 'test_site')

def setup_test_data():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    os.makedirs(TEST_DATA_DIR)

    # 1. SEO Vulnerability (No Title, No H1)
    with open(os.path.join(TEST_DATA_DIR, 'index.html'), 'w') as f:
        f.write("<html><body><p>Just content, no headers</p></body></html>")

    # 2. Security Vulnerability (Exposed Key)
    with open(os.path.join(TEST_DATA_DIR, 'config.js'), 'w') as f:
        f.write("const aws_key = 'AKIAIOSFODNN7EXAMPLE';")

    # 3. Stability (Unpinned Deps)
    with open(os.path.join(TEST_DATA_DIR, 'requirements.txt'), 'w') as f:
        f.write("flask\nrequests==2.0.0")

    # 4. Compliance (PII)
    with open(os.path.join(TEST_DATA_DIR, 'users.txt'), 'w') as f:
        f.write("Contact: admin@example.com")

    print("Test data created.")

def run_audit():
    main_script = os.path.join(BASE_DIR, 'src', 'main.py')
    output_report = os.path.join(BASE_DIR, 'tests', 'risk_report.json')
    
    cmd = [
        sys.executable, 
        main_script, 
        '--target', TEST_DATA_DIR,
        '--output', output_report
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("\n--- STDOUT ---")
    print(result.stdout)
    
    if result.returncode == 0:
        with open(output_report, 'r') as f:
            data = json.load(f)
            stats = data['summary']
            print("\nVerification Results:")
            print(f"Critical: {stats['Critical']} (Expected >= 1)") # AWS Key
            print(f"Medium: {stats['Medium']} (Expected >= 2)") # SEO Title, Unpinned Dep
            print(f"Low: {stats['Low']} (Expected >= 1)") # Email
            
            if stats['Critical'] >= 1 and stats['Medium'] >= 2:
                print("✅ VERIFICATION PASSED")
            else:
                print("❌ VERIFICATION FAILED")
    else:
        print("❌ Command Failed")
        print(result.stderr)

if __name__ == "__main__":
    setup_test_data()
    run_audit()
