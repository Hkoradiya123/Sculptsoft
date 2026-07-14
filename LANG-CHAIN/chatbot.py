from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import halo
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=1.7,
)

chat_model = ChatHuggingFace(llm=llm)
chat_history =  []

while True:
    user_input = input("USER: ")
    chat_history.append(user_input)
    
    if user_input.lower() == "exit":
        print("ASSISTANT: Goodbye! Have a great day!")
        break
    with halo.Halo("Thinking..."):
        response = chat_model.invoke(chat_history)
    chat_history.append(response.content)
    print("\n")
    print("ASSISTANT:", response.content)
    print("\n")


print("Chat History:")
print(chat_history)
chat_history.clear()

# here we are using chat_history to store the chat history and then we are using it to generate the response
# but the main probelm is the ai cant understant which is user input and which is ai response so we need to make user:" ", assistant:" " like this a dictionary
# but luckily langchain has a class called ChatMessageHistory which can help us to store the chat history   
# chec messages.py file in PROMPTS folder for more details and updated versions of chatbot with history in chatbot_with_proper_hitsory_messages.py file for more details    