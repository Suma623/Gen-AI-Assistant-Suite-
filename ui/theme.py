import streamlit as st

def inject_theme():
    """
    Injects the unified custom CSS based on native prefers-color-scheme logic.
    """
    try:
        import os
        css_file = os.path.join(os.path.dirname(__file__), '..', 'styles', 'custom.css')
        with open(css_file, "r") as f:
            css_contents = f.read()
            # Storing it strictly globally
            st.markdown(f'<style>{css_contents}</style>', unsafe_allow_html=True)
            
    except Exception as e:
        pass
