import streamlit as st
from utils.constants import DOMAINS, STYLES
from ui.profile_menu import render_profile_menu
from ui.cards import render_response_card
from features.file_upload import handle_uploaded_file
from features.suggested_prompts import get_suggested_prompts
from features.timestamps import get_current_timestamp
from domains.domain_validator import validate_domain_mismatch
from ai.response_handler import handle_query
from database.db_utils import save_chat, get_user_chat_history, get_user_bookmarks

def render_history_sidebar():
    st.sidebar.markdown("### 📝 Recent History")
    history = get_user_chat_history(st.session_state['user']['id'])
    if not history:
        st.sidebar.markdown("<p style='color:gray;'>No previous chats found.</p>", unsafe_allow_html=True)
    
    for chat in history[:5]: # Show last 5
        with st.sidebar.expander(f"{chat['domain']}: {chat['query'][:20]}..."):
            st.write(chat['response'][:80] + "...")
            
    st.sidebar.markdown("### 🏷️ Bookmarks")
    bookmarks = get_user_bookmarks(st.session_state['user']['id'])
    if not bookmarks:
        st.sidebar.markdown("<p style='color:gray;'>No saved bookmarks.</p>", unsafe_allow_html=True)
        
    for b in bookmarks[:5]:
        with st.sidebar.expander(f"📌 {b['domain']}: {b['query'][:15]}..."):
            st.write(b['response'][:80] + "...")

def render_dashboard():
    # Sidebar rendering
    render_profile_menu()
    render_history_sidebar()
    
    # Outer container to prevent ugly full-width stretch on ultra-wide monitors
    with st.container():
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: var(--primary-color);'>GenAI Assistant Suite</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: var(--text-muted); margin-bottom: 2rem;'>Your smart, localized companion across domain-specific expert roles.</p>", unsafe_allow_html=True)
        
        # Configuration Row Wrapper
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                selected_domain = st.selectbox("🎯 Select Context Domain", DOMAINS)
            with col2:
                selected_style = st.selectbox("🎭 Response Output Style", STYLES)
                
            # Optional Upload Expander
            with st.expander("📎 Attach Context (PDF, TXT, Image)"):
                st.markdown("<p style='font-size: 0.85rem; color: var(--text-muted);'>You can drag and drop your file below. We support document extraction and image vision!</p>", unsafe_allow_html=True)
                uploaded_file = st.file_uploader("", type=["pdf", "txt", "png", "jpg", "jpeg"], label_visibility="collapsed")
        
        # Suggested prompt chips mapping to buttons securely
        st.markdown("<br><p style='font-weight: 500; margin-bottom: 4px;'>Try asking:</p>", unsafe_allow_html=True)
        suggestions = get_suggested_prompts(selected_domain)
        
        scol1, scol2, scol3 = st.columns(3)
        if scol1.button(suggestions[0], use_container_width=True): st.session_state['chip_query'] = suggestions[0]
        if scol2.button(suggestions[1], use_container_width=True): st.session_state['chip_query'] = suggestions[1]
        if scol3.button(suggestions[2], use_container_width=True): st.session_state['chip_query'] = suggestions[2]

        # Input Area
        query_default = st.session_state.get('chip_query', "")
        query = st.text_area("What do you need help with?", value=query_default, height=140, placeholder="Type your query for the AI here...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit Button Centered cleanly
        if st.button("🚀 Ask GenAI", use_container_width=True, type="primary"):
            if not query.strip():
                st.warning("Please enter a query.")
                return
                
            mismatch_warning = validate_domain_mismatch(selected_domain, query)
            if mismatch_warning:
                st.warning(mismatch_warning)
                
            with st.spinner("🤖 Processing with Gemini..."):
                # Pass data to logic
                file_context, image_obj, ftype, ferror = handle_uploaded_file(uploaded_file)
                
                if ferror:
                    st.error(ferror)
                    return
                    
                response = handle_query(
                    domain=selected_domain,
                    style=selected_style,
                    query=query,
                    file_context=file_context,
                    image_file=image_obj
                )
                
                # Save execution
                timestamp = get_current_timestamp()
                chat_id = save_chat(
                    user_id=st.session_state['user']['id'],
                    domain=selected_domain,
                    query=query,
                    response=response,
                    file_context="Yes" if uploaded_file else "None"
                )
                
                st.session_state['last_response'] = {
                    'chat_id': chat_id,
                    'domain': selected_domain,
                    'timestamp': timestamp,
                    'query': query,
                    'response': response
                }
                
                # Clear chips and re-run UI
                st.session_state['chip_query'] = ""

        # Last Output Results Rendering Below
        if 'last_response' in st.session_state:
            lr = st.session_state['last_response']
            render_response_card(
                lr['chat_id'], lr['domain'], lr['timestamp'], lr['query'], lr['response'], st.session_state['user']['id']
            )
