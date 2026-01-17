# Digital Twin Pre-Migration Auditor (Product 1)

A calm, factual system that compares an existing (source) environment with a planned (target) environment to detect risks before launch.

## Features
- **Digital Twin Crawling**: Scans both source and target environments (File System or HTTP).
- **Delta Detection**: Identifies missing assets, new files, modified content, and configuration drift.
- **Risk Categorization**: Automatically classifies issues into Blockers, Warnings, and Info.
- **Structured Reporting**: Outputs a clear CLI summary and a detailed JSON report.

## Installation
1. Ensure Python 3.x is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool from the command line:

```bash
python src/main.py --source <SOURCE_PATH_OR_URL> --target <TARGET_PATH_OR_URL>
```

### Examples

**Compare local directories:**
```bash
python src/main.py --source ./old_site --target ./new_site
```

**Compare live sites (Basic):**
```bash
python src/main.py --source https://example.com --target https://staging.example.com
```

## Output
The tool provides:
1. **Console Output**: A high-level executive summary of risks.
2. **JSON Report**: A detailed machine-readable report (default: `audit_report.json`).

## Risk Levels
- **[BLOCKER]**: Missing assets or Critical errors. Must be resolved before launch.
- **[WARNING]**: Modified content or Config drift. Review recommended.
- **[INFO]**: New assets. For information only.
