import streamlit as st
from services import api_client
from utils.session import set_auth


def render_login():
    st.markdown("<h1 style='text-align:center'>🤖 AI Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray'>Sign in to start chatting</p>", unsafe_allow_html=True)
    st.divider()

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

    if submitted:
        if not email or not password:
            st.error("Please enter email and password.")
            return
        try:
            data = api_client.login(email, password)
            set_auth(data["access_token"], data["refresh_token"])
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center'>Don't have an account? "
        "<a href='#' onclick=''>Register below</a></p>",
        unsafe_allow_html=True,
    )
    if st.button("Create an account →", use_container_width=True):
        st.session_state.page = "register"
        st.rerun()
