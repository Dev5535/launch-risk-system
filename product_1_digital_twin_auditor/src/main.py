import argparse
import sys
import os
import time

# Add current directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crawler import Crawler
from src.analyzer import Analyzer
from src.reporter import Reporter

def main():
    parser = argparse.ArgumentParser(description="Launch Risk Intelligence - Digital Twin Pre-Migration Auditor")
    parser.add_argument('--source', required=True, help="Source environment (URL or Directory Path)")
    parser.add_argument('--target', required=True, help="Target environment (URL or Directory Path)")
    parser.add_argument('--output', default='audit_report.json', help="Output JSON report file path")
    
    args = parser.parse_args()

    print(f"Starting Audit...")
    print(f"Source: {args.source}")
    print(f"Target: {args.target}")

    # Crawl Source
    print("\nCrawling Source Environment...")
    source_crawler = Crawler(args.source)
    source_assets = source_crawler.crawl()
    print(f"Found {len(source_assets)} assets in Source.")

    # Crawl Target
    print("\nCrawling Target Environment...")
    target_crawler = Crawler(args.target)
    target_assets = target_crawler.crawl()
    print(f"Found {len(target_assets)} assets in Target.")

    # Analyze
    print("\nAnalyzing Differences...")
    analyzer = Analyzer(source_assets, target_assets)
    report_data = analyzer.analyze()
    report_data['meta'] = {
        'timestamp': time.time(),
        'source': args.source,
        'target': args.target
    }

    # Report
    reporter = Reporter(report_data)
    reporter.generate_console_report()
    reporter.export_json(args.output)

if __name__ == "__main__":
    main()
