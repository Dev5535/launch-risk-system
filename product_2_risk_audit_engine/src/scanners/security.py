import re
from .base import BaseScanner

class SecurityScanner(BaseScanner):
    def scan(self, target):
        self._scan_headers(target)
        self._scan_secrets(target)
        self._scan_protocol(target)

    def _scan_protocol(self, target):
        if target.url and target.url.startswith('http://'):
             self.registry.add_finding('Security', 'High', 'Insecure Protocol (HTTP)', 'Site is served over HTTP instead of HTTPS', target.url)

    def _scan_headers(self, target):
        if not target.is_remote: return
        
        headers = {k.lower(): v for k, v in target.headers.items()}
        
        required = {
            'strict-transport-security': 'Missing HSTS Header',
            'x-frame-options': 'Missing X-Frame-Options',
            'x-content-type-options': 'Missing X-Content-Type-Options',
            'content-security-policy': 'Missing CSP Header'
        }

        for header, msg in required.items():
            if header not in headers:
                severity = 'Medium' if header != 'content-security-policy' else 'Low' # CSP is hard, often missing
                self.registry.add_finding('Security', severity, msg, f"Header {header} not found", target.url)

        if 'server' in headers or 'x-powered-by' in headers:
             self.registry.add_finding('Security', 'Low', 'Server Information Disclosure', f"Server/Powered-By headers exposed: {headers.get('server', '')} {headers.get('x-powered-by', '')}", target.url)

    def _scan_secrets(self, target):
        if not target.content: return
        
        content = target.content.decode('utf-8', errors='ignore')
        
        patterns = {
            'AWS Access Key': r'AKIA[0-9A-Z]{16}',
            'Generic Private Key': r'-----BEGIN PRIVATE KEY-----',
            'Slack Token': r'xox[baprs]-([0-9a-zA-Z]{10,48})',
            'Google API Key': r'AIza[0-9A-Za-z-_]{35}'
        }

        for name, regex in patterns.items():
            if re.search(regex, content):
                self.registry.add_finding('Security', 'Critical', f"Exposed {name}", "Secret pattern match found in content", target.url or target.path)
