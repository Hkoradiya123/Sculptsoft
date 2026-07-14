from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint  
from dotenv import load_dotenv
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=1.7,
)

chat_model = ChatHuggingFace(llm=llm)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="tell me about langchain"),
]

result = chat_model.invoke(messages)
AI_message = AIMessage(content=result.content)
messages.append(AI_message)
print(messages)
