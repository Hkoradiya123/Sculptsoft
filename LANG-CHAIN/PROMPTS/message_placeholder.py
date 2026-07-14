from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chat_tempelate = ChatPromptTemplate([
    ("system", "You are a helpful CUSTOMER SUPPORT AGENT"),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', {query})
])

chat_history = []

# load chat history
with open("chat_history.txt") as f:
    chat_history.extend(f.readlines())

print(chat_history)

result = chat_tempelate.invoke({"chat_history": chat_history , "query": "where is my refund?"})
print(result.content)