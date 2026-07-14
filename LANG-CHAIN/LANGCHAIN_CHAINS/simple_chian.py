from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

prompt = PromptTemplate(
    template="Generate 5 interesting facts about {topic}",
    input_variables=["topic"]
)

# Local OpenAI-compatible server (freeLLM API)
model = ChatOpenAI(
    base_url="http://127.0.0.1:3001/v1",
    model="auto",
    temperature=0.4,
    api_key= "freellmapi-54d03f924917c6aa41542a694ed2722a2c85e82b85ffd0f0" 
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"topic": "black hole"})
print(result)

chain.get_graph().print_ascii() # to print the whole flow of the chain
