import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from utils.session import is_logged_in

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "page" not in st.session_state:
    st.session_state.page = "login"

if is_logged_in():
    from pages.chat import render_chat
    render_chat()
else:
    if st.session_state.page == "register":
        from pages.register import render_register
        _, col, _ = st.columns([1, 2, 1])
        with col:
            render_register()
    else:
        from pages.login import render_login
        _, col, _ = st.columns([1, 2, 1])
        with col:
            render_login()
