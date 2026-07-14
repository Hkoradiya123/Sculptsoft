from langchain_core.prompts import ChatPromptTemplate   

# dynamic set of messages
chat_template = ChatPromptTemplate([
    ("system", "You are a helpful {domain} expert."), # in this way you can create dynamic set of messages
    ("human", " Explain in simple terms, what is {topic}?")
])

prompt = chat_template.invoke({"domain": "sports", "topic": "football"})
print(prompt)   