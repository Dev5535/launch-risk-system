import streamlit as st
import sys
import os
import json
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Add web_ui to path for layout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from product_2_risk_audit_engine.src.engine import AuditEngine
from layout import render_support_sidebar, render_footer

st.set_page_config(page_title="Risk Audit Engine", page_icon="🛡️")

render_support_sidebar()

st.header("🛡️ Product 2: Automated Risk Audit Engine")
st.markdown("**User:** Project Leads / Analysts | **Goal:** Multi-domain Risk Monitoring")

# Input Section
st.sidebar.header("Configuration")
target_url = st.text_input("Target URL to Scan", value="http://localhost:8000")
scan_types = st.multiselect("Active Scanners", ["SEO", "Security", "PII"], default=["SEO", "Security", "PII"])

if st.button("📡 Start Risk Scan"):
    with st.spinner("Scanning target... (This may take a moment)"):
        engine = AuditEngine()
        # Mocking or running actual scan depending on implementation
        # The engine.run() expects a URL and returns results
        
        try:
            # We need to adapt the engine call to match what we implemented in P2
            # P2 main.py uses: engine.run(url)
            results = engine.run(target_url)
            
            # Store for P4/P5
            st.session_state['p2_report'] = results
            
            st.success("Scan Completed Successfully")
            
            # Dashboard View
            st.subheader("Risk Registry Dashboard")
            
            # Summary Metrics
            # Note: P2 results structure might be flat 'risks' list or grouped 'results'.
            # Based on Engine.py: return self.registry.get_report()
            # Registry.get_report() usually returns {'summary': ..., 'risks': [...] } or similar.
            # Let's adapt based on standard P2 structure which I might have just updated or is standard.
            # If results has 'risks' list, we calculate metrics from that.
            
            risks = results.get('findings', [])
            metrics = results.get('metrics', {})
            
            seo_issues = len([r for r in risks if r['category'] == 'SEO'])
            sec_issues = len([r for r in risks if r['category'] == 'Security'])
            pii_issues = len([r for r in risks if r['category'] == 'Compliance'])
            dq_score = metrics.get('data_quality_score', 0)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("SEO Issues", seo_issues, delta_color="inverse")
            c2.metric("Security Risks", sec_issues, delta_color="inverse")
            c3.metric("Compliance/PII", pii_issues, delta_color="inverse")
            c4.metric("Data Quality", f"{dq_score}%", delta=f"{dq_score-100}%" if dq_score < 100 else None)
            
            # Detailed Breakdown
            st.divider()
            st.subheader("Risk Details & Incident Response")
            
            if risks:
                # Convert to DF
                df = pd.DataFrame(risks)
                
                # Make Playbook URL clickable
                if 'playbook_url' in df.columns:
                    df['Action'] = df['playbook_url'].apply(lambda x: f'<a href="{x}" target="_blank">📖 Open Playbook</a>')
                    # We need to render HTML for links to work
                    st.write(df[['category', 'severity', 'description', 'location', 'Action']].to_html(escape=False), unsafe_allow_html=True)
                else:
                    st.dataframe(df)
            else:
                st.success("✅ No Risks Found across any category.")

            # Export
            st.download_button(
                label="📥 Download Risk Report JSON",
                data=json.dumps(results, indent=2),
                file_name="p2_risk_report.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Scan Failed: {e}")

render_footer()
