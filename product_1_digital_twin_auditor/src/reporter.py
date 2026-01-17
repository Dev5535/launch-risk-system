import json
import sys

class Reporter:
    def __init__(self, report_data):
        self.report_data = report_data

    def generate_console_report(self):
        summary = self.report_data['summary']
        details = self.report_data['details']

        print("\n" + "="*60)
        print("LAUNCH RISK INTELLIGENCE: DIGITAL TWIN AUDIT REPORT")
        print("="*60 + "\n")

        print("SUMMARY:")
        print(f"  Missing Assets:     {summary['missing']}")
        print(f"  New Assets:         {summary['new']}")
        print(f"  Modified Assets:    {summary['modified']}")
        print(f"  Config Drift:       {summary['metadata_mismatch']}")
        print(f"  Errors:             {summary['errors']}")
        print("-" * 60)

        blockers = [d for d in details if d['severity'] in ['Critical', 'High']]
        warnings = [d for d in details if d['severity'] in ['Medium']]
        infos = [d for d in details if d['severity'] in ['Low']]

        if blockers:
            print("\n[BLOCKER] CRITICAL ISSUES (MUST FIX BEFORE LAUNCH):")
            for item in blockers:
                print(f"  [{item['type']}] {item['path']}")
                print(f"     Reason: {item['description']}")
                if item.get('details'):
                    print(f"     Details: {item['details'][:200]}..." if len(str(item['details'])) > 200 else f"     Details: {item['details']}")
        else:
            print("\n[OK] NO BLOCKERS DETECTED.")

        if warnings:
            print("\n[WARNING] REVIEW RECOMMENDED:")
            for item in warnings:
                print(f"  [{item['type']}] {item['path']}")
                print(f"     Reason: {item['description']}")

        if infos:
            print("\n[INFO] FYI:")
            for item in infos:
                print(f"  [{item['type']}] {item['path']}")

        print("\n" + "="*60)
        print("END OF REPORT")
        print("="*60 + "\n")

    def export_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.report_data, f, indent=2)
        print(f"Full structured report saved to: {filepath}")
