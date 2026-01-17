import os
import shutil
import json
import sys
import subprocess

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_DIR = os.path.join(BASE_DIR, 'tests', 'test_data')
SOURCE_DIR = os.path.join(TEST_DATA_DIR, 'source')
TARGET_DIR = os.path.join(TEST_DATA_DIR, 'target')

def setup_test_data():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR)
    
    os.makedirs(SOURCE_DIR)
    os.makedirs(TARGET_DIR)

    # 1. Identical File
    with open(os.path.join(SOURCE_DIR, 'logo.png'), 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
    with open(os.path.join(TARGET_DIR, 'logo.png'), 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')

    # 2. Config Drift (Modified)
    with open(os.path.join(SOURCE_DIR, 'config.json'), 'w') as f:
        json.dump({"version": "1.0", "database": "mysql", "timeout": 30}, f)
    with open(os.path.join(TARGET_DIR, 'config.json'), 'w') as f:
        json.dump({"version": "2.0", "database": "postgres", "timeout": 30}, f)

    # 3. Missing in Target
    with open(os.path.join(SOURCE_DIR, 'legacy_script.js'), 'w') as f:
        f.write("console.log('legacy');")

    # 4. New in Target
    with open(os.path.join(TARGET_DIR, 'new_feature.js'), 'w') as f:
        f.write("console.log('new feature');")

    print("Test data created.")

def run_audit():
    main_script = os.path.join(BASE_DIR, 'src', 'main.py')
    output_report = os.path.join(BASE_DIR, 'tests', 'audit_report.json')
    
    cmd = [
        sys.executable, 
        main_script, 
        '--source', SOURCE_DIR, 
        '--target', TARGET_DIR,
        '--output', output_report
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("\n--- STDOUT ---")
    print(result.stdout)
    print("\n--- STDERR ---")
    print(result.stderr)
    
    if result.returncode == 0:
        print("\nAudit command executed successfully.")
        if os.path.exists(output_report):
             print(f"Report generated at {output_report}")
             with open(output_report, 'r') as f:
                 data = json.load(f)
                 summary = data.get('summary', {})
                 print("\nVerification Checks:")
                 print(f"Missing: {summary.get('missing')} (Expected 1)")
                 print(f"New: {summary.get('new')} (Expected 1)")
                 print(f"Modified: {summary.get('modified')} (Expected 1)")
                 
                 if summary.get('missing') == 1 and summary.get('new') == 1 and summary.get('modified') == 1:
                     print("✅ VERIFICATION PASSED")
                 else:
                     print("❌ VERIFICATION FAILED")
    else:
        print("❌ Audit command failed.")

if __name__ == "__main__":
    setup_test_data()
    run_audit()
