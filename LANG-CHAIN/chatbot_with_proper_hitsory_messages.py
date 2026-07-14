from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage  
from dotenv import load_dotenv
import halo
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=1.7,
)

chat_model = ChatHuggingFace(llm=llm)
chat_history =  [SystemMessage(content="You are a helpful AI assistant.")]

while True:
    user_input = input("YOU: ")
    chat_history.append(HumanMessage(content=user_input))
    
    if user_input.lower() == "exit":
        print("ASSISTANT: Goodbye! Have a great day!")
        break
    with halo.Halo("Thinking..."):
        response = chat_model.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    print("\n") 
    print("ASSISTANT:", response.content)
    print("\n")


print("Chat History:")
print(chat_history)
chat_history.clear()

