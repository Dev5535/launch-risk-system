import os
import sys
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, 'tests', 'test_map.json')

def run_test(name, args, expected_regs):
    print(f"\nRunning Test: {name}")
    
    cmd = [sys.executable, os.path.join(BASE_DIR, 'src', 'main.py')] + args + ['--output', OUTPUT_FILE]
    
    # print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Command Failed")
        print(result.stderr)
        return False

    if not os.path.exists(OUTPUT_FILE):
        print("❌ Output file not found")
        return False

    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)
        
    regs = data['results']['regulations']
    checklist = data['results']['checklist']
    
    # Check if expected regulations are present
    missing = [r for r in expected_regs if r not in regs]
    
    print(f"  Found Regulations: {regs}")
    print(f"  Checklist Items: {len(checklist)}")
    
    if missing:
        print(f"❌ FAILED. Missing expected regs: {missing}")
        return False
    else:
        print("✅ PASSED")
        return True

def main():
    # Test 1: Healthcare in US (HIPAA)
    t1 = run_test(
        "US Healthcare",
        ['--industry', 'Healthcare', '--region', 'US', '--data-types', 'Health'],
        ['HIPAA']
    )

    # Test 2: EU SaaS handling PII (GDPR + SOC2)
    t2 = run_test(
        "EU SaaS PII",
        ['--industry', 'SaaS', '--region', 'EU', '--data-types', 'PII'],
        ['GDPR', 'SOC2']
    )

    # Test 3: Global Finance (ISO27001 + GDPR)
    t3 = run_test(
        "Global Finance",
        ['--industry', 'Finance', '--region', 'Global', '--data-types', 'Financial'],
        ['ISO27001', 'GDPR']
    )

    if t1 and t2 and t3:
        print("\n🎉 ALL TESTS PASSED")
    else:
        print("\n💥 SOME TESTS FAILED")

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(OUTPUT_FILE)):
        os.makedirs(os.path.dirname(OUTPUT_FILE))
    main()
