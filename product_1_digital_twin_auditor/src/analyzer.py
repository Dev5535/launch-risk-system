import json
try:
    import yaml
except ImportError:
    yaml = None
import difflib
from .crawler import Asset

class Analyzer:
    def __init__(self, source_assets, target_assets):
        self.source_assets = source_assets
        self.target_assets = target_assets
        self.report = {
            'summary': {'missing': 0, 'new': 0, 'modified': 0, 'metadata_mismatch': 0, 'errors': 0},
            'details': [],
            'removed_in_prod': [],
            'modified': []
        }

    def analyze(self):
        all_paths = set(self.source_assets.keys()) | set(self.target_assets.keys())

        for path in sorted(all_paths):
            source = self.source_assets.get(path)
            target = self.target_assets.get(path)

            if source and not target:
                self._add_issue('MISSING', path, 'Asset exists in source but missing in target', 'High')
                self.report['summary']['missing'] += 1
                self.report['removed_in_prod'].append(path)
            elif target and not source:
                self._add_issue('NEW', path, 'New asset found in target', 'Low')
                self.report['summary']['new'] += 1
            else:
                # Both exist
                self._compare_assets(source, target)

        return self.report

    def _compare_assets(self, source, target):
        # Check for errors first
        if 'error' in source.metadata or 'error' in target.metadata:
            self._add_issue('ERROR', source.path, f"Crawl error. Source: {source.metadata.get('error')}, Target: {target.metadata.get('error')}", 'Critical')
            self.report['summary']['errors'] += 1
            return

        # Content Check
        if source.content_hash != target.content_hash:
            diff_details = self._get_content_diff(source, target)
            self._add_issue('MODIFIED', source.path, 'Content differs between source and target', 'Medium', diff_details)
            self.report['summary']['modified'] += 1
            self.report['modified'].append(source.path)
        
        # Metadata Check (Permissions, Headers)
        # We filter out some volatile metadata like 'mtime' or 'Date' header
        source_meta = self._clean_metadata(source.metadata)
        target_meta = self._clean_metadata(target.metadata)
        
        if source_meta != target_meta:
             meta_diff = self._dict_diff(source_meta, target_meta)
             self._add_issue('METADATA_MISMATCH', source.path, 'Metadata configuration drift detected', 'Medium', str(meta_diff))
             self.report['summary']['metadata_mismatch'] += 1

    def _clean_metadata(self, metadata):
        # Remove volatile fields
        clean = metadata.copy()
        clean.pop('mtime', None)
        clean.pop('Date', None) # HTTP header
        clean.pop('Last-Modified', None) # HTTP header
        clean.pop('Etag', None) # HTTP header
        return clean

    def _dict_diff(self, d1, d2):
        diff = {}
        all_keys = set(d1.keys()) | set(d2.keys())
        for k in all_keys:
            if k not in d1:
                diff[k] = {'old': None, 'new': d2[k]}
            elif k not in d2:
                diff[k] = {'old': d1[k], 'new': None}
            elif d1[k] != d2[k]:
                diff[k] = {'old': d1[k], 'new': d2[k]}
        return diff

    def _get_content_diff(self, source, target):
        # Try to parse as JSON or YAML for structured diff
        try:
            s_obj = self._parse_structured(source.content)
            t_obj = self._parse_structured(target.content)
            if s_obj and t_obj:
                return str(self._dict_diff(s_obj, t_obj))
        except:
            pass
        return "Binary or unstructured text difference"

    def _parse_structured(self, content):
        if not content: return None
        try:
            return json.loads(content)
        except:
            pass
        try:
            return yaml.safe_load(content)
        except:
            pass
        return None

    def _add_issue(self, issue_type, path, description, severity, details=None):
        self.report['details'].append({
            'type': issue_type,
            'path': path,
            'description': description,
            'severity': severity,
            'details': details
        })
