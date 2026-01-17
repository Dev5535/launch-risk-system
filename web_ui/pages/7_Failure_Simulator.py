import streamlit as st
import sys
import os

# Add project root to path to allow importing from product_6
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from product_6_failure_simulator.src.simulator import FailureSimulator
from web_ui.layout import render_support_sidebar

st.set_page_config(page_title="Failure Simulator", page_icon="💥", layout="wide")

# Initialize Simulator
if 'simulator' not in st.session_state:
    st.session_state['simulator'] = FailureSimulator()

render_support_sidebar()

st.title("💥 Failure Simulation Platform")
st.markdown("### The 'What-If' Engine for Decision Assurance")

# --- STAGE 4: METHODOLOGY & TRUST ---
with st.expander("ℹ️ How This Works (Methodology & Trust)", expanded=False):
    st.markdown("""
    **Methodology:**
    This system uses **Deterministic Dependency Modeling** to simulate failure scenarios based on architectural definitions. 
    
    **Constraints & Safety:**
    - ✅ **Hypothetical Simulation:** No live systems are touched, probed, or stressed.
    - ✅ **No Exploitation:** This is not a chaos monkey or penetration test tool.
    - ✅ **No Data Access:** Simulations run entirely on abstract models, not customer data.
    
    **Goal:** Provide clarity and decision confidence before irreversible actions.
    """)

# --- STAGE 1: SCENARIO SELECTION ---
st.sidebar.header("Scenario Parameters")

scenario_type = st.sidebar.selectbox(
    "1. Select Failure Type",
    ["Service Outage", "Configuration Error", "Human Mistake", "Traffic Spike", "Dependency Failure", "Compliance Slip"]
)

component = st.sidebar.selectbox(
    "2. Affected Component",
    ["Database", "Auth Service", "Payment Gateway", "CDN", "Logging Service", "API Gateway"]
)

redundancy = st.sidebar.selectbox(
    "3. Redundancy Level",
    ["None", "Medium (Active-Passive)", "High (Active-Active)"]
)

# --- EXECUTION ---
if st.button("🚀 Run Simulation", type="primary"):
    with st.spinner("Modeling failure cascades..."):
        result = st.session_state['simulator'].simulate(scenario_type, component, redundancy)
        st.session_state['sim_result'] = result

# --- RESULTS DISPLAY ---
if 'sim_result' in st.session_state:
    res = st.session_state['sim_result']
    
    st.divider()
    
    # --- STAGE 2: IMPACT MODELING & BLAST RADIUS ---
    st.subheader("⚠️ Impact Analysis & Blast Radius")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Primary Impact", "Confirmed", delta="-Critical")
    with col2:
        st.metric("Cascading Systems", len(res['secondary_impacts']), delta="Affected")
    with col3:
        st.metric("Est. Recovery Time", f"{res['ttr_estimate_mins']} min", delta_color="inverse")
    with col4:
        st.metric("Blast Radius Level", res['blast_radius_level'], delta_color="off")
        
    st.markdown(f"**Primary Vector:** {res['primary_impact']}")
    if res['secondary_impacts']:
        st.markdown("**Cascading Effects:**")
        for impact in res['secondary_impacts']:
            st.markdown(f"- 🔴 {impact}")
            
    st.divider()
    
    # --- STAGE 3 & 4: DECISION BRIEF & OUTPUT MODES ---
    st.subheader("📋 Decision Brief")
    
    mode = st.radio("Select Output Mode:", ["Executive", "Policy"], horizontal=True, help="Switch between concise decision support and formal audit language.")
    
    brief = st.session_state['simulator'].generate_brief(res, mode)
    
    # Styled display for the brief
    st.code(brief, language="markdown")
    
    # Confidence Score Visualization
    st.progress(res['confidence_score'] / 100, text=f"Simulation Confidence Score: {res['confidence_score']}/100")
    
    if res['confidence_score'] > 75:
        st.success("✅ **Recommendation: PROCEED.** Risk controls appear sufficient.")
    elif res['confidence_score'] > 50:
        st.warning("⚠️ **Recommendation: PROCEED WITH CAUTION.** Review mitigations.")
    else:
        st.error("🛑 **Recommendation: DELAY.** Risk exposure exceeds safety thresholds.")

    st.caption("Disclaimer: This is a deterministic decision-support model. Real-world outcomes may vary based on unmodeled variables.")

else:
    st.info("👈 Configure a scenario in the sidebar and click 'Run Simulation' to see the impact model.")
