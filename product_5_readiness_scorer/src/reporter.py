import datetime

class ExecutiveReporter:
    def __init__(self):
        pass

    def generate_html(self, score_data, detailed_findings):
        """
        score_data: dict from LaunchScorer
        detailed_findings: list of strings/dicts for the appendix
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = score_data['status']
        color = score_data['color']
        score = score_data['score']
        breakdown = score_data['breakdown']
        
        # Simple CSS
        css = """
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; }
        .header { text-align: center; border-bottom: 2px solid #eee; padding-bottom: 20px; }
        .score-card { background: #f8f9fa; border-radius: 8px; padding: 30px; text-align: center; margin: 30px 0; }
        .score { font-size: 64px; font-weight: bold; }
        .status { font-size: 24px; padding: 5px 15px; border-radius: 4px; display: inline-block; margin-top: 10px; color: white; }
        .red { background: #dc3545; }
        .yellow { background: #ffc107; color: #333; }
        .green { background: #28a745; }
        .metrics { display: flex; justify-content: space-around; margin-top: 20px; }
        .metric { text-align: center; }
        .metric-val { font-size: 24px; font-weight: bold; }
        .metric-label { font-size: 14px; color: #666; }
        .appendix { margin-top: 40px; }
        .finding { padding: 10px; border-bottom: 1px solid #eee; }
        """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Launch Readiness Executive Summary</title>
            <style>{css}</style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Launch Readiness Report</h1>
                <p>Generated: {timestamp}</p>
            </div>
            
            <div class="score-card">
                <div class="score" style="color: {color}">{score}/100</div>
                <div class="status {color}">{status}</div>
                
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-val" style="color: #dc3545">{breakdown['Critical']}</div>
                        <div class="metric-label">Critical Blockers</div>
                    </div>
                    <div class="metric">
                        <div class="metric-val" style="color: #fd7e14">{breakdown['High']}</div>
                        <div class="metric-label">High Risks</div>
                    </div>
                    <div class="metric">
                        <div class="metric-val" style="color: #ffc107">{breakdown['Medium']}</div>
                        <div class="metric-label">Medium Risks</div>
                    </div>
                     <div class="metric">
                        <div class="metric-val" style="color: #6c757d">{breakdown['Low']}</div>
                        <div class="metric-label">Low Risks</div>
                    </div>
                </div>
            </div>
            
            <div class="appendix">
                <h2>🔍 Risk Audit Appendix</h2>
                <p>Top findings influencing this score:</p>
                <ul>
        """
        
        for f in detailed_findings[:10]: # Show top 10
            html += f"<li class='finding'>{f}</li>"
            
        if len(detailed_findings) > 10:
             html += f"<li>...and {len(detailed_findings) - 10} more findings.</li>"
             
        html += """
                </ul>
                <p><i>Refer to the Remediation Runbook (Product 4) for fix instructions.</i></p>
            </div>
            
            <div class="footer" style="text-align: center; margin-top: 50px; font-size: 12px; color: #999;">
                Launch Risk Intelligence System &copy; 2026
            </div>
        </body>
        </html>
        """
        
        return html
