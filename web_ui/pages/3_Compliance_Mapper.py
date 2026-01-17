import streamlit as st
import sys
import os
import json
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Add web_ui to path for layout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from product_3_compliance_mapper.src.engine import RulesEngine
from layout import render_support_sidebar, render_footer

st.set_page_config(page_title="Compliance Mapper", page_icon="⚖️")

render_support_sidebar()

st.header("⚖️ Product 3: Dynamic Regulatory Compliance Mapper")
st.markdown("**User:** Compliance Officers / Legal | **Goal:** Generate Custom Readiness Checklists")

# UI Selector
st.sidebar.header("Context Selectors")

industry = st.sidebar.selectbox("Target Industry", ["Healthcare", "Finance", "SaaS", "E-commerce", "Government"])
regions = st.sidebar.multiselect("Operating Regions", ["EU", "US", "Global", "CA"], default=["US"])
data_types = st.sidebar.multiselect("Data Types Handled", ["PII", "Health", "Financial", "Technical"], default=["PII"])

if st.button("🗺️ Generate Compliance Map"):
    # Load Rules
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    rules_path = os.path.join(base_dir, 'product_3_compliance_mapper', 'src', 'data', 'rules.json')
    
    engine = RulesEngine(rules_path)
    
    context = {
        'industry': industry,
        'region': regions,
        'data_types': data_types
    }
    
    results = engine.evaluate(context)
    st.session_state['p3_report'] = results
    
    # Display
    st.subheader("Applicable Regulations")
    st.write(f"Based on your profile, you are subject to: **{', '.join(results['regulations'])}**")
    
    st.subheader("📋 Readiness Checklist")
    
    checklist = results['checklist']
    if not checklist:
        st.info("No specific requirements triggered for this profile.")
    else:
        # Custom rendering for checklist
        for item in checklist:
            priority_color = "red" if item['priority'] == 'Critical' else "orange" if item['priority'] == 'High' else "blue"
            
            with st.expander(f"[{item['regulation']}] {item['title']} ({item['priority']})"):
                st.markdown(f"**Description:** {item['description']}")
                st.markdown(f"**Required Action:** `{item['action']}`")
                st.caption(f"ID: {item['id']}")
    
    # DataFrame View for Export
    st.markdown("---")
    st.subheader("Export View")
    df = pd.DataFrame(checklist)
    if not df.empty:
        st.dataframe(df[['id', 'regulation', 'title', 'priority', 'action']])
        
        st.download_button(
            label="📥 Download Compliance Map JSON",
            data=json.dumps(results, indent=2),
            file_name="p3_compliance_map.json",
            mime="application/json"
        )

# Trust Centre Portal (Read-Only View)
if st.checkbox("Show Trust Centre Preview"):
    st.divider()
    st.subheader("🔒 Trust Centre & External Assurance Portal")
    st.info("This view is intended for external auditors or customers.")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://placehold.co/150x150?text=Security+Seal", caption="Certified Secure")
        st.metric("Audit Readiness", "85%", "High")
    
    with col2:
        st.markdown("### Compliance Posture Summary")
        if 'p3_report' in st.session_state and st.session_state['p3_report']:
            regs = st.session_state['p3_report'].get('regulations', [])
            st.write(f"This organization is aligned with: **{', '.join(regs)}**")
            
            st.markdown("#### Public Controls")
            # Show simplified view of controls without sensitive details
            public_controls = []
            if 'checklist' in st.session_state['p3_report']:
                for item in st.session_state['p3_report']['checklist']:
                    public_controls.append({
                        "Control ID": item['id'],
                        "Standard": item['regulation'],
                        "Status": "Implemented" # Mock status
                    })
            st.table(pd.DataFrame(public_controls))
        else:
            st.write("No compliance data available. Please run the mapper first.")

render_footer()
