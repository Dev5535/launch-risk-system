import json
import os
import datetime

class RemediationEngine:
    def __init__(self, solutions_path):
        self.solutions = self._load_solutions(solutions_path)

    def _load_solutions(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, 'r') as f:
            return json.load(f)

    def generate_runbook(self, findings):
        """
        findings: List of dicts {'id': '...', 'context': {...}}
        Returns: Markdown string
        """
        runbook = []
        runbook.append(f"# 🛠️ FIX-IT-YOURSELF REMEDIATION RUNBOOK")
        runbook.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if not findings:
            runbook.append("✅ No issues found requiring remediation.")
            return "\n".join(runbook)

        # Group by Issue ID to avoid duplicates if possible, or list instances
        # Actually, listing instances is better for things like "File Missing" (multiple files)
        # But for "Implement GDPR", it's a one-time thing.
        
        # Let's iterate and lookup
        for idx, finding in enumerate(findings, 1):
            issue_id = finding.get('id')
            context = finding.get('context', {})
            
            solution = self.solutions.get(issue_id)
            
            if not solution:
                # If we don't have a canned solution, output a generic placeholder
                runbook.append(f"## {idx}. Issue: {issue_id}")
                runbook.append(f"**Context:** {context}")
                runbook.append("> ⚠️ No automated remediation guide available for this specific issue.\n")
                continue

            # Populate template
            title = solution.get('title', issue_id)
            content = solution.get('content', '')
            
            # Simple template substitution
            for key, val in context.items():
                if val:
                    content = content.replace(f"{{{{{key}}}}}", str(val))

            runbook.append(f"## {idx}. {title} ({issue_id})")
            
            if solution.get('type') == 'workflow':
                 runbook.append("**Type:** 🚨 Manual Workflow\n")
            elif solution.get('type') == 'command':
                 runbook.append("**Type:** 💻 Terminal Command\n")
            elif solution.get('type') == 'code':
                 runbook.append("**Type:** 📝 Code Change\n")

            lang = solution.get('lang', '')
            if lang:
                runbook.append(f"```{lang}")
                runbook.append(content)
                runbook.append("```\n")
            else:
                runbook.append(content + "\n")
                
            runbook.append("---\n")

        return "\n".join(runbook)
