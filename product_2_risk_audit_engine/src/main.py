import argparse
import sys
import os
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.engine import AuditEngine

def main():
    parser = argparse.ArgumentParser(description="Launch Risk Intelligence - Automated Risk Audit Engine")
    parser.add_argument('--target', required=True, help="Target URL or Directory Path to audit")
    parser.add_argument('--output', default='risk_report.json', help="Output JSON report file path")
    
    args = parser.parse_args()

    engine = AuditEngine()
    report = engine.run(args.target)

    # Console Summary
    print("\n" + "="*60)
    print("LAUNCH RISK INTELLIGENCE: COMPREHENSIVE AUDIT REPORT")
    print("="*60)
    
    stats = report['summary']
    print(f"\nRISK SUMMARY:")
    print(f"  [CRITICAL] Critical: {stats['Critical']}")
    print(f"  [HIGH]     High:     {stats['High']}")
    print(f"  [MEDIUM]   Medium:   {stats['Medium']}")
    print(f"  [LOW]      Low:      {stats['Low']}")
    
    if report['findings']:
        print("\nTOP RISKS DETECTED:")
        # Show top 5 findings
        for f in report['findings'][:5]:
            print(f"  [{f['severity'].upper()}] {f['category']}: {f['description']}")
            print(f"     Location: {f['location']}")
            print(f"     Evidence: {f['evidence'][:100]}...")
    else:
        print("\n[OK] No significant risks detected.")

    print("\n" + "="*60)

    # Export
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Full report saved to: {args.output}")

if __name__ == "__main__":
    main()
