import requests
import os
from urllib.parse import urlparse, urljoin
import logging

logger = logging.getLogger(__name__)

class AuditTarget:
    def __init__(self, url=None, path=None):
        self.url = url
        self.path = path
        self.is_remote = bool(url)
        self.content = None
        self.headers = {}
        self.status_code = None

class Crawler:
    def __init__(self, target):
        self.target = target # String url or path
        self.visited = {} # Map url/path -> AuditTarget

    def crawl(self, limit=50):
        # MVP: Shallow crawl (Homepage + 1 level or single directory)
        # to demonstrate logic without taking forever.
        
        if self.target.startswith('http'):
            self._crawl_web(self.target, limit)
        else:
            self._crawl_fs(self.target)
        return self.visited

    def _crawl_web(self, start_url, limit):
        queue = [start_url]
        base_domain = urlparse(start_url).netloc

        while queue and len(self.visited) < limit:
            url = queue.pop(0)
            if url in self.visited:
                continue

            try:
                response = requests.get(url, timeout=5)
                target = AuditTarget(url=url)
                target.content = response.content
                target.headers = response.headers
                target.status_code = response.status_code
                
                self.visited[url] = target

                # Simple link extraction for next hop
                if 'text/html' in response.headers.get('Content-Type', ''):
                    # We'll rely on Scanners to parse HTML deeply, 
                    # but here we just need links for the crawler.
                    # Using simple string search for speed in MVP
                    import re
                    links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
                    for link in links:
                        next_url = urljoin(url, link)
                        if urlparse(next_url).netloc == base_domain:
                            if next_url not in self.visited and next_url not in queue:
                                queue.append(next_url)

            except Exception as e:
                logger.error(f"Failed to crawl {url}: {e}")
                t = AuditTarget(url=url)
                t.error = str(e)
                self.visited[url] = t

    def _crawl_fs(self, root_path):
        for root, _, files in os.walk(root_path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'rb') as f:
                        content = f.read()
                    
                    target = AuditTarget(path=full_path)
                    target.content = content
                    self.visited[full_path] = target
                except Exception as e:
                    logger.error(f"Failed to read {full_path}: {e}")
