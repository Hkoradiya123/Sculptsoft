import streamlit as st
from services import api_client


def render_register():
    st.markdown("<h1 style='text-align:center'>🤖 AI Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray'>Create your account</p>", unsafe_allow_html=True)
    st.divider()

    with st.form("register_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
        submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")

    if submitted:
        if not email or not password or not confirm:
            st.error("All fields are required.")
            return
        if password != confirm:
            st.error("Passwords do not match.")
            return
        if len(password) < 6:
            st.error("Password must be at least 6 characters.")
            return
        try:
            api_client.register(email, password)
            st.success("Account created! Please sign in.")
            st.session_state.page = "login"
            st.rerun()
        except Exception as e:
            st.error(f"Registration failed: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Sign In", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()
