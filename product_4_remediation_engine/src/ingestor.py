import json
import os

class ReportIngestor:
    def __init__(self):
        pass

    def load_report(self, file_path, product_type):
        if not os.path.exists(file_path):
            print(f"Warning: Report file not found: {file_path}")
            return []
            
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {file_path}")
                return []

        if product_type == 'p1':
            return self._normalize_p1(data)
        elif product_type == 'p2':
            return self._normalize_p2(data)
        elif product_type == 'p3':
            return self._normalize_p3(data)
        else:
            print(f"Unknown product type: {product_type}")
            return []

    def _normalize_p1(self, data):
        """Normalize Digital Twin Auditor (Drift) Report"""
        findings = []
        # Expecting structure from P1 Analyzer
        # It might be nested under 'delta' or root
        
        delta = data.get('delta', data) # Fallback if structure varies
        
        for file in delta.get('removed_in_prod', []): # Assuming 'removed' means missing in prod
             findings.append({
                 'id': 'DRIFT-FILE-MISSING',
                 'context': {'staging_path': file, 'prod_path': file.replace('staging', 'prod')} # simplified logic
             })
             
        for file in delta.get('modified', []):
            findings.append({
                'id': 'DRIFT-CONTENT-MISMATCH',
                'context': {'staging_path': file, 'prod_path': file.replace('staging', 'prod')}
            })
            
        return findings

    def _normalize_p2(self, data):
        """Normalize Risk Audit Engine Report"""
        findings = []
        results = data.get('results', {})
        
        # SEO
        seo = results.get('seo', {})
        for url in seo.get('missing_title', []):
            findings.append({
                'id': 'SEO-MISSING-TITLE',
                'context': {'url': url}
            })
            
        # Security
        sec = results.get('security', {})
        for secret in sec.get('secrets', []):
            # secret: {'type': 'AWS Key', 'file': '...', 'line': 1, 'content': '...'}
            if 'AWS' in secret.get('type', ''):
                findings.append({
                    'id': 'SEC-AWS-KEY',
                    'context': {
                        'file_path': secret.get('file'),
                        'match_content': secret.get('content')
                    }
                })
        
        # PII
        pii = results.get('pii', {})
        for item in pii.get('findings', []):
            if 'Email' in item.get('type', ''):
                 findings.append({
                    'id': 'PII-EMAIL-EXPOSED',
                    'context': {
                        'match_content': item.get('content')
                    }
                })

        return findings

    def _normalize_p3(self, data):
        """Normalize Compliance Mapper Report"""
        findings = []
        results = data.get('results', {})
        checklist = results.get('checklist', [])
        
        for item in checklist:
            # Item: {'id': 'GDPR-1', 'title': ..., 'priority': ...}
            findings.append({
                'id': item.get('id'),
                'context': {
                    'regulation': item.get('regulation'),
                    'priority': item.get('priority')
                }
            })
            
        return findings
