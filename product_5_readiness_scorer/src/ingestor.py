import json
import os

class ReportIngestor:
    def load_report(self, file_path, product_type):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except:
                return []
        
        if product_type == 'p1': return self._normalize_p1(data)
        if product_type == 'p2': return self._normalize_p2(data)
        if product_type == 'p3': return self._normalize_p3(data)
        return []

    def _normalize_p1(self, data):
        findings = []
        delta = data.get('delta', data)
        for f in delta.get('removed_in_prod', []):
            findings.append({'severity': 'Critical', 'desc': f"Missing File in Prod: {f}"})
        for f in delta.get('modified', []):
            findings.append({'severity': 'High', 'desc': f"Config Drift: {f}"})
        return findings

    def _normalize_p2(self, data):
        findings = []
        # Support new P2 structure (list of findings) or legacy (nested results)
        raw_findings = data.get('findings', [])
        
        # New Structure
        if raw_findings:
            for f in raw_findings:
                findings.append({
                    'severity': f.get('severity', 'Low'), 
                    'desc': f"{f.get('category')}: {f.get('description')}"
                })
            return findings

        # Legacy / Fallback Structure
        results = data.get('results', {})
        
        # Security
        sec = results.get('security', {})
        for s in sec.get('secrets', []):
            findings.append({'severity': 'Critical', 'desc': f"Secret Exposed: {s.get('type')}"})
            
        # PII
        pii = results.get('pii', {})
        for p in pii.get('findings', []):
            findings.append({'severity': 'High', 'desc': f"PII Leak: {p.get('type')}"})
            
        # SEO
        seo = results.get('seo', {})
        for s in seo.get('missing_title', []):
            findings.append({'severity': 'Low', 'desc': f"SEO Missing Title: {s}"})
            
        return findings

    def _normalize_p3(self, data):
        findings = []
        # Support new P3 structure (direct dict) or nested
        checklist = data.get('checklist', [])
        if not checklist:
             checklist = data.get('results', {}).get('checklist', [])

        for item in checklist:
            # Map item priority to severity
            prio = item.get('priority', 'Low')
            findings.append({'severity': prio, 'desc': f"Compliance Gap: {item.get('title')}"})
        return findings
