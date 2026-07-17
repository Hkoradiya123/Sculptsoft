# this hugging face models doesnt give structured output
# so we need to use output parser to convert the output to structured format
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAI , ChatOpenAI
import os

dotenv.load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
    huggingfacehub_api_token=os.environ.get("HuggingFace_API_KEY")
)

model = ChatOpenAI(
    model="gpt-oss-120b", 
    base_url="http://127.0.0.1:3001/v1",
    temperature=0.4, 
    api_key=os.environ.get("FREELLM_API_KEY")
)
# 1st prompt  -> detailed report

tempelate1 = PromptTemplate(
    template="write a detailed report on {topic}",
    input_variables=["topic"])

# 2nd prompt -> summary

template2 = PromptTemplate(
    template="write 5 line summary on the following text. /n {text}",
    input_variables=["text"])

parser = StrOutputParser()

chain = tempelate1 | model | parser | template2 | model | parser # pipeline

result = chain.invoke({"topic":"black hole"})
print(result)


