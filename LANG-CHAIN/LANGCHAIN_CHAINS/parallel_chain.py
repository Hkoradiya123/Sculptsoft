from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import os

load_dotenv()

llm1 = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
    huggingfacehub_api_token=os.environ.get("HuggingFace_API_KEY"), 
)

llm2 = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-20b",
    task="text-generation",
    temperature=0.4,
    huggingfacehub_api_token=os.environ.get("HuggingFace_API_KEY"), 
)

chat_model1 = ChatHuggingFace(llm=llm1)
chat_model2 = ChatHuggingFace(llm=llm2)

prompt1 = PromptTemplate(
    template= " Generate shot and simple notes from the following text \n {text}",
    input_variables=["text"]
)

prompt2 = PromptTemplate(
    template="Generate a 5 pointer summary from the following text \n{text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template = "Merge the Provided notes and quiz into the single document \n notes -> {notes} \n quiz -> {quiz}",
    input_variables=["notes", "quiz"]
)

parser = StrOutputParser()

prompt_plaintext = PromptTemplate(
    template="""
        notes:
        
        {notes}
        
        quiz:
        
        {quiz}

        Do not return JSON.
        Do not use Markdown.
        Do not explain your answer.
        """,
    input_variables=["text"]
)

parallel_chain = RunnableParallel(
    {
        "notes": prompt1 | chat_model1 | parser,
        "quiz": prompt2 | chat_model2 | parser,
    }
)

merge_chain = prompt3  | chat_model1 | parser

chain = parallel_chain | merge_chain

result = chain.invoke({"text": "Support Vector Machine in Machine Learning"})
print("-- Parallel Chain Result --")
print(result)
print("-- Parallel Chain Graph --")
chain.get_graph().print_ascii()