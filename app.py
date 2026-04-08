import streamlit as st

# MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="GenAI Assistant Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.session_manager import init_session
from ui.theme import inject_theme
from auth.login import render_login
from auth.signup import render_signup
from ui.dashboard import render_dashboard
from database.init_db import init_db
import os
import time

def check_oauth_redirect():
    """Checks if the user returned from Google OAuth and logs them in."""
    # Catch both standard query_params (st>=1.30)
    query_params = st.query_params
    code = query_params.get("code")
    
    if code:
        from auth.oauth_utils import exchange_code_for_user_info
        from auth.auth_utils import get_or_create_google_user
        from utils.session_manager import login_session
        
        with st.spinner("Authenticating with Google..."):
            user_info, error = exchange_code_for_user_info(code)
            
            if error:
                st.error(f"Google Login Failed: {error}")
            elif user_info and "email" in user_info:
                email = user_info["email"]
                name = user_info.get("name", "Google User")
                
                # Fetch or auto-register safely
                user = get_or_create_google_user(email, name)
                if user:
                    login_session(user)
                    st.success("Successfully logged in with Google!")
            
            # Clear URL so it doesn't try assigning code on refresh
            st.query_params.clear()
            st.rerun()

def main():
    # Attempt to initialize DB if not exists
    if not os.path.exists("database/app.db"):
        init_db()

    # Intercept OAuth Code FIRST
    check_oauth_redirect()

    # Rehydrate session via cookies 
    init_session()
    
    # Inject Custom UI
    inject_theme()
    
    if st.session_state.get('authenticated'):
        render_dashboard()
    else:
        # Auth routing
        if st.session_state.get('current_page') == 'signup':
            render_signup()
        else:
            render_login()

if __name__ == "__main__":
    main()
