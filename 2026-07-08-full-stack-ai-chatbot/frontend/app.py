from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from openai import OpenAI
from database.db import Conversation
from database.crud import (
    get_db,
    get_all_conversations,
    create_conversation,
    update_conversation_title,
    get_messages,
    save_message,
)

client = OpenAI()
model = "gpt-5.5"

instructions = """
You are a helpful assistant. Please provide clear and concise responses to the user's queries.
You should not provide any explanations or additional information unless explicitly asked by the user.
"""

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💀",
    layout="centered",
)

# db
db = get_db()



def load_conversation(conversation_id: int):
    msgs = get_messages(db, conversation_id)
    st.session_state.conversation_id = conversation_id
    st.session_state.messages = [{"role": m.role, "content": m.content} for m in msgs]
    st.query_params["convo"] = str(conversation_id)


def new_chat():
    st.session_state.conversation_id = None
    st.session_state.messages = []
    st.query_params.clear()


#  Bootstrap session 

if "conversation_id" not in st.session_state:
    convo_param = st.query_params.get("convo")
    if convo_param and convo_param.isdigit():
        convo_id = int(convo_param)
        convo = db.query(Conversation).filter_by(id=convo_id).first()
        if convo:
            load_conversation(convo_id)
        else:
            new_chat()
    else:
        new_chat()


#  Sidebar 

with st.sidebar:
    
    st.markdown("<h1 align='center'>😎 AI Chatbot</h1>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("New chat")
    if st.button("＋ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    model = st.selectbox(
        "Select Model",
        ["gpt-5.5", "gpt-4.1", "gpt-4o", "gpt-4o-mini"],
        index=0,
    )
 
    st.divider()

    st.subheader("Conversations")
    
    for convo in get_all_conversations(db):
        is_active = convo.id == st.session_state.conversation_id
        if st.button(
            convo.title,
            key=f"convo_{convo.id}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            load_conversation(convo.id)
            st.rerun()


#  Main chat UI 

st.subheader("Ask ai")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

   

prompt = st.chat_input("Type your message...")
    
    
if prompt:
    # Create conversation on first message
    if st.session_state.conversation_id is None:
        convo = create_conversation(db, title=prompt[:40].strip())
        st.session_state.conversation_id = convo.id
    else:
        convo = db.query(Conversation).filter_by(id=st.session_state.conversation_id).first()
        if convo and convo.title == "New Chat":
            update_conversation_title(db, st.session_state.conversation_id, prompt[:40].strip())

    save_message(db, st.session_state.conversation_id, "user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.responses.create(
            model=model,
            input=st.session_state.messages,
            instructions=instructions,
            stream=True,
        )

        for event in stream:
            if event.type == "response.output_text.delta":
                full_response += event.delta
                placeholder.markdown(full_response)

        placeholder.markdown(full_response)

    save_message(db, st.session_state.conversation_id, "assistant", full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    db.close
    st.rerun()

db.close()