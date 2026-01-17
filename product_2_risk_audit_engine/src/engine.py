from .crawler import Crawler
from .risk_registry import RiskRegistry
from .scanners.seo import SEOScanner
from .scanners.security import SecurityScanner
from .scanners.pii import PIIScanner
from .scanners.dependencies import DependencyScanner
import logging

logger = logging.getLogger(__name__)

class AuditEngine:
    def __init__(self):
        self.registry = RiskRegistry()
        self.scanners = [
            SEOScanner(self.registry),
            SecurityScanner(self.registry),
            PIIScanner(self.registry),
            DependencyScanner(self.registry)
        ]

    def run(self, target_input):
        print(f"Starting Audit for: {target_input}")
        
        # 1. Crawl
        crawler = Crawler(target_input)
        assets = crawler.crawl(limit=20) # Limit for MVP
        print(f"Crawled {len(assets)} assets/pages.")

        # 2. Scan
        print("Running Risk Scanners...")
        for path, asset in assets.items():
            for scanner in self.scanners:
                try:
                    scanner.scan(asset)
                except Exception as e:
                    logger.error(f"Scanner error on {path}: {e}")
        
        # 3. Data Quality Score
        # Calculate a simple Data Quality Score based on empty assets or missing metadata
        total_assets = len(assets)
        quality_issues = 0
        for path, asset in assets.items():
            if not asset.content:
                quality_issues += 1
            if asset.is_remote and asset.status_code != 200:
                quality_issues += 1
        
        dq_score = 100 - (quality_issues / total_assets * 100) if total_assets > 0 else 0
        self.registry.add_metric('data_quality_score', round(dq_score, 2))
        
        # 4. Playbook Linking
        # Post-process risks to add playbook links
        for risk in self.registry.findings:
            risk['playbook_url'] = self._get_playbook(risk['category']) # Use category (SEO, Security) not type

        return self.registry.get_report()

    def _get_playbook(self, risk_type):
        # Map categories to playbooks
        risk_type = risk_type.upper()
        playbooks = {
            'COMPLIANCE': 'https://internal-docs/playbooks/pii-leak-response',
            'SECURITY': 'https://internal-docs/playbooks/security-incident',
            'SEO': 'https://internal-docs/playbooks/seo-fix',
            'STABILITY': 'https://internal-docs/playbooks/vuln-patching'
        }
        return playbooks.get(risk_type, 'https://internal-docs/playbooks/general-triage')
