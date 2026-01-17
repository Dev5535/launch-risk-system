import sys
import os
import json
import unittest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingestor import ReportIngestor
from src.engine import RemediationEngine

class TestRemediation(unittest.TestCase):
    def setUp(self):
        # Create dummy reports
        self.p1_data = {
            "delta": {
                "removed_in_prod": ["/var/www/html/config.php"],
                "modified": ["/etc/nginx/nginx.conf"]
            }
        }
        self.p2_data = {
            "results": {
                "seo": {"missing_title": ["http://localhost/about"]},
                "security": {"secrets": [{"type": "AWS Key", "file": "src/aws.js", "content": "AKIA123456"}]}
            }
        }
        self.p3_data = {
            "results": {
                "checklist": [
                    {"id": "GDPR-1", "priority": "High", "regulation": "GDPR"},
                    {"id": "HIPAA-1", "priority": "Critical", "regulation": "HIPAA"}
                ]
            }
        }
        
        with open('test_p1.json', 'w') as f: json.dump(self.p1_data, f)
        with open('test_p2.json', 'w') as f: json.dump(self.p2_data, f)
        with open('test_p3.json', 'w') as f: json.dump(self.p3_data, f)

    def tearDown(self):
        # Cleanup
        for f in ['test_p1.json', 'test_p2.json', 'test_p3.json', 'test_runbook.md']:
            if os.path.exists(f):
                os.remove(f)

    def test_full_flow(self):
        ingestor = ReportIngestor()
        findings = []
        findings.extend(ingestor.load_report('test_p1.json', 'p1'))
        findings.extend(ingestor.load_report('test_p2.json', 'p2'))
        findings.extend(ingestor.load_report('test_p3.json', 'p3'))
        
        self.assertEqual(len(findings), 6) # 2 from P1, 2 from P2, 2 from P3
        
        # Check IDs
        ids = [f['id'] for f in findings]
        self.assertIn('DRIFT-FILE-MISSING', ids)
        self.assertIn('SEO-MISSING-TITLE', ids)
        self.assertIn('GDPR-1', ids)
        
        # Run Engine
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        solutions_path = os.path.join(base_dir, 'src', 'data', 'solutions.yaml')
        
        engine = RemediationEngine(solutions_path)
        runbook = engine.generate_runbook(findings)
        
        # Check Content
        self.assertIn("# 🛠️ FIX-IT-YOURSELF REMEDIATION RUNBOOK", runbook)
        self.assertIn("cp /var/www/html/config.php", runbook) # P1 Template injection
        self.assertIn("AKIA123456", runbook) # P2 Context injection
        self.assertIn("Implement 'Right to be Forgotten'", runbook) # P3 Title

        with open('test_runbook.md', 'w', encoding='utf-8') as f:
            f.write(runbook)
            
        print("\nTest Runbook Generated Successfully!")

if __name__ == '__main__':
    unittest.main()
