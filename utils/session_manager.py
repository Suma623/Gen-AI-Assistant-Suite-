import streamlit as st
import json
from streamlit_cookies_controller import CookieController

# Global cookie controller initialization
# Must be instantiated near the top before use
if 'cookie_controller' not in st.session_state:
    st.session_state['cookie_controller'] = CookieController()

def get_cookie_controller():
    # Attempt to retrieve, if it fails return the session one
    return CookieController()

def init_session():
    """Initializes default Streamlit session state variables and reads cookies."""
    controller = get_cookie_controller()
    
    # Check cookies first safely
    try:
        stored_auth = controller.get('auth_status')
        stored_user_str = controller.get('auth_user')
        stored_theme = controller.get('theme')
    except Exception:
        stored_auth = None
        stored_user_str = None
        stored_theme = None

    # Rehydrate authenticated state dynamically 
    # (to catch cookies mounting late on F5 refreshes)
    if stored_auth == 'true' and stored_user_str:
        try:
            st.session_state['authenticated'] = True
            st.session_state['user'] = json.loads(stored_user_str)
            st.session_state['current_page'] = 'dashboard'
        except Exception:
            if 'authenticated' not in st.session_state:
                st.session_state['authenticated'] = False
    else:
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False

    # Standard Defaults
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'dashboard' if st.session_state.get('authenticated') else 'login'
        
    if 'user' not in st.session_state:
        st.session_state['user'] = None
        
    if 'theme' not in st.session_state:
        st.session_state['theme'] = stored_theme if stored_theme else 'dark'
        
    if 'chat_history_cache' not in st.session_state:
        st.session_state['chat_history_cache'] = []

def login_session(user_dict):
    """Sets session state and cookies for login."""
    controller = CookieController()
    st.session_state['user'] = user_dict
    st.session_state['authenticated'] = True
    st.session_state['current_page'] = 'dashboard'
    
    controller.set('auth_status', 'true')
    controller.set('auth_user', json.dumps(user_dict))

def logout_session():
    """Clears session state and cookies."""
    controller = CookieController()
    try:
        controller.remove('auth_status')
        controller.remove('auth_user')
    except Exception:
        pass
    
    st.session_state['user'] = None
    st.session_state['authenticated'] = False
    st.session_state['current_page'] = 'login'

def save_theme_preference(theme_val):
    st.session_state['theme'] = theme_val
    controller = CookieController()
    controller.set('theme', theme_val)
