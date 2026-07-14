# this hugging face models doesnt give structured output
# so we need to use output parser to convert the output to structured format
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
)

model = ChatHuggingFace(llm=llm)

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


