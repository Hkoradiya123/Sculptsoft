import streamlit as st


def is_logged_in() -> bool:
    return bool(st.session_state.get("access_token"))


def get_token() -> str | None:
    return st.session_state.get("access_token")


def set_auth(access_token: str, refresh_token: str) -> None:
    st.session_state.access_token = access_token
    st.session_state.refresh_token = refresh_token


def logout() -> None:
    for key in ["access_token", "refresh_token", "conversation_id", "messages", "conversations"]:
        st.session_state.pop(key, None)


def init_chat_state() -> None:
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversations" not in st.session_state:
        st.session_state.conversations = []
