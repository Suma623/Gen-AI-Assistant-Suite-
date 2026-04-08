import streamlit as st
from auth.auth_utils import register_user

def render_signup():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('''
            <div class="auth-card">
                <h2 style='text-align: center; margin-bottom: 0px;'>Create Account</h2>
                <p style='text-align: center; color: var(--text-muted); margin-top: 0px;'>Join the GenAI Ecosystem</p>
            </div>
        ''', unsafe_allow_html=True)

        with st.form("signup_form"):
            username = st.text_input("Username", placeholder="Enter username")
            email = st.text_input("Email (Optional)", placeholder="Enter email")
            password = st.text_input("Password", type="password", placeholder="Create password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
            
            submit = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Username and Password are required.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, msg = register_user(username, email, password)
                    if success:
                        st.success("Account created successfully! Please login.")
                        st.session_state['current_page'] = 'login'
                        st.rerun()
                    else:
                        st.error(f"Signup failed: {msg}")

        st.markdown("---")
        
        scol1, scol2 = st.columns([3, 2])
        with scol1:
            st.markdown("<p style='margin-top: 5px; color: var(--text-muted);'>Already have an account?</p>", unsafe_allow_html=True)
        with scol2:
            if st.button("Login here", use_container_width=True):
                st.session_state['current_page'] = 'login'
                st.rerun()
