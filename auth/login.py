import streamlit as st
from auth.auth_utils import authenticate_user
from utils.session_manager import login_session

def render_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Empty columns to center the login box
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('''
            <div class="auth-card">
                <h2 style='text-align: center; margin-bottom: 0px;'>Welcome Back</h2>
                <p style='text-align: center; color: var(--text-muted); margin-top: 0px;'>Sign in to your GenAI Suite</p>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            submit = st.form_submit_button("Log In", type="primary", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please fill in both fields.")
                else:
                    user = authenticate_user(username, password)
                    if user:
                        login_session(user)
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                        
        st.markdown("---")
        
        from auth.oauth_utils import get_google_auth_url
        auth_url = get_google_auth_url()
        
        if auth_url:
            st.link_button("Continue with Google", auth_url, use_container_width=True)
        else:
            st.warning("Google Auth not fully configured in .env yet.")
            
        scol1, scol2 = st.columns([3, 2])
        with scol1:
            st.markdown("<p style='margin-top: 5px; color: var(--text-muted);'>Don't have an account?</p>", unsafe_allow_html=True)
        with scol2:
            if st.button("Sign up here", use_container_width=True):
                st.session_state['current_page'] = 'signup'
                st.rerun()
