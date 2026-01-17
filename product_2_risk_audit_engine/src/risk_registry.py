import json
from datetime import datetime

class RiskRegistry:
    def __init__(self):
        self.findings = []
        self.metrics = {}
        self.stats = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        }

    def add_metric(self, key, value):
        self.metrics[key] = value

    def add_finding(self, category, severity, description, evidence, location=None):
        if severity not in self.stats:
            severity = 'Low' # Fallback
        
        self.findings.append({
            'category': category, # SEO, Security, Stability, Compliance
            'severity': severity,
            'description': description,
            'evidence': evidence,
            'location': location,
            'timestamp': datetime.now().isoformat()
        })
        self.stats[severity] += 1

    def get_report(self):
        return {
            'summary': self.stats,
            'metrics': self.metrics,
            'findings': sorted(self.findings, key=lambda x: self._severity_weight(x['severity']), reverse=True)
        }

    def _severity_weight(self, severity):
        weights = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
        return weights.get(severity, 0)

    def export_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.get_report(), f, indent=2)
