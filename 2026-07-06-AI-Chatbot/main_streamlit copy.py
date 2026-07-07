from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from openai import OpenAI

client = OpenAI()
model = "gpt-5.5"

instructions = """
You are a helpful assistant. Please provide clear and concise responses to the user's queries.
You should not provide any explanations or additional information unless explicitly asked by the user.
"""

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Chatbot")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello, How can I assist you today?"
        }
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
prompt = st.chat_input("Type your message...")

if prompt:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        stream = client.responses.create(
            model=model,
            input=st.session_state.messages,
            instructions=instructions,
            stream=True,
        )

        full_response = ""

        for event in stream:
            if event.type == "response.output_text.delta":
                full_response += event.delta
                response_placeholder.markdown(full_response)

        response_placeholder.write(full_response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
        }
    )

# Sidebar
with st.sidebar:

    st.header("Options")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello, How can I assist you today?"
            }
        ]
        st.rerun()