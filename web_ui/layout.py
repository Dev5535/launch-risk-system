import streamlit as st

def render_support_sidebar():
    """
    Renders the standardized Support & Feedback sidebar section.
    Should be called at the top of every page.
    """
    with st.sidebar:
        st.markdown("---")
        st.header("Support Center")
        
        # Link to the main support page
        # Streamlit doesn't support direct linking easily without rerun hacks, 
        # but we can just guide them or use page_link if on newer streamlit.
        # Assuming newer streamlit for page_link, otherwise just text.
        try:
            st.page_link("pages/6_Settings_and_Support.py", label="Report an Issue", icon="⚠️")
        except AttributeError:
            st.info("Go to **Settings & Support** to report issues.")
            
        st.caption("Version 1.0.0-beta")
        st.caption("© 2025 Launch Risk Intelligence")

def render_footer():
    """
    Renders the deterministic system disclaimer.
    """
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8em;'>
            <strong>DISCLAIMER:</strong> This is a deterministic decision-support system. 
            Results are based on static analysis and predefined rules. 
            While high-precision, always verify critical findings manually. 
            <br>
            <a href='/Settings_and_Support' target='_self'>Report a Bug</a> | <a href='mailto:devshahsasu1211@gmail.com'>Contact Support</a>
        </div>
        """,
        unsafe_allow_html=True
    )
