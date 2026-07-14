from LANGCHAIN-RUNNABLES.runnable_passthrough import joke_gen_chain
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnablePassthrough,RunnableParallel,RunnableLambda
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
)

chat_model = ChatHuggingFace(llm=llm)

prompt1 = PromptTemplate(
    template="write a joke about {topic}",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="write explanation of joke:- {text}",
    input_variables=["text"]
)

parser = StrOutputParser()

def word_counter(text):
    return len(text.split())

joke_gen_chain = RunnableSequence(prompt1,chat_model,parser)

parallel_chain = RunnableParallel({
    "joke": RunnablePassthrough(),
    "word_count": RunnableLambda(word_counter)
})

final_chain = RunnableSequence([joke_gen_chain,parallel_chain])

result = final_chain.invoke({"topic":"AI"})
print(result)   