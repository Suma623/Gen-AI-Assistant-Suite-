import streamlit as st
import time
from database.db_utils import save_feedback, bookmark_chat
from features.pdf_export import create_pdf

def render_response_card(chat_id: int, domain: str, timestamp: str, query: str, response: str, user_id: int):
    """
    Renders a beautifully styled response card with native actions securely nested underneath.
    """
    # Protect against any unhandled character entities
    safe_query = query.replace('<', '&lt;').replace('>', '&gt;')
    # We output the response via Streamlit Markdown rather than purely raw HTML 
    # to preserve native Streamlit markdown formatting (bolds, code blocks etc.)
    
    html_header = f"""
    <div class="ai-response-card">
        <div class="ai-card-header">
            <span class="ai-domain-badge">{domain}</span>
            <span class="ai-timestamp">{timestamp}</span>
        </div>
        <div class="ai-card-body">
            <strong>Query:</strong> {safe_query}
        </div>
    </div>
    """
    st.markdown(html_header, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(response)

        # Action Buttons Layout Configuration
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns([1, 1, 1, 1, 1, 3])
        
        with cols[0]:
            if st.button("💾 Save", key=f"save_{chat_id}", help="Bookmark this response"):
                if bookmark_chat(user_id, chat_id):
                    st.toast("Saved to bookmarks!")
                else:
                    st.toast("Already saved.")
                    
        with cols[1]:
            pdf_bytes = create_pdf(domain, timestamp, query, response)
            st.download_button(
                label="📄 PDF",
                data=pdf_bytes,
                file_name=f"{domain}_Response_{chat_id}.pdf",
                mime="application/pdf",
                key=f"pdf_{chat_id}",
                help="Download response as PDF"
            )
            
        with cols[2]:
            share_text = f"Check out this answer I got from GenAI ({domain}):\n\nQ: {query}\n\nA: {response}"
            if st.button("🔗 Share", key=f"share_{chat_id}", help="Get shareable link"):
                st.session_state[f'share_text_{chat_id}'] = share_text
                
        with cols[3]:
            if st.button("👍", key=f"up_{chat_id}", help="Mark as helpful"):
                save_feedback(user_id, chat_id, True, "")
                st.toast("Thanks for the feedback!")
                
        with cols[4]:
            if st.button("👎", key=f"down_{chat_id}", help="Mark as unhelpful"):
                save_feedback(user_id, chat_id, False, "")
                st.toast("Thanks for the feedback!")
                
        if f'share_text_{chat_id}' in st.session_state:
            st.text_area("Copy this text to share:", value=st.session_state[f'share_text_{chat_id}'], height=100)
