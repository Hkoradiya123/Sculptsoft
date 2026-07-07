
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import streamlit as st

client = OpenAI()
model = "gpt-5.5"

instructions = """
You are a helpful assistant. Please provide clear and concise responses to the user's queries.
you only respond in plain/text format, without any markdown or code blocks.
you should not provide any explanations or additional information unless explicitly asked by the user.
"""


def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


def chat_stream(messages: list):
    return client.responses.create(
        model=model,
        input=messages,
        instructions=instructions,
        stream=True,
    )


# ── Streamlit UI ──────────────────────────────────────────────────────────────

st.title("AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    add_assistant_message(st.session_state.messages, "Hello, How can I assist you today?")

# Render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box at the bottom
user_input = st.chat_input("Type your message…")

if user_input:
    add_user_message(st.session_state.messages, user_input)
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        stream = chat_stream(st.session_state.messages)
        for event in stream:
            if event.type == "response.output_text.delta":
                full_response += event.delta
                placeholder.write(full_response)
        placeholder.write(full_response)

    add_assistant_message(st.session_state.messages, full_response)
