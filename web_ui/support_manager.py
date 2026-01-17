import json
import os
import datetime
import streamlit as st

class SupportManager:
    def __init__(self, log_file="support_tickets.jsonl", feedback_file="feedback_log.jsonl"):
        self.log_file = log_file
        self.feedback_file = feedback_file

    def get_system_metadata(self):
        """Auto-collects system metadata for the report."""
        return {
            "app_version": "1.0.0-beta", # Assuming version
            "timestamp": datetime.datetime.now().isoformat(),
            "platform": os.name,
            "user_session_id": str(getattr(st.session_state, 'user_id', 'anonymous')),
            # Try to get readiness score if available in session state
            "readiness_score": st.session_state.get('readiness_score', 'Not Calculated')
        }

    def submit_ticket(self, ticket_data):
        """
        Saves the ticket to a local JSONL file and simulates sending an email.
        ticket_data: dict containing user inputs
        """
        metadata = self.get_system_metadata()
        full_record = {**metadata, **ticket_data, "status": "OPEN"}
        
        # 1. Save to local log file (Audit Trail)
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(full_record) + "\n")
        except Exception as e:
            return False, f"Failed to save local log: {e}"

        # 2. Simulate Email Sending (as per "no external APIs" rule)
        # In a real app, this would use smtplib or an API call.
        # We just return success here.
        
        return True, f"Ticket #{id(full_record)} logged and queued for support team."

    def submit_feedback(self, feedback_data):
        """
        Saves feedback to a local JSONL file.
        feedback_data: dict containing user rating and comments
        """
        metadata = self.get_system_metadata()
        full_record = {**metadata, **feedback_data}
        
        try:
            with open(self.feedback_file, "a") as f:
                f.write(json.dumps(full_record) + "\n")
        except Exception as e:
            return False, f"Failed to save feedback: {e}"
            
        return True, "Feedback received! Thank you for helping us improve."

    def get_recent_tickets(self, limit=5):
        """Retrieves recent tickets for display (optional)."""
        tickets = []
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                for line in f:
                    try:
                        tickets.append(json.loads(line))
                    except:
                        pass
        return tickets[-limit:]
