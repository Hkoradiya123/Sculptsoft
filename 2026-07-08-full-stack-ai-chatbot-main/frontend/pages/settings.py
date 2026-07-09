import streamlit as st
from utils.session import get_token
from services import api_client


def render_settings():
    st.title("⚙️ Settings")
    st.divider()

    st.subheader("API Connection")
    st.info("Backend: http://localhost:8000")
    if st.button("Test Connection"):
        try:
            import requests
            r = requests.get("http://localhost:8000/health", timeout=5)
            if r.ok:
                st.success(f"Connected — {r.json()}")
            else:
                st.error(f"Backend returned {r.status_code}")
        except Exception as e:
            st.error(f"Cannot reach backend: {e}")
