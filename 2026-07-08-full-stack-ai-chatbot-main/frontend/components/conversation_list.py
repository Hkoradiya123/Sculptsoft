import streamlit as st
from services import api_client
from utils.session import get_token


def refresh_conversations() -> None:
    token = get_token()
    if token:
        try:
            st.session_state.conversations = api_client.get_conversations(token)
        except Exception:
            st.session_state.conversations = []


def render_conversation_list(on_select, on_delete) -> None:
    conversations = st.session_state.get("conversations", [])
    active_id = st.session_state.get("conversation_id")

    for convo in conversations:
        cols = st.columns([6, 1])
        with cols[0]:
            label = convo["title"] or "Untitled"
            is_active = convo["id"] == active_id
            if st.button(
                label,
                key=f"convo_{convo['id']}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                on_select(convo["id"])
        with cols[1]:
            if st.button("🗑", key=f"del_{convo['id']}"):
                on_delete(convo["id"])
