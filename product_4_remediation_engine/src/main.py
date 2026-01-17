import argparse
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestor import ReportIngestor
from src.engine import RemediationEngine

def main():
    parser = argparse.ArgumentParser(description="Launch Risk Intelligence - Fix-It-Yourself Remediation Engine")
    parser.add_argument('--p1', help="Path to Product 1 Report (Digital Twin)")
    parser.add_argument('--p2', help="Path to Product 2 Report (Risk Audit)")
    parser.add_argument('--p3', help="Path to Product 3 Report (Compliance Map)")
    parser.add_argument('--output', default='remediation_runbook.md', help="Output Markdown file")
    
    args = parser.parse_args()
    
    ingestor = ReportIngestor()
    all_findings = []
    
    if args.p1:
        print(f"Loading Product 1 Report: {args.p1}")
        all_findings.extend(ingestor.load_report(args.p1, 'p1'))
        
    if args.p2:
        print(f"Loading Product 2 Report: {args.p2}")
        all_findings.extend(ingestor.load_report(args.p2, 'p2'))
        
    if args.p3:
        print(f"Loading Product 3 Report: {args.p3}")
        all_findings.extend(ingestor.load_report(args.p3, 'p3'))

    if not all_findings:
        print("No findings loaded. Please provide at least one report file (--p1, --p2, --p3).")
        # Proceeding anyway to generate empty runbook
    
    print(f"Total findings to remediate: {len(all_findings)}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    solutions_path = os.path.join(base_dir, 'src', 'data', 'solutions.yaml')
    
    engine = RemediationEngine(solutions_path)
    runbook_content = engine.generate_runbook(all_findings)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(runbook_content)
        
    print(f"\n✅ Runbook generated: {args.output}")

if __name__ == "__main__":
    main()
