import streamlit as st
from services import api_client
from utils.session import get_token, logout
from components.conversation_list import refresh_conversations, render_conversation_list

MODELS = ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4-turbo"]


def render_sidebar(on_new_chat, on_select_conversation):
    with st.sidebar:
        st.markdown("<h2 style='text-align:center'>💬 AI Chatbot</h2>", unsafe_allow_html=True)
        st.divider()

        if st.button("＋ New Chat", use_container_width=True, type="primary"):
            on_new_chat()

        model = st.selectbox("Model", MODELS, index=0, key="selected_model")

        st.divider()
        st.subheader("Conversations")

        refresh_conversations()
        render_conversation_list(
            on_select=on_select_conversation,
            on_delete=_delete_conversation,
        )

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

    return model


def _delete_conversation(conversation_id: int) -> None:
    token = get_token()
    if not token:
        return
    try:
        api_client.delete_conversation(token, conversation_id)
        if st.session_state.get("conversation_id") == conversation_id:
            st.session_state.conversation_id = None
            st.session_state.messages = []
        refresh_conversations()
        st.rerun()
    except Exception as e:
        st.error(f"Could not delete conversation: {e}")
