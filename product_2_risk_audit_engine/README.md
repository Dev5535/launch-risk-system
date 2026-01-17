# Automated Comprehensive Risk Audit Engine (Product 2)

An extensible, multi-domain risk detection engine that scans for SEO, Security, Stability, and Compliance risks.

## Features
- **Multi-Domain Scanning**:
  - **SEO**: Detects missing titles, H1s, meta descriptions, and broken links.
  - **Security**: Scans for exposed secrets (API keys), missing security headers, and insecure protocols.
  - **Stability**: Checks for unpinned dependencies in `requirements.txt` and `package.json`.
  - **Compliance**: Basic PII detection (Emails, SSNs).
- **Evidence-Backed Findings**: Every risk includes location and evidence snippet.
- **Severity Grading**: Categorizes risks into Critical, High, Medium, and Low.
- **Unified Reporting**: CLI summary and JSON export.

## Installation
1. Ensure Python 3.x is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the audit against a URL or local directory:

```bash
python src/main.py --target <URL_OR_DIRECTORY>
```

### Examples

**Audit a local project:**
```bash
python src/main.py --target ./my_project_src
```

**Audit a live website:**
```bash
python src/main.py --target https://example.com
```

## Scanners Included
| Domain | Checks |
|--------|--------|
| **SEO** | Titles, Meta Descriptions, H1 Structure, Alt Text, Robots.txt |
| **Security** | AWS/API Keys, Security Headers (HSTS, CSP, etc.), HTTP vs HTTPS |
| **Stability** | Unpinned dependencies (Python/Node.js) |
| **Compliance** | Potential PII exposure (Emails, SSNs) |

## Output
- **Console**: Executive summary of top risks.
- **JSON**: Full report with all findings (`risk_report.json`).
