import sys
import os
import unittest
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scorer import LaunchScorer
from src.ingestor import ReportIngestor

class TestScorer(unittest.TestCase):
    def test_scoring_logic(self):
        scorer = LaunchScorer()
        
        # Test 1: Perfect Score
        self.assertEqual(scorer.calculate([])['score'], 100)
        self.assertEqual(scorer.calculate([])['status'], "APPROVED")
        
        # Test 2: Critical Blocker
        findings = [{'severity': 'Critical', 'desc': 'Missing DB'}]
        res = scorer.calculate(findings)
        self.assertEqual(res['score'], 0)
        self.assertEqual(res['status'], "BLOCKED")
        
        # Test 3: Multiple Issues
        # Start 100. -10 (High) -10 (High) -5 (Med) = 75
        findings = [
            {'severity': 'High'},
            {'severity': 'High'},
            {'severity': 'Medium'}
        ]
        res = scorer.calculate(findings)
        self.assertEqual(res['score'], 75)
        self.assertEqual(res['status'], "CAUTION") # < 90 is Caution

    def test_ingestion(self):
        ingestor = ReportIngestor()
        # Mocking P1 data
        p1_data = {'delta': {'removed_in_prod': ['file1']}}
        with open('temp_p1.json', 'w') as f: json.dump(p1_data, f)
        
        findings = ingestor.load_report('temp_p1.json', 'p1')
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['severity'], 'Critical')
        
        os.remove('temp_p1.json')

if __name__ == '__main__':
    unittest.main()
