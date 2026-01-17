import argparse
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.engine import RulesEngine
from src.reporter import ReportGenerator

def get_user_input():
    print("\n--- COMPLIANCE CONTEXT GATHERING ---\n")
    
    industry = input("Industry (e.g., Healthcare, Finance, SaaS): ").strip()
    
    print("\nRegions (comma separated, e.g., EU, US, CA):")
    regions_in = input("> ").strip()
    regions = [r.strip() for r in regions_in.split(',')] if regions_in else []
    
    print("\nData Types Handled (comma separated, e.g., PII, Health, Financial):")
    data_in = input("> ").strip()
    data_types = [d.strip() for d in data_in.split(',')] if data_in else []
    
    return {
        'industry': industry,
        'region': regions,
        'data_types': data_types
    }

def main():
    parser = argparse.ArgumentParser(description="Launch Risk Intelligence - Dynamic Regulatory Compliance Mapper")
    parser.add_argument('--interactive', action='store_true', help="Run in interactive mode")
    parser.add_argument('--industry', help="Target Industry")
    parser.add_argument('--region', help="Target Regions (comma separated)")
    parser.add_argument('--data-types', help="Data Types (comma separated)")
    parser.add_argument('--output', default='compliance_map.json', help="Output JSON file")
    
    args = parser.parse_args()

    context = {}
    if args.interactive:
        context = get_user_input()
    else:
        # CLI Mode
        if not (args.industry or args.region or args.data_types):
            print("Error: Must provide inputs via arguments or use --interactive")
            sys.exit(1)
            
        context = {
            'industry': args.industry,
            'region': [r.strip() for r in args.region.split(',')] if args.region else [],
            'data_types': [d.strip() for d in args.data_types.split(',')] if args.data_types else []
        }

    # Load Rules
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rules_path = os.path.join(base_dir, 'src', 'data', 'rules.yaml')
    
    engine = RulesEngine(rules_path)
    results = engine.evaluate(context)

    # Report
    reporter = ReportGenerator(results)
    reporter.generate_console()
    reporter.generate_json(args.output)

if __name__ == "__main__":
    main()
