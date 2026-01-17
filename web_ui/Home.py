import streamlit as st
import os
from layout import render_support_sidebar, render_footer

st.set_page_config(
    page_title="Launch Risk Intelligence",
    page_icon="🚀",
    layout="wide"
)

render_support_sidebar()

st.title("🚀 Launch Risk Intelligence System")
st.markdown("### The Non-AI, Explainable Decision Engine for Enterprise Launches")

st.markdown("""
---
**Welcome to the Central Command Center.**

This suite provides 6 evidence-backed products to ensure your software launch is risk-free and compliant.
Please navigate using the sidebar to access specific modules.

#### Product Suite Overview

| Module | Target User (Expanded) | Function |
| :--- | :--- | :--- |
| **1. Digital Twin Auditor** | IT Manager, DevOps, Cloud Architects, SREs | Compares Staging vs. Production environments to detect drift. |
| **2. Risk Audit Engine** | Project Leads, Analysts, QA & Security Engineers | Scans for SEO, Security, and Stability risks. |
| **3. Compliance Mapper** | Legal, Compliance, DPOs, Risk Managers | Generates regulatory checklists (GDPR, HIPAA, SOC2). |
| **4. Remediation Engine** | Developers, Tech Leads, Engineering Managers | Converts findings into actionable "Fix-It-Yourself" runbooks. |
| **5. Executive Dashboard** | C-Suite, VPs, Board Members, Directors | Final Go/No-Go readiness scoring and sign-off. |
| **6. Failure Simulator** | Architects, Risk Officers, Executives | "What-if" scenario modeling for impact & blast radius analysis. |

---
*System Status: Online* 🟢 (Operational)
""")

# Session State Initialization for passing data between pages
if 'p1_report' not in st.session_state: st.session_state['p1_report'] = None
if 'p2_report' not in st.session_state: st.session_state['p2_report'] = None
if 'p3_report' not in st.session_state: st.session_state['p3_report'] = None

render_footer()
