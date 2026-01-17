import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, data):
        self.data = data
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_console(self):
        print("\n" + "="*60)
        print("LAUNCH RISK INTELLIGENCE: COMPLIANCE READINESS MAP")
        print("="*60)
        print(f"Generated: {self.timestamp}")
        
        print("\n[SCOPE] APPLICABLE REGULATIONS:")
        if self.data['regulations']:
            for reg in self.data['regulations']:
                print(f"  - {reg}")
        else:
            print("  - None detected based on inputs.")

        print("\n[CHECKLIST] DYNAMIC REQUIREMENTS:")
        
        checklist = self.data['checklist']
        if not checklist:
            print("  No specific requirements found.")
        else:
            current_priority = None
            for item in checklist:
                if item['priority'] != current_priority:
                    current_priority = item['priority']
                    print(f"\n--- {current_priority.upper()} PRIORITY ---")
                
                print(f"  [ ] {item['id']} ({item['regulation']}): {item['title']}")
                print(f"      Action: {item['action']}")

        print("\n" + "="*60)
        print("NOTE: This is not legal advice. Consult a professional.")
        print("="*60 + "\n")

    def generate_json(self, filepath):
        output = {
            'meta': {
                'generated_at': self.timestamp,
                'tool': 'Product 3 - Compliance Mapper'
            },
            'results': self.data
        }
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Compliance map saved to: {filepath}")
