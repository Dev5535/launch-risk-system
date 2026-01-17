import streamlit as st
import sys
import os

import urllib.parse

# Add parent dir to path to allow importing from web_ui
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from support_manager import SupportManager
from layout import render_support_sidebar, render_footer

st.set_page_config(page_title="Settings & Support", page_icon="⚙️", layout="wide")

render_support_sidebar()

st.title("⚙️ Settings & Support Center")

tab1, tab2, tab3 = st.tabs(["Report an Issue", "System Info", "Feedback"])

manager = SupportManager()
SUPPORT_EMAIL = "devshahsasu1211@gmail.com"

with tab3:
    st.markdown("### Give Us Your Feedback")
    st.info("Your feedback helps us build a better risk intelligence platform.")
    
    with st.form("feedback_form"):
        rating = st.slider("How would you rate the Launch Risk Intelligence System?", 1, 5, 5)
        category = st.selectbox("What is this feedback about?", ["User Interface", "Features", "Performance", "Accuracy", "Other"])
        comments = st.text_area("Comments", placeholder="Tell us what you like or what needs improvement...")
        
        submitted_feedback = st.form_submit_button("Submit Feedback")
        
        if submitted_feedback:
            feedback_data = {
                "rating": rating,
                "category": category,
                "comments": comments
            }
            success, msg = manager.submit_feedback(feedback_data)
            if success:
                st.success(msg)
                st.balloons()
                
                # Generate Mailto Link for Feedback
                subject = f"System Feedback: {category} ({rating}/5 Stars)"
                body = f"""
Rating: {rating}/5 Stars
Category: {category}

Comments:
{comments}

(Sent from Launch Risk Intelligence System)
"""
                # URL encode
                subject_enc = urllib.parse.quote(subject)
                body_enc = urllib.parse.quote(body)
                mailto_link = f"mailto:{SUPPORT_EMAIL}?subject={subject_enc}&body={body_enc}"
                
                st.markdown(f"""
                <div style="background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <strong>📧 Send Feedback to Admin:</strong><br>
                    Please click the button below to ensure your feedback is emailed directly to the developer.
                    <br><br>
                    <a href="{mailto_link}" target="_blank" style="background-color: #28a745; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; font-weight: bold;">📩 Open Email Client to Send</a>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(msg)

with tab1:
    st.markdown("### Submit a Support Ticket")
    st.info(f"We value your feedback. Tickets are logged locally and can be sent to **{SUPPORT_EMAIL}**.")
    
    with st.form("support_ticket_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            issue_type = st.selectbox("Issue Type", ["Bug / Error", "Feature Request", "Security Vulnerability", "Data Discrepancy", "Other"])
            module = st.selectbox("Affected Module", [
                "General / System-wide",
                "Digital Twin Auditor (P1)",
                "Risk Audit Engine (P2)",
                "Compliance Mapper (P3)",
                "Remediation Workflow (P4)",
                "Readiness Scorer (P5)"
            ])
            
        with col2:
            severity = st.selectbox("Severity Level", ["Low (Cosmetic)", "Medium (Workaround available)", "High (Feature broken)", "Critical (System down)"])
            contact_email = st.text_input("Your Contact Email", placeholder="you@company.com")
            
        description = st.text_area("Description", placeholder="Steps to reproduce, expected behavior, and what actually happened...", height=150)
        
        # Hidden metadata preview
        with st.expander("View Attached System Metadata"):
            meta = manager.get_system_metadata()
            st.json(meta)
            
        submitted = st.form_submit_button("Submit & Log Report")
        
        if submitted:
            if not description:
                st.error("Please provide a description.")
            else:
                ticket_data = {
                    "type": issue_type,
                    "module": module,
                    "severity": severity,
                    "email": contact_email,
                    "description": description
                }
                
                success, msg = manager.submit_ticket(ticket_data)
                if success:
                    st.success("✅ Report logged locally!")
                    st.toast(msg)
                    
                    # Generate Mailto Link
                    subject = f"Support Ticket: {issue_type} - {module}"
                    body = f"""
Issue Type: {issue_type}
Module: {module}
Severity: {severity}
Reporter: {contact_email}

Description:
{description}

System Metadata:
{meta}
"""
                    # URL encode
                    subject_enc = urllib.parse.quote(subject)
                    body_enc = urllib.parse.quote(body)
                    mailto_link = f"mailto:{SUPPORT_EMAIL}?subject={subject_enc}&body={body_enc}"
                    
                    st.markdown(f"""
                    <div style="background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        <strong>📧 Send to Support Team:</strong><br>
                        Since this is a local instance, please click the button below to email the report directly to the admin.
                        <br><br>
                        <a href="{mailto_link}" target="_blank" style="background-color: #28a745; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; font-weight: bold;">📩 Open Email Client to Send</a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.error(f"❌ Error submitting report: {msg}")

with tab2:
    st.markdown("### System Configuration")
    st.write("Current Environment:")
    st.code(f"""
    OS: {os.name}
    Python: {sys.version.split()[0]}
    Working Directory: {os.getcwd()}
    """, language="text")
    
    st.markdown("### Recent Local Tickets (Audit Log)")
    tickets = manager.get_recent_tickets()
    if tickets:
        st.table(tickets)
    else:
        st.caption("No local tickets found.")

render_footer()
