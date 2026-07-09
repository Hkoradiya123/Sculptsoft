import streamlit as st
from services import api_client
from utils.session import get_token, init_chat_state
from components.sidebar import render_sidebar
from components.chat_window import render_messages


def render_chat():
    init_chat_state()
    token = get_token()

    def new_chat():
        st.session_state.conversation_id = None
        st.session_state.messages = []

    def select_conversation(conversation_id: int):
        try:
            msgs = api_client.get_messages(token, conversation_id)
            st.session_state.conversation_id = conversation_id
            st.session_state.messages = [{"role": m["role"], "content": m["content"]} for m in msgs]
        except Exception as e:
            st.error(f"Could not load messages: {e}")
        st.rerun()

    model = render_sidebar(on_new_chat=new_chat, on_select_conversation=select_conversation)

    convo_id = st.session_state.get("conversation_id")
    if convo_id:
        convo_list = st.session_state.get("conversations", [])
        title = next((c["title"] for c in convo_list if c["id"] == convo_id), "Conversation")
        st.subheader(title)
    else:
        st.subheader("New Chat")

    render_messages(st.session_state.messages)

    prompt = st.chat_input("Type your message...")

    if prompt:
        try:
            if convo_id is None:
                convo = api_client.create_conversation(token, title=prompt[:50].strip())
                convo_id = convo["id"]
                st.session_state.conversation_id = convo_id
                st.session_state.conversations = api_client.get_conversations(token)

            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""
                try:
                    for chunk in api_client.send_message_stream(token, convo_id, prompt, model):
                        full_response += chunk
                        placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)
                except Exception:
                    response = api_client.send_message(token, convo_id, prompt, model)
                    full_response = response["content"]
                    placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {e}")
