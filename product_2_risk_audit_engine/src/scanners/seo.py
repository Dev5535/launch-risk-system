import re
from .base import BaseScanner

class SEOScanner(BaseScanner):
    def scan(self, target):
        if target.status_code and target.status_code >= 400:
            self.registry.add_finding(
                'SEO', 'High', f"Broken Link (Status {target.status_code})", 
                f"URL returned {target.status_code}", target.url or target.path
            )
            return

        content_type = target.headers.get('Content-Type', '') if target.is_remote else ''
        if not target.is_remote and (target.path.endswith('.html') or target.path.endswith('.htm')):
             content_type = 'text/html'

        if 'text/html' in content_type and target.content:
            self._scan_html(target)
        
        if target.url and 'robots.txt' in target.url:
             self._scan_robots(target)

    def _scan_html(self, target):
        try:
            content = target.content.decode('utf-8', errors='ignore')
            
            # Title
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if not title_match or not title_match.group(1).strip():
                self.registry.add_finding('SEO', 'Medium', 'Missing Title Tag', 'Page has no <title>', target.url or target.path)
            elif len(title_match.group(1)) > 60:
                self.registry.add_finding('SEO', 'Low', 'Title Tag too long', f"Length: {len(title_match.group(1))} (Recommended < 60)", target.url or target.path)

            # Meta Description
            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
            if not desc_match or not desc_match.group(1).strip():
                self.registry.add_finding('SEO', 'Medium', 'Missing Meta Description', 'Page has no meta description', target.url or target.path)

            # H1
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            if not h1s:
                self.registry.add_finding('SEO', 'High', 'Missing H1 Tag', 'Page content should have a main heading', target.url or target.path)
            elif len(h1s) > 1:
                self.registry.add_finding('SEO', 'Low', 'Multiple H1 Tags', f"Found {len(h1s)} H1 tags (Recommended: 1)", target.url or target.path)

            # Images alt - basic regex
            # Find img tags, then check for alt
            img_tags = re.findall(r'<img[^>]+>', content, re.IGNORECASE)
            missing_alt = [tag for tag in img_tags if 'alt=' not in tag]
            if missing_alt:
                self.registry.add_finding('SEO', 'Low', 'Images missing Alt text', f"Found {len(missing_alt)} images without alt text", target.url or target.path)

        except Exception as e:
            pass # Parsing error

    def _scan_robots(self, target):
        content = target.content.decode('utf-8', errors='ignore')
        if 'Disallow: /' in content and 'Allow:' not in content:
             self.registry.add_finding('SEO', 'Critical', 'Robots.txt blocks everything', 'User-agent: * Disallow: / detected', target.url)
