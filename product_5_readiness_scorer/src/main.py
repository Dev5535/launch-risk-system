import argparse
import sys
import os

# Add path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestor import ReportIngestor
from src.scorer import LaunchScorer
from src.reporter import ExecutiveReporter

def main():
    parser = argparse.ArgumentParser(description="Launch Readiness Scoring Engine")
    parser.add_argument('--p1', help="Path to Product 1 Report")
    parser.add_argument('--p2', help="Path to Product 2 Report")
    parser.add_argument('--p3', help="Path to Product 3 Report")
    parser.add_argument('--output', default='launch_readiness.html', help="Output HTML file")
    
    args = parser.parse_args()
    
    ingestor = ReportIngestor()
    findings = []
    
    if args.p1: findings.extend(ingestor.load_report(args.p1, 'p1'))
    if args.p2: findings.extend(ingestor.load_report(args.p2, 'p2'))
    if args.p3: findings.extend(ingestor.load_report(args.p3, 'p3'))
    
    scorer = LaunchScorer()
    score_result = scorer.calculate(findings)
    
    # Format detailed findings for appendix
    detailed = [f"{f['severity'].upper()}: {f['desc']}" for f in sorted(findings, key=lambda x: scorer.weights.get(x['severity'], 0), reverse=True)]
    
    reporter = ExecutiveReporter()
    html_content = reporter.generate_html(score_result, detailed)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"\n🚀 Readiness Score: {score_result['score']}/100")
    print(f"Status: {score_result['status']}")
    print(f"Report generated: {args.output}")

if __name__ == "__main__":
    main()
