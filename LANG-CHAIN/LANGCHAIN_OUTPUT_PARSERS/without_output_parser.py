# this hugging face models doesnt give structured output
# so we need to use output parser to convert the output to structured format
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import dotenv
from langchain_core.prompts import PromptTemplate

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

prompt1 = tempelate1.invoke({"topic":"black hole"})

result = model.invoke(prompt1)
print(result.content)

prompt2 = template2.invoke({"text":result.content})
result2 = model.invoke(prompt2)
print(result2.content)