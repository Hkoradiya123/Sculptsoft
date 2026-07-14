from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st    
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=1.7,
)

chat_model = ChatHuggingFace(llm=llm)

st.title("DEEPSEEK SUMMARIZER")

# THIS IS A STATIC PROMPT(IT MEANS USER INPUT IS PROMPT AND IT CAN CHANGE)
user_input = st.text_input("Enter your text")

if st.button("Submit"):
    with st.spinner("Thinking..."):
        result = chat_model.invoke("summarize this text: " + user_input)
    st.success("Result:")
    st.write(result.content)
