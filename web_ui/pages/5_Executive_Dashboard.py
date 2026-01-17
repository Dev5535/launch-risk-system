import streamlit as st
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Add web_ui to path for layout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from product_5_readiness_scorer.src.scorer import LaunchScorer
from product_5_readiness_scorer.src.ingestor import ReportIngestor
from product_5_readiness_scorer.src.reporter import ExecutiveReporter
from layout import render_support_sidebar, render_footer

st.set_page_config(page_title="Executive Dashboard", page_icon="👔")

render_support_sidebar()

st.header("📊 Product 5: Launch Readiness & Executive Sign-Off")
st.markdown("**User:** C-Suite / VPs | **Goal:** Go/No-Go Decision Support")

# Gather Data
findings = []
ingestor = ReportIngestor()

if st.session_state.get('p1_report'): findings.extend(ingestor._normalize_p1(st.session_state['p1_report']))
if st.session_state.get('p2_report'): findings.extend(ingestor._normalize_p2(st.session_state['p2_report']))
if st.session_state.get('p3_report'): findings.extend(ingestor._normalize_p3(st.session_state['p3_report']))

if not findings:
    st.info("Waiting for data from other modules...")
    st.stop()

# Scoring
scorer = LaunchScorer()
result = scorer.calculate(findings)

# Dashboard Layout
st.markdown("---")
col_score, col_status = st.columns([1, 2])

with col_score:
    st.metric("Readiness Score", f"{result['score']}/100")

with col_status:
    status = result['status']
    color = result['color']
    
    if status == "APPROVED":
        st.success(f"### STATUS: {status}")
        st.balloons()
    elif status == "CAUTION":
        st.warning(f"### STATUS: {status}")
    else:
        st.error(f"### STATUS: {status}")

# Risk Breakdown
st.subheader("Risk Breakdown & Financial Impact")
c1, c2, c3, c4 = st.columns(4)
bk = result['breakdown']
c1.metric("Critical Blockers", bk['Critical'])
c2.metric("High Risks", bk['High'])
c3.metric("Medium Risks", bk['Medium'])
c4.metric("Low Risks", bk['Low'])

# Financial Impact Analyzer
# Simple heuristic model
impact_cost = (bk['Critical'] * 1000000) + (bk['High'] * 100000) + (bk['Medium'] * 10000) + (bk['Low'] * 1000)
st.metric("Estimated Financial Exposure", f"£{impact_cost:,.0f}", delta_color="inverse")

# Predictive Analytics
st.markdown("---")
st.subheader("🔮 Predictive Scenario Planning")
st.info("What if we delay the launch to fix issues?")

col_pred1, col_pred2 = st.columns(2)
with col_pred1:
    delay_weeks = st.slider("Planned Delay (Weeks)", 0, 12, 0)
    # Simulation: Assume 20% of risks are fixed per week
    remediation_rate = 0.20
    remediated_fraction = min(1.0, delay_weeks * remediation_rate)
    
    projected_score = result['score'] + ((100 - result['score']) * remediated_fraction)
    projected_cost = impact_cost * (1 - remediated_fraction)

with col_pred2:
    st.metric("Projected Readiness Score", f"{projected_score:.0f}/100", delta=f"{projected_score - result['score']:.0f}")
    st.metric("Projected Risk Exposure", f"£{projected_cost:,.0f}", delta=f"-£{impact_cost - projected_cost:,.0f}")

# Decision Module
st.markdown("---")
st.subheader("Executive Decision & Audit Trail")

col_d1, col_d2 = st.columns(2)
with col_d1:
    signer_name = st.text_input("Executive Name")
    reason = st.text_area("Sign-Off Notes / Conditions")
    
with col_d2:
    st.write("Action:")
    if st.button("✅ APPROVE LAUNCH", type="primary", disabled=(status=="BLOCKED")):
        st.success(f"Launch Approved by {signer_name}! Notification sent to Ops.")
        # Log to Audit Trail
        if signer_name:
            with open("audit_log.csv", "a") as f:
                f.write(f"{pd.Timestamp.now()},{signer_name},APPROVED,{result['score']},{reason}\n")
    
    if st.button("⛔ REJECT / DELAY"):
        st.error(f"Launch Rejected by {signer_name}. Remediation required.")
        if signer_name:
            with open("audit_log.csv", "a") as f:
                f.write(f"{pd.Timestamp.now()},{signer_name},REJECTED,{result['score']},{reason}\n")

# Display Audit Trail
with st.expander("📜 View Historical Audit Trail"):
    if os.path.exists("audit_log.csv"):
        try:
            # Handle potential empty file or header issues
            log_df = pd.read_csv("audit_log.csv", names=["Timestamp", "User", "Action", "Score", "Notes"])
            st.dataframe(log_df)
        except:
            st.write("No logs yet.")
    else:
        st.write("No audit trail found.")

# Export Report
st.markdown("---")
detailed = [f"{f['severity'].upper()}: {f['desc']}" for f in sorted(findings, key=lambda x: scorer.weights.get(x['severity'], 0), reverse=True)]
reporter = ExecutiveReporter()
html_report = reporter.generate_html(result, detailed)

st.download_button("📄 Download Executive HTML Report", html_report, file_name="launch_executive_summary.html", mime="text/html")

render_footer()
