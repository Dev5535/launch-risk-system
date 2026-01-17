import streamlit as st
from layout import render_support_sidebar, render_footer

st.set_page_config(
    page_title="Payments & Subscriptions",
    page_icon="💳",
    layout="wide"
)

render_support_sidebar()

st.title("💳 Payments & Subscriptions")
st.markdown("---")

st.info("ℹ️ **Note:** Secure Payment Gateway is currently being configured. Please contact sales for manual invoicing.")

st.markdown("### 🚀 Launch Risk Intelligence System - Enterprise Access")

st.markdown("""
Unlock the full potential of deterministic risk analysis. 
All plans include access to Digital Twin Auditor, Risk Audit Engine, Compliance Mapper, and Remediation Workflows.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏢 Single Launch Engagement")
    st.markdown("## £2,500 <span style='font-size:0.6em'>/ launch</span>", unsafe_allow_html=True)
    st.markdown("""
    *   Full Audit & Risk Report
    *   Compliance Mapping (GDPR/SOC2)
    *   Remediation Runbooks
    *   Executive Sign-off Dashboard
    *   **30-Day Data Retention**
    """)
    # Button removed as per request


with col2:
    st.markdown("#### 🌍 Enterprise Annual License")
    st.markdown("## £25,000 <span style='font-size:0.6em'>/ year</span>", unsafe_allow_html=True)
    st.markdown("""
    *   **Unlimited Launches**
    *   Priority Support (24/7)
    *   Custom Rule Definitions
    *   API Access for CI/CD Integration
    *   **Permanent Data Retention**
    """)
    # Button removed as per request


st.markdown("---")
st.markdown("### 🛡️ Payment Security")
st.markdown("""
*   All transactions are processed via secure 256-bit SSL encryption.
*   We do not store your credit card details.
*   Invoices are VAT compliant.
""")

render_footer()
