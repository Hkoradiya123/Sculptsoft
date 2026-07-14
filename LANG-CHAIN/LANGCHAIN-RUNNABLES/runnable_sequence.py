from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
)

chat_model = ChatHuggingFace(llm=llm)
    
prompt = PromptTemplate(
    template="Generate a 5 pointer summary from the following text \n{text}",
    input_variables=["text"]
)

parser = StrOutputParser()

chain = RunnableSequence(prompt,chat_model,parser) # we can use "|" operator too to chain the prompt,chat_model,parser

result = chain.invoke({"text":"What is the capital of India?"})   
print(result)
