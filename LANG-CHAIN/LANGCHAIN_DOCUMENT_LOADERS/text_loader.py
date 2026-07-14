from langchain_community.document_loaders import TextLoader
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_openai import OpenAI 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
import os

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,    
    huggingfacehub_api_token=os.environ.get("HuggingFace_API_KEY")
)



model = ChatHuggingFace(llm = llm)

parser = StrOutputParser()

prompt = PromptTemplate(
    template = "write summary of following content - \n {content}",
    input_variables=["content"]
)


file_path = f"{Path(__file__).parent / 'data_files' / 'example.txt'}"
# A DOCUMENT HAS TWO PARTS 
# 1. PAGE CONTENT
# 2. METADATA

loader = TextLoader(file_path,encoding = "utf-8")
data = loader.load()
print(data[0].page_content)
print(data[0].metadata)

chain = prompt | model | parser

result = chain.invoke({"content":data[0].page_content})
print(result)