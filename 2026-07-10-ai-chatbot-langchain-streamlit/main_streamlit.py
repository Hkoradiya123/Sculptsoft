from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

import streamlit as st
from core import init_components, get_context_window, SYSTEM_PROMPT
from database.db import Conversation
from database.crud import (
    get_db,
    get_all_conversations,
    create_conversation,
    update_conversation_title,
    get_messages,
    save_message,
)

load_dotenv()

MAX_TOOL_ROUNDS = 5

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

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()


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
        ["gpt-4o", "gpt-4o-mini", "gpt-4.1"],
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


#  Model + tools (re-init only when the selected model changes)

if st.session_state.get("current_model") != model:
    st.session_state.model_with_tools, st.session_state.tools_by_name, _ = init_components(
        st.session_state.indexed_files,
        model_name=model,
        warn_callback=lambda msg: st.sidebar.warning(msg),
    )
    st.session_state.current_model = model


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

        model_with_tools = st.session_state.model_with_tools
        tools_by_name = st.session_state.tools_by_name

        lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]
        for m in st.session_state.messages:
            if m["role"] == "user":
                lc_messages.append(HumanMessage(content=m["content"]))
            else:
                lc_messages.append(AIMessage(content=m["content"]))

        with st.spinner("Thinking..."):
            ai_msg = model_with_tools.invoke(get_context_window(lc_messages))

            rounds = 0
            while ai_msg.tool_calls and rounds < MAX_TOOL_ROUNDS:
                lc_messages.append(ai_msg)
                for call in ai_msg.tool_calls:
                    result = tools_by_name[call["name"]].invoke(call["args"])
                    lc_messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
                ai_msg = model_with_tools.invoke(get_context_window(lc_messages))
                rounds += 1

        full_response = ai_msg.content or ""
        placeholder.markdown(full_response)

    save_message(db, st.session_state.conversation_id, "assistant", full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    db.close()
    st.rerun()

db.close()
