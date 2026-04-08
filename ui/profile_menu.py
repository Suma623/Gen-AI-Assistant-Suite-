import streamlit as st
from database.db_utils import update_user_profile
from utils.session_manager import logout_session

@st.dialog("User Profile")
def open_profile_dialog():
    user = st.session_state.get('user', {})
    st.write(f"Logged in as: **{user.get('username')}**")
    
    new_display = st.text_input("Display Name", value=user.get('display_name') or "")
    if st.button("Save Profile"):
        update_user_profile(user['id'], display_name=new_display)
        st.session_state['user']['display_name'] = new_display
        st.success("Profile Updated!")
        st.rerun()

@st.dialog("About GenAI Assistant Suite")
def open_about_dialog():
    st.markdown("""
    ### GenAI Assistant Suite
    **Version:** 1.0.0  
    **Architecture:** Streamlit + SQLite + Gemini 2.5 Flash
    
    **Supported Domains:**
    - Education
    - Healthcare
    - Finance
    - Marketing
    
    **Safety Disclaimer:** Responses from Healthcare and Finance domains are for educational purposes. 
    Do not treat them as professional advice.
    """)

@st.dialog("Send Feedback")
def open_feedback_dialog():
    st.write("Help us improve the overall app experience!")
    fb = st.text_area("Feedback description")
    inc_ss = st.checkbox("Include page screenshot (Simulated)")
    
    if st.button("Submit"):
        st.success("Feedback submitted successfully! Thank you.")

@st.dialog("Confirm Logout")
def open_logout_dialog():
    st.write("Are you sure you want to log out?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Logout", use_container_width=True, type="primary"):
            logout_session()
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

def render_profile_menu():
    st.sidebar.markdown("---")
    user_name = st.session_state.get('user', {}).get('display_name') or st.session_state.get('user', {}).get('username')
    st.sidebar.markdown(f"### 👋 Hey, {user_name}")
    
    if st.sidebar.button("👤 Profile", use_container_width=True):
        open_profile_dialog()
        
    if st.sidebar.button("ℹ️ About App", use_container_width=True):
        open_about_dialog()
        
    if st.sidebar.button("📝 Setup/Feedback", use_container_width=True):
        open_feedback_dialog()
        
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        open_logout_dialog()
