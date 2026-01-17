import streamlit as st
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Add web_ui to path for layout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from product_4_remediation_engine.src.engine import RemediationEngine
from product_4_remediation_engine.src.ingestor import ReportIngestor
from layout import render_support_sidebar, render_footer

st.set_page_config(page_title="Remediation Workflow", page_icon="🛠️")

render_support_sidebar()

st.header("🛠️ Product 4: Fix-It-Yourself Remediation Engine")
st.markdown("**User:** IT Staff / Developers | **Goal:** Actionable Runbooks & Workflows")

st.info("This module ingests reports from P1, P2, and P3 to generate code-level fixes.")

# Ingest Data
findings = []
ingestor = ReportIngestor()

# Load from Session State if available
if st.session_state.get('p1_report'):
    st.success("✅ P1 Report Loaded from Session")
    findings.extend(ingestor.load_report('p1_session_placeholder', 'p1') if False else ingestor._normalize_p1(st.session_state['p1_report']))

if st.session_state.get('p2_report'):
    st.success("✅ P2 Report Loaded from Session")
    findings.extend(ingestor.load_report('p2_session_placeholder', 'p2') if False else ingestor._normalize_p2(st.session_state['p2_report']))

if st.session_state.get('p3_report'):
    st.success("✅ P3 Report Loaded from Session")
    findings.extend(ingestor.load_report('p3_session_placeholder', 'p3') if False else ingestor._normalize_p3(st.session_state['p3_report']))

# Manual Upload Option
uploaded_file = st.file_uploader("Or Upload External Report (JSON)", type=['json'])
if uploaded_file:
    data = json.load(uploaded_file)
    # Simple heuristic to guess type
    if 'delta' in data:
        findings.extend(ingestor._normalize_p1(data))
    elif 'results' in data and 'checklist' in data['results']:
         findings.extend(ingestor._normalize_p3(data))
    elif 'results' in data:
         findings.extend(ingestor._normalize_p2(data))
    st.success(f"Loaded {len(findings)} findings from file.")

if not findings:
    st.warning("No findings loaded. Please run P1-P3 first or upload a report.")
else:
    st.markdown("---")
    st.subheader(f"⚡ Remediation Workflow ({len(findings)} Tasks)")
    
    # Generate Runbook
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    solutions_path = os.path.join(base_dir, 'product_4_remediation_engine', 'src', 'data', 'solutions.json')
    engine = RemediationEngine(solutions_path)
    
    runbook_md = engine.generate_runbook(findings)
    
    # Display Interactive Runbook
    # We can parse the MD or display it.
    # For "Workflow Manager", let's use checkboxes
    
    # Task Management State
    if 'tasks' not in st.session_state:
        st.session_state['tasks'] = {}
    
    tab_view, tab_kanban, tab_raw = st.tabs(["Interactive Workflow", "📋 Task Board", "Raw Markdown"])
    
    with tab_view:
        for idx, finding in enumerate(findings):
            task_id = f"task_{finding['id']}_{idx}"
            
            # Initialize task state if new
            if task_id not in st.session_state['tasks']:
                st.session_state['tasks'][task_id] = {
                    'status': 'Pending',
                    'assignee': 'Unassigned',
                    'due_date': None
                }
            
            task_data = st.session_state['tasks'][task_id]
            
            # UI Card
            with st.container():
                st.markdown(f"### {finding['id']}: {engine.solutions.get(finding['id'], {}).get('title', 'Issue Remediation')}")
                
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                     st.write(f"**Description:** {finding.get('description', 'No description')}")
                with c2:
                     new_status = st.selectbox("Status", ["Pending", "In Progress", "Review", "Done"], key=f"status_{task_id}", index=["Pending", "In Progress", "Review", "Done"].index(task_data['status']))
                     st.session_state['tasks'][task_id]['status'] = new_status
                with c3:
                     assignee = st.text_input("Assignee", value=task_data['assignee'], key=f"assignee_{task_id}")
                     st.session_state['tasks'][task_id]['assignee'] = assignee

                with st.expander("🛠️ Show Fix & Instructions"):
                    # Get solution content
                    sol = engine.solutions.get(finding['id'], {})
                    if sol:
                        st.markdown(f"**Remediation Type:** `{sol.get('type')}`")
                        st.info("Copy the code below to apply the fix:")
                        st.code(sol.get('content'), language=sol.get('lang', 'bash'))
                    else:
                        st.warning("No automated fix available. Please investigate manually.")
                        st.json(finding.get('context', {}))
                st.divider()

    with tab_kanban:
        st.subheader("Task Kanban Board")
        cols = st.columns(4)
        statuses = ["Pending", "In Progress", "Review", "Done"]
        
        for i, status in enumerate(statuses):
            with cols[i]:
                st.markdown(f"#### {status}")
                # Filter tasks by status
                for t_id, t_data in st.session_state['tasks'].items():
                    if t_data['status'] == status:
                        # Extract finding ID from task ID for label
                        f_id = t_id.split('_')[1]
                        st.info(f"**{f_id}**\n\n👤 {t_data['assignee']}")

    with tab_raw:
        st.text_area("Copy Markdown", runbook_md, height=400)
        st.download_button("📥 Download Runbook", runbook_md, file_name="remediation_runbook.md")

render_footer()
