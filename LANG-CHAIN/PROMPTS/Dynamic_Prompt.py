# CREATING A TEMPELATE FOR PROMPT AND WITH SOME FIELDS WHICH USER WILL PROVIDE , THIS IS CALLED DYNAMIC PROMPT

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st    
from langchain_core.prompts import PromptTemplate  ,load_prompt  
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=1.7,
)

chat_model = ChatHuggingFace(llm=llm)

st.title("DEEPSEEK SUMMARIZER")

# METHOD 1 (USE JSON PROMPT WHICH IS MADE BY prompt_generator.py)
tempelate_json = load_prompt("prompt_template.json")

                  ## OR ##

# METHOD 2 (USE PROMPT TEMPLATE)

paper_input = st.selectbox("Select a paper", ["Attention is all you need", "GPT: A game-changer in natural language processing", "The Transformer: A novel approach to machine translation"])    

style_input = st.selectbox("Select a style", ["formal", "informal", "technical", "non-technical","Mathematical"])    

length_input = st.selectbox("Select a length", ["short", "medium", "long"])  

#TEMPELATE
tempelate = PromptTemplate(
    input_variables=["paper", "style", "length"],
    template="""
    You are a helpful assistant that summarizes academic papers.
    Paper: {paper}
    Style: {style}
    Length: {length}
    """
)

# prompt = tempelate.invoke({"paper": paper_input, "style": style_input, "length": length_input})


if st.button("Submit"):
    with st.spinner("Thinking..."):
        chain = tempelate | chat_model # this creates a chain ,first tempelate is applied then chat_model is applied in chain, so we dont need to invoke tempelate and chat_model separately
        result = chain.invoke({"paper": paper_input, "style": style_input, "length": length_input})# first it will apply tempelates variables then it will apply chat_model
    st.success("Result:")
    st.write(result.content)

