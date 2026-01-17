import json
import os

class RulesEngine:
    def __init__(self, rules_path):
        self.rules = self._load_rules(rules_path)

    def _load_rules(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, 'r') as f:
            return json.load(f)

    def _priority_sort(self, priority):
        priorities = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        return priorities.get(priority, 4)

    def evaluate(self, context):
        applicable_requirements = []
        triggered_regulations = []
        
        user_industry = [i.lower() for i in context.get('industry', [])] if isinstance(context.get('industry'), list) else [context.get('industry', '').lower()]
        user_region = [r.lower() for r in context.get('region', [])]
        user_data = [d.lower() for d in context.get('data_types', [])]

        for reg_name, reg_data in self.rules.items():
            triggers = reg_data.get('triggers', {})
            match = False
            
            # Check Region
            req_regions = [r.lower() for r in triggers.get('region', [])]
            if req_regions:
                if 'global' in req_regions or any(r in req_regions for r in user_region):
                    match = True
            
            # Check Industry
            req_industries = [i.lower() for i in triggers.get('industry', [])]
            if req_industries:
                if any(i in req_industries for i in user_industry):
                    match = True

            # Check Data Types
            req_data = [d.lower() for d in triggers.get('data_types', [])]
            if req_data:
                if any(d in req_data for d in user_data):
                    match = True

            if match:
                triggered_regulations.append(reg_name)
                for req in reg_data.get('requirements', []):
                    # Create a copy to avoid modifying the loaded rules
                    req_copy = req.copy()
                    req_copy['regulation'] = reg_name
                    applicable_requirements.append(req_copy)

        return {
            'regulations': triggered_regulations,
            'checklist': sorted(applicable_requirements, key=lambda x: self._priority_sort(x.get('priority', 'Low')))
        }
