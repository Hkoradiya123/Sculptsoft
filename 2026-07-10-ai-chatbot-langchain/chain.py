from langchain.chains import LLMChain, SequentialChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

# 1. Model
model = ChatOpenAI(
    model="gpt-5-mini",
    max_completion_tokens=500,
    timeout=30,
    max_retries=2,
)

title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Tu ek senior backend engineer hai. give a short title for an article about'{topic}'."
)
big_prompt = PromptTemplate(
    input_variables=["title"],
    template="Tu ek senior backend engineer hai. Write a 3 line article about '{title}'."
)
titlechain = LLMChain(llm=model, prompt=title_prompt,output_key="title")
bigchain = LLMChain(llm=model, prompt=big_prompt,output_key="blog")


chain = SequentialChain(
    chains=[titlechain, bigchain],
    input_variables=["topic"],
    output_variables=["blog"]
)

# 4. Run
result = chain.invoke({"topic": "database connection pooling"})
print(result["title"])
print(result["blog"])


# for chunk in chain.stream({"topic": "database connection pooling"}):
#     print(chunk, end="", flush=True)