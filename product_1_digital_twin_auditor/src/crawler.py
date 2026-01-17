import os
import hashlib
import requests
from urllib.parse import urlparse, urljoin
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Asset:
    def __init__(self, path, asset_type, content=None, metadata=None):
        self.path = path
        self.asset_type = asset_type
        self.content = content
        self.metadata = metadata or {}
        self.content_hash = self._compute_hash(content)

    def _compute_hash(self, content):
        if content is None:
            return None
        if isinstance(content, str):
            content = content.encode('utf-8')
        return hashlib.sha256(content).hexdigest()

    def __repr__(self):
        return f"<Asset path={self.path} type={self.asset_type} hash={self.content_hash[:8] if self.content_hash else 'None'}>"

class Crawler:
    def __init__(self, base_uri):
        self.base_uri = base_uri
        self.is_url = base_uri.startswith('http://') or base_uri.startswith('https://')
        self.assets = {} # Map path -> Asset

    def crawl(self):
        logger.info(f"Starting crawl for: {self.base_uri}")
        if self.is_url:
            self._crawl_url(self.base_uri)
        else:
            self._crawl_dir(self.base_uri)
        return self.assets

    def _crawl_dir(self, directory):
        # Shadow IT extensions to watch for
        SHADOW_IT_EXTS = {'.exe', '.bat', '.sh', '.ps1', '.vbs', '.msi', '.jar', '.war'}
        
        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.base_uri).replace('\\', '/')
                _, ext = os.path.splitext(file)
                
                try:
                    with open(full_path, 'rb') as f:
                        content = f.read()
                    
                    stat = os.stat(full_path)
                    metadata = {
                        'size': stat.st_size,
                        'permissions': oct(stat.st_mode)[-3:],
                        'mtime': stat.st_mtime
                    }
                    
                    # Shadow IT Detection
                    if ext.lower() in SHADOW_IT_EXTS:
                        metadata['shadow_it_flag'] = True
                        metadata['shadow_reason'] = f"Unmanaged executable format: {ext}"
                    
                    # Dependency Extraction (Python/JS)
                    dependencies = []
                    try:
                        text_content = content.decode('utf-8', errors='ignore')
                        if ext.lower() == '.py':
                            dependencies.extend(re.findall(r'^(?:import|from)\s+([\w\.]+)', text_content, re.MULTILINE))
                        elif ext.lower() in ['.js', '.ts']:
                            dependencies.extend(re.findall(r'require\([\'"]([^\'"]+)[\'"]\)', text_content))
                            dependencies.extend(re.findall(r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]', text_content))
                    except:
                        pass
                    
                    if dependencies:
                        metadata['dependencies'] = list(set(dependencies))

                    self.assets[rel_path] = Asset(rel_path, 'file', content, metadata)
                except Exception as e:
                    logger.error(f"Error reading file {full_path}: {e}")
                    self.assets[rel_path] = Asset(rel_path, 'file', None, {'error': str(e)})

    def _crawl_url(self, url, visited=None):
        # Basic depth-1 crawler for now to avoid infinite loops in this MVP
        # In a real scenario, this would be more robust with depth control.
        # We will focus on the provided URL and its immediate internal links.
        if visited is None:
            visited = set()
        
        parsed_base = urlparse(self.base_uri)
        parsed_current = urlparse(url)
        
        if parsed_current.netloc != parsed_base.netloc:
            return # Skip external links

        rel_path = parsed_current.path
        if rel_path == '': rel_path = '/'
        
        if rel_path in self.assets:
            return

        visited.add(url)
        
        try:
            response = requests.get(url, timeout=10)
            metadata = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'url': url
            }
            
            content = response.content
            self.assets[rel_path] = Asset(rel_path, 'url', content, metadata)

            # If HTML, find more links
            if 'text/html' in response.headers.get('Content-Type', ''):
                # Simple regex link extraction instead of BS4
                try:
                    text_content = content.decode('utf-8', errors='ignore')
                    links = re.findall(r'href=[\'"]?([^\'" >]+)', text_content)
                    for href in links:
                        next_url = urljoin(url, href)
                        # Only crawl internal links
                        if urlparse(next_url).netloc == parsed_base.netloc:
                             # Limit recursion for MVP to avoid huge crawl times
                             if next_url not in visited:
                                 pass 
                except Exception as e:
                    logger.warning(f"Error parsing links in {url}: {e}")

        except Exception as e:
            logger.error(f"Error crawling URL {url}: {e}")
            self.assets[rel_path] = Asset(rel_path, 'url', None, {'error': str(e)})

