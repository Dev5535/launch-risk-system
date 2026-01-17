import os
from .base import BaseScanner

class DependencyScanner(BaseScanner):
    def scan(self, target):
        if not target.path: return # Only relevant for file system scan usually, unless we find these files via web (rare/bad)
        
        filename = os.path.basename(target.path)
        
        if filename == 'requirements.txt':
            self._scan_requirements_txt(target)
        elif filename == 'package.json':
            self._scan_package_json(target)

    def _scan_requirements_txt(self, target):
        content = target.content.decode('utf-8', errors='ignore')
        lines = content.splitlines()
        
        unpinned = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if '==' not in line:
                unpinned.append(line)
        
        if unpinned:
             self.registry.add_finding('Stability', 'Medium', 'Unpinned Python Dependencies', f"Found {len(unpinned)} unpinned libs (e.g., {unpinned[0]})", target.path)

    def _scan_package_json(self, target):
        # MVP: just check for existence, maybe parsing is overkill for "text" scan if we want to be fast
        # But let's try basic json parse
        import json
        try:
            data = json.loads(target.content)
            deps = data.get('dependencies', {})
            dev_deps = data.get('devDependencies', {})
            
            all_deps = {**deps, **dev_deps}
            unpinned = [k for k, v in all_deps.items() if v.startswith('^') or v.startswith('~') or v == '*']
            
            if unpinned:
                self.registry.add_finding('Stability', 'Low', 'Loose Node.js Dependencies', f"Found {len(unpinned)} loose versions (e.g., {unpinned[0]})", target.path)
        except:
            pass
