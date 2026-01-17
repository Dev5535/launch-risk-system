import re
from .base import BaseScanner

class PIIScanner(BaseScanner):
    def scan(self, target):
        if not target.content: return
        
        content = target.content.decode('utf-8', errors='ignore')
        
        # Simple regexes - can be prone to false positives, handled by "Low/Medium" severity
        patterns = {
            'Email Address': (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'Low'), # Emails are often public
            'US SSN': (r'\b\d{3}-\d{2}-\d{4}\b', 'High'),
            'Credit Card (Potential)': (r'\b(?:\d{4}[- ]?){3}\d{4}\b', 'High')
        }

        for name, (regex, severity) in patterns.items():
            matches = re.findall(regex, content)
            if matches:
                # Dedupe
                count = len(set(matches))
                self.registry.add_finding('Compliance', severity, f"Potential {name} Exposure", f"Found {count} instance(s) of {name}", target.url or target.path)
